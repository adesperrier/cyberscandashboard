const scanForm = document.getElementById('scanForm');
const resultsSection = document.getElementById('resultsSection');
const detailsModal = new bootstrap.Modal(document.getElementById('detailsModal'));

scanForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const target = document.getElementById('target').value;
    const mode = document.getElementById('mode').value;
    const customPorts = document.getElementById('customPorts').value;

    try {
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
    }
});

function displayResults(data) {
    const resultsBody = document.getElementById('resultsBody');
    resultsBody.innerHTML = '';

    const ports = data.ports || [];
    ports.forEach(port => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${port.port}</strong></td>
            <td><span class="status-badge status-${port.state}">${port.state}</span></td>
            <td>${port.service}</td>
            <td>${port.product || '-'}</td>
            <td><span class="status-badge risk-${port.risk.toLowerCase()}">${port.risk}</span></td>
            <td><button class="btn-details" onclick="showDetails('${JSON.stringify(port).replace(/'/g, "&#39;")}')">Details</button></td>
        `;
        resultsBody.appendChild(row);
    });

    updateStatistics(data);
    resultsSection.style.display = 'block';
}

function updateStatistics(data) {
    const summary = data.summary || {};
    document.getElementById('openPorts').textContent = summary.open_ports || 0;
    document.getElementById('servicesCount').textContent = summary.total_ports || 0;
    document.getElementById('criticalCount').textContent = summary.critical_issues || 0;
}

function showDetails(portJson) {
    const port = JSON.parse(portJson);
    const modalBody = document.getElementById('modalBody');

    let issuesHtml = '';
    if (port.issues && port.issues.length > 0) {
        issuesHtml = port.issues.map(issue => `<div style="margin-top: 0.5rem; color: #00ff88;">- ${issue}</div>`).join('');
    }

    modalBody.innerHTML = `
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
            element.innerHTML = `
                <div class="history-target">Target: ${item.target}</div>
                <div class="history-time">Time: ${timeStr}</div>
                <div>
                    <span class="history-stat">${item.summary.open_ports}</span> open |
                    <span class="history-stat">${item.summary.total_ports}</span> total |
                    <span style="color: #ff006e;">${item.summary.critical_issues}</span> critical |
                    <span style="color: #ff4400;">${item.summary.high_issues}</span> high
                </div>
            `;
            historyList.appendChild(element);
        });
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

window.addEventListener('load', loadHistory);
