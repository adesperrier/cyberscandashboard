const scanForm = document.getElementById('scanForm');
const resultsSection = document.getElementById('resultsSection');
const detailsModal = new bootstrap.Modal(document.getElementById('detailsModal'));

let currentResults = [];
let sortColumn = null;
let sortDirection = 'asc';

scanForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const target = document.getElementById('target').value;
    const mode = document.getElementById('mode').value;
    const customPorts = document.getElementById('customPorts').value;
    const scanButton = scanForm.querySelector('button[type="submit"]');

    try {
        // Show loading state
        scanButton.disabled = true;
        scanButton.innerHTML = '<span class="spinner"></span>Scanning...';

        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                target: target,
                mode: mode,
                custom_ports: customPorts
            })
        });

        const data = await response.json();

        if (response.ok) {
            displayResults(data);
            loadHistory();
        } else {
            alert('Scan failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        // Reset button
        scanButton.disabled = false;
        scanButton.innerHTML = 'Scan';
    }
});

function displayResults(data) {
    currentResults = data.ports || [];
    sortColumn = null;
    sortDirection = 'asc';
    renderResults();
    updateStatistics(data);
    resultsSection.style.display = 'block';
}

function renderResults() {
    const resultsBody = document.getElementById('resultsBody');
    resultsBody.innerHTML = '';
    
    currentResults.forEach(port => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${port.host}</strong></td>
            <td><strong>${port.port}</strong></td>
            <td><span class="status-badge status-${port.state}">${port.state}</span></td>
            <td>${port.service}</td>
            <td>${port.product || '-'}</td>
            <td><span class="status-badge risk-${port.risk.toLowerCase()}">${port.risk}</span></td>
            <td><button class="btn-details" onclick="showDetails(event)">Details</button></td>
        `;
        row.dataset.port = JSON.stringify(port);
        resultsBody.appendChild(row);
    });
    
    updateSortIndicators();
}

function sortResults(column) {
    // Si on clique sur la même colonne, inverser la direction
    if (sortColumn === column) {
        sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        sortColumn = column;
        sortDirection = 'asc';
    }
    
    // Trier les résultats
    currentResults.sort((a, b) => {
        let aVal = a[column];
        let bVal = b[column];
        
        // Gérer les valeurs nulles
        if (aVal === null || aVal === undefined) aVal = '';
        if (bVal === null || bVal === undefined) bVal = '';
        
        // Tri numérique pour les ports et nombres
        if (column === 'port') {
            aVal = parseInt(aVal);
            bVal = parseInt(bVal);
            return sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
        }
        
        // Tri alphabétique
        aVal = String(aVal).toLowerCase();
        bVal = String(bVal).toLowerCase();
        
        if (sortDirection === 'asc') {
            return aVal.localeCompare(bVal);
        } else {
            return bVal.localeCompare(aVal);
        }
    });
    
    renderResults();
}

function updateSortIndicators() {
    // Réinitialiser tous les indicateurs
    document.querySelectorAll('.sort-indicator').forEach(indicator => {
        indicator.classList.remove('active-asc', 'active-desc');
    });
    
    // Ajouter l'indicateur pour la colonne active
    if (sortColumn) {
        const headers = document.querySelectorAll('.table-modern th');
        const columnIndex = {
            'host': 0,
            'port': 1,
            'state': 2,
            'service': 3,
            'product': 4,
            'risk': 5
        }[sortColumn];
        
        if (columnIndex !== undefined && headers[columnIndex]) {
            const indicator = headers[columnIndex].querySelector('.sort-indicator');
            if (indicator) {
                indicator.classList.add(sortDirection === 'asc' ? 'active-asc' : 'active-desc');
            }
        }
    }
}

function updateStatistics(data) {
    const summary = data.summary || {};
    document.getElementById('openPorts').textContent = summary.open_ports || 0;
    document.getElementById('servicesCount').textContent = summary.total_ports || 0;
    document.getElementById('criticalCount').textContent = summary.critical_issues || 0;
}

function showDetails(event) {
    event.preventDefault();
    const row = event.target.closest('tr');
    const port = JSON.parse(row.dataset.port);
    const modalBody = document.getElementById('modalBody');

    let issuesHtml = '';
    if (port.issues && port.issues.length > 0) {
        issuesHtml = port.issues.map(issue => `<div style="margin-top: 0.5rem; color: #00ff88;">- ${issue}</div>`).join('');
    }

    modalBody.innerHTML = `
        <div class="modal-item">
            <div class="modal-label">Host</div>
            <div>${port.host}</div>
        </div>
        <div class="modal-item">
            <div class="modal-label">Port Number</div>
            <div>${port.port}</div>
        </div>
        <div class="modal-item">
            <div class="modal-label">State</div>
            <div><span class="status-badge status-${port.state}">${port.state}</span></div>
        </div>
        <div class="modal-item">
            <div class="modal-label">Service</div>
            <div>${port.service}</div>
        </div>
        <div class="modal-item">
            <div class="modal-label">Product</div>
            <div>${port.product || 'Unknown'}</div>
        </div>
        <div class="modal-item">
            <div class="modal-label">Version</div>
            <div>${port.version || 'Unknown'}</div>
        </div>
        <div class="modal-item">
            <div class="modal-label">Risk Level</div>
            <div><span class="status-badge risk-${port.risk.toLowerCase()}">${port.risk}</span></div>
        </div>
        ${issuesHtml ? `<div class="modal-item">
            <div class="modal-label">Security Issues</div>
            ${issuesHtml}
        </div>` : ''}
    `;

    detailsModal.show();
}

async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const history = await response.json();

        const historyList = document.getElementById('historyList');
        historyList.innerHTML = '';

        if (history.length === 0) {
            historyList.innerHTML = '<p style="color: #999;">No scans yet</p>';
            return;
        }

        history.forEach(item => {
            const date = new Date(item.timestamp);
            const timeStr = date.toLocaleString();

            const element = document.createElement('div');
            element.className = 'history-item';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'history-content';
            contentDiv.innerHTML = `
                <div class="history-target">Target: ${item.target}</div>
                <div class="history-time">Time: ${timeStr}</div>
                <div>
                    <span class="history-stat">${item.summary.open_ports}</span> open |
                    <span class="history-stat">${item.summary.total_ports}</span> total |
                    <span style="color: #ff006e;">${item.summary.critical_issues}</span> critical |
                    <span style="color: #ff4400;">${item.summary.high_issues}</span> high
                </div>
            `;
            contentDiv.onclick = () => loadScanDetails(item.filename);
            
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'history-actions';
            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'btn-delete';
            deleteBtn.innerHTML = '✕ Delete';
            deleteBtn.onclick = (e) => {
                e.stopPropagation();
                deleteScan(item.filename);
            };
            actionsDiv.appendChild(deleteBtn);
            
            element.appendChild(contentDiv);
            element.appendChild(actionsDiv);
            historyList.appendChild(element);
        });
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

async function loadScanDetails(filename) {
    try {
        const response = await fetch(`/api/scan/${filename}`);
        if (!response.ok) {
            alert('Error loading scan details');
            return;
        }
        const data = await response.json();
        displayResults(data);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
        alert('Error loading scan details: ' + error.message);
    }
}

async function deleteScan(filename) {
    if (!confirm('Delete this scan? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/scan/${filename}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            alert('Error deleting scan');
            return;
        }
        
        loadHistory();
    } catch (error) {
        alert('Error deleting scan: ' + error.message);
    }
}

window.addEventListener('load', loadHistory);
