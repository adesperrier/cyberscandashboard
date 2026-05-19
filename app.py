from __future__ import annotations
import socket
import ipaddress
import os
import re
import shutil
import subprocess
import uuid
from collections import deque
from datetime import datetime

import nmap
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-change-me")

MAX_NETWORK_HOSTS = 1024
HISTORY = deque(maxlen=5)

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
)

SCAN_PRESETS = {
    "quick": {
        "args": "-sV --top-ports 100",
        "label": "Quick (top 100 ports)",
    },
    "common": {
        "args": "-sV -p 20,21,22,23,25,53,67,68,80,110,123,135,139,143,161,389,443,445,465,514,587,636,993,995,1433,3306,3389,5432,5984,6379,7000,8080,8443,9200,27017",
        "label": "Courants (services web, DB, RDP, etc)",
    },
    "full": {
        "args": "-sV -p 1-65535",
        "label": "Complet (tous les ports - LENT)",
    },
}

KNOWN_VULNERABILITIES = {
    "ftp": [
        {
            "version": "*",
            "issue": "FTP sans chiffrage",
            "risk": "Critique",
            "solution": "Désactiver FTP. Utiliser SFTP/SCP ou SSH.",
        }
    ],
    "telnet": [
        {
            "version": "*",
            "issue": "Telnet sans chiffrage",
            "risk": "Critique",
            "solution": "Désactiver Telnet. Utiliser SSH.",
        }
    ],
    "http": [
        {
            "version": "*",
            "issue": "HTTP sans SSL/TLS",
            "risk": "Élevé",
            "solution": "Configurer HTTPS/TLS. Rediriger HTTP vers HTTPS.",
        }
    ],
    "ssh": [
        {
            "version": "OpenSSH 1.*",
            "issue": "OpenSSH très ancien (vulnérable)",
            "risk": "Élevé",
            "solution": "Mettre à jour SSH à la dernière version stable.",
        }
    ],
    "smb": [
        {
            "version": "*",
            "issue": "SMB exposé sur le réseau",
            "risk": "Élevé",
            "solution": "Restreindre SMB au réseau interne uniquement. Utiliser VPN.",
        }
    ],
    "mysql": [
        {
            "version": "*",
            "issue": "MySQL exposé publiquement",
            "risk": "Critique",
            "solution": "Ne pas exposer MySQL. Utiliser tunnel SSH ou proxy.",
        }
    ],
    "postgresql": [
        {
            "version": "*",
            "issue": "PostgreSQL exposé publiquement",
            "risk": "Critique",
            "solution": "Ne pas exposer PostgreSQL. Utiliser tunnel SSH ou proxy.",
        }
    ],
    "mongodb": [
        {
            "version": "*",
            "issue": "MongoDB sans authentification par défaut",
            "risk": "Critique",
            "solution": "Activer authentification. Restreindre accès réseau.",
        }
    ],
    "redis": [
        {
            "version": "*",
            "issue": "Redis sans mot de passe par défaut",
            "risk": "Critique",
            "solution": "Configurer mot de passe Redis. Restreindre accès réseau.",
        }
    ],
}


def normalize_target(value: str) -> tuple[str, str]:
    value = (value or "").strip()
    if not value:
        raise ValueError("La cible est requise.")

    try:
        ip = ipaddress.ip_address(value)
        return str(ip), "ip"
    except ValueError:
        pass

    try:
        network = ipaddress.ip_network(value, strict=False)
    except ValueError:
        network = None

    if network:
        if network.num_addresses > MAX_NETWORK_HOSTS:
            raise ValueError(
                f"Plage trop large : maximum {MAX_NETWORK_HOSTS} hôtes autorisés."
            )
        return str(network), "network"

    if DOMAIN_RE.fullmatch(value):
        return value.lower().rstrip("."), "domain"

    raise ValueError("Cible invalide. Utilise une IP, un domaine ou un CIDR.")


def get_arp_neighbors() -> list[dict]:
    """Récupère les voisins ARP (hôtes actifs sur le réseau local)."""
    try:
        if os.name == "nt":
            output = subprocess.check_output(["arp", "-a"], text=True)
            lines = output.split("\n")
            neighbors = []
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        ipaddress.ip_address(parts[0])
                        mac = parts[1] if len(parts) > 1 else "?"
                        neighbors.append(
                            {
                                "ip": parts[0],
                                "mac": mac,
                                "state": "dynamic",
                            }
                        )
                    except ValueError:
                        pass
            return neighbors
        else:
            output = subprocess.check_output(
                ["arp", "-a"], text=True, stderr=subprocess.DEVNULL
            )
            lines = output.split("\n")
            neighbors = []
            for line in lines:
                if "(" in line and ")" in line:
                    ip_match = re.search(r"\(([0-9.]+)\)", line)
                    mac_match = re.search(
                        r"([0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2})",
                        line,
                        re.IGNORECASE,
                    )
                    if ip_match:
                        neighbors.append(
                            {
                                "ip": ip_match.group(1),
                                "mac": mac_match.group(1) if mac_match else "?",
                                "state": "dynamic",
                            }
                        )
            return neighbors
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def ping_host(ip: str, timeout: int = 2) -> bool:
    """Vérifie si un hôte est actif via ICMP (ping)."""
    try:
        if os.name == "nt":
            subprocess.check_output(
                ["ping", "-n", "1", "-w", str(timeout * 1000), ip],
                stderr=subprocess.DEVNULL,
                timeout=timeout + 1,
            )
        else:
            subprocess.check_output(
                ["ping", "-c", "1", "-W", str(timeout * 1000), ip],
                stderr=subprocess.DEVNULL,
                timeout=timeout + 1,
            )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False


def dns_lookup(target: str) -> dict:
    """Effectue une recherche DNS (forward et reverse)."""
    result = {"forward": None, "reverse": None, "error": None}
    try:
        if re.match(r"^[0-9.]+$", target):
            result["forward"] = socket.gethostbyaddr(target)[0]
            result["reverse"] = target
        else:
            result["forward"] = target
            result["reverse"] = socket.gethostbyname(target)
    except (socket.gaierror, socket.herror):
        result["error"] = "Résolution DNS impossible"
    return result


def traceroute(target: str, hops: int = 15) -> list[dict]:
    """Trace la route vers la cible."""
    try:
        if os.name == "nt":
            output = subprocess.check_output(
                ["tracert", "-h", str(hops), target],
                stderr=subprocess.DEVNULL,
                timeout=30,
                text=True,
            )
        else:
            output = subprocess.check_output(
                ["traceroute", "-m", str(hops), target],
                stderr=subprocess.DEVNULL,
                timeout=30,
                text=True,
            )

        hops_list = []
        for line in output.split("\n"):
            if re.search(r"\d+\.", line):
                match = re.search(r"(\[?[0-9.]+\]?)", line)
                if match:
                    hops_list.append({"hop": line.strip()})
        return hops_list
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return [{"error": "Traceroute impossible"}]


def whois_lookup(target: str) -> dict:
    """Récupère les infos WHOIS (enregistrement de domaine)."""
    result = {"domain": target, "info": None, "error": None}
    try:
        if os.name == "nt":
            result["error"] = "WHOIS non disponible sur Windows (nativement)"
        else:
            output = subprocess.check_output(
                ["whois", target],
                stderr=subprocess.DEVNULL,
                timeout=10,
                text=True,
            )
            lines = []
            for line in output.split("\n")[:20]:
                if line.strip():
                    lines.append(line.strip())
            result["info"] = "\n".join(lines) if lines else "Aucune information"
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        result["error"] = "Commande WHOIS non trouvée. Installe: apt-get install whois"
    return result


def compare_scans(target_ip: str) -> dict:
    """Compare le scan actuel avec le scan précédent pour l'IP."""
    if target_ip not in SCAN_DB:
        return {"has_previous": False, "comparison": None}

    previous_scan = SCAN_DB[target_ip]
    return {
        "has_previous": True,
        "previous_scan": previous_scan,
        "timestamp": previous_scan.get("timestamp"),
    }



def build_nmap_search_path() -> tuple[str, ...]:
    exe_name = "nmap.exe" if os.name == "nt" else "nmap"
    candidates = []

    env_path = os.environ.get("NMAP_PATH", "").strip()
    if env_path:
        env_path = env_path.strip('"')
        if os.path.isdir(env_path):
            env_path = os.path.join(env_path, exe_name)
        candidates.append(env_path)

    found = shutil.which(exe_name)
    if found:
        candidates.append(found)

    if os.name == "nt":
        candidates.extend(
            [
                r"C:\Program Files\Nmap\nmap.exe",
                r"C:\Program Files (x86)\Nmap\nmap.exe",
            ]
        )
    else:
        candidates.extend(["/usr/bin/nmap", "/usr/local/bin/nmap", "/snap/bin/nmap"])

    candidates.append(exe_name)

    seen = set()
    deduped = []
    for path in candidates:
        if not path:
            continue
        normalized = os.path.normpath(path)
        if normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(path)

    return tuple(deduped)


def check_vulnerabilities(service: str, product: str, version: str) -> list[dict]:
    service_lower = service.lower()
    product_lower = (product or "").lower()
    version_lower = (version or "").lower()

    vulns = []
    if service_lower in KNOWN_VULNERABILITIES:
        for vuln in KNOWN_VULNERABILITIES[service_lower]:
            if vuln["version"] == "*" or version_lower.startswith(vuln["version"]):
                vulns.append(vuln)

    return vulns


def run_scan(target: str, scan_preset: str = "quick", custom_ports: str = "") -> dict:
    if scan_preset not in SCAN_PRESETS and not custom_ports:
        scan_preset = "quick"

    if custom_ports and custom_ports.strip():
        scan_args = f"-sV -p {custom_ports.strip()}"
    else:
        scan_args = SCAN_PRESETS[scan_preset]["args"]

    scanner = nmap.PortScanner(nmap_search_path=build_nmap_search_path())
    started = datetime.now()
    scanner.scan(hosts=target, arguments=scan_args)
    elapsed = (datetime.now() - started).total_seconds()

    hosts = []
    total_open_ports = 0

    for host in scanner.all_hosts():
        host_state = scanner[host].state()
        hostname = scanner[host].hostname() or ""
        ports = []
        open_count = 0

        for proto in scanner[host].all_protocols():
            for port in sorted(scanner[host][proto].keys()):
                port_info = scanner[host][proto][port]
                state = port_info.get("state", "")
                if state == "open":
                    open_count += 1

                service = port_info.get("name", "")
                product = port_info.get("product", "")
                version = port_info.get("version", "")
                vulns = check_vulnerabilities(service, product, version)

                ports.append(
                    {
                        "port": port,
                        "proto": proto,
                        "state": state,
                        "service": service,
                        "product": product,
                        "version": version,
                        "extrainfo": port_info.get("extrainfo", ""),
                        "vulnerabilities": vulns,
                    }
                )

        total_open_ports += open_count
        hosts.append(
            {
                "address": host,
                "hostname": hostname,
                "state": host_state,
                "ports": ports,
                "open_count": open_count,
            }
        )

    return {
        "scan_id": uuid.uuid4().hex,
        "target": target,
        "started_at": started.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": datetime.now().isoformat(),
        "elapsed": elapsed,
        "scan_args": scan_args,
        "hosts": hosts,
        "open_ports": total_open_ports,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        target_input = request.form.get("target", "")
        scan_preset = request.form.get("scan_preset", "quick")
        custom_ports = request.form.get("custom_ports", "")

        try:
            target, target_type = normalize_target(target_input)
            result = run_scan(target, scan_preset, custom_ports)
            result["target_type"] = target_type

            HISTORY.appendleft(
                {
                    "scan_id": result["scan_id"],
                    "target": result["target"],
                    "started_at": result["started_at"],
                    "elapsed": result["elapsed"],
                    "hosts": len(result["hosts"]),
                    "open_ports": result["open_ports"],
                }
            )
        except nmap.PortScannerError as exc:
            error = (
                "Nmap introuvable. Installe-le ou définis NMAP_PATH vers nmap.exe "
                f"(ou son dossier). Détail: {exc}"
            )
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "index.html",
        result=result,
        error=error,
        history=list(HISTORY),
        scan_presets=SCAN_PRESETS,
    )


@app.route("/api/arp-neighbors")
def api_arp_neighbors():
    """Retourne la liste des voisins ARP détectés."""
    neighbors = get_arp_neighbors()
    return jsonify(neighbors)


@app.route("/api/ping")
def api_ping():
    """Teste si un hôte est actif."""
    ip = request.args.get("ip", "").strip()
    if not ip:
        return jsonify({"error": "IP requise"}), 400
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return jsonify({"error": "IP invalide"}), 400
    alive = ping_host(ip)
    return jsonify({"ip": ip, "alive": alive})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
