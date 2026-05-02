// Time Sync
function updateTime() {
    const dateTimeEl = document.getElementById('dateTime');
    if (dateTimeEl) {
        dateTimeEl.innerText = new Date().toLocaleTimeString('en-US', { hour12: false });
    }
}
setInterval(updateTime, 1000);
updateTime();

// Audio System
const alarmAudio = document.getElementById('alarmAudio');
const muteBtn = document.getElementById('muteBtn');
let isMuted = true;

if (alarmAudio && muteBtn) {
    alarmAudio.muted = isMuted;
    muteBtn.addEventListener('click', () => {
        isMuted = !isMuted;
        alarmAudio.muted = isMuted;

        if (!isMuted && document.body.classList.contains('global-alert')) {
            alarmAudio.play().catch(e => console.log('Audio init delayed:', e));
        } else {
            alarmAudio.pause();
        }

        muteBtn.innerText = isMuted ? "🔊 Mute Alarm" : "🔉 Alarm Armed";
        muteBtn.style.color = isMuted ? "" : "var(--alert-red)";
        muteBtn.style.borderColor = isMuted ? "" : "var(--alert-red)";
    });
}

// Map Initialization (HTML5 Geolocation)
const mapEl = document.getElementById('cameraMap');
let map = null;

if (mapEl) {
    map = L.map('cameraMap', { zoomControl: false, attributionControl: false }).setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                map.setView([lat, lon], 16);
                L.marker([lat, lon]).addTo(map).bindPopup("<b>LOCAL-HOST</b><br>Active GPS Location").openPopup();

                const locStatus = document.getElementById('locStatus');
                if (locStatus) locStatus.innerText = "LIVE GPS SYNCED";
            },
            () => {
                const locStatus = document.getElementById('locStatus');
                if (locStatus) locStatus.innerText = "GPS DENIED (Using Default)";

                map.setView([40.7128, -74.0060], 15);
                L.marker([40.7128, -74.0060]).addTo(map).bindPopup("<b>DEFAULT-CAM</b><br>NYC Sim").openPopup();
            }
        );
    } else {
        const locStatus = document.getElementById('locStatus');
        if (locStatus) locStatus.innerText = "GPS Unavailable";
    }
}

// Chart.js Setup
const canvasEl = document.getElementById('confidenceChart');
let confChart = null;

if (canvasEl) {
    const ctx = canvasEl.getContext('2d');
    Chart.defaults.color = '#8b949e';
    Chart.defaults.font.family = "'Outfit', sans-serif";

    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(239, 68, 68, 0.8)');
    gradient.addColorStop(0.5, 'rgba(239, 68, 68, 0.4)');
    gradient.addColorStop(1, 'rgba(239, 68, 68, 0.05)');

    confChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array(30).fill(''),
            datasets: [{
                label: 'Fire Confidence (%)',
                data: Array(30).fill(0),
                borderColor: '#ef4444',
                backgroundColor: gradient,
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    ticks: { padding: 10 },
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    border: { display: false }
                },
                x: { display: false }
            },
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            animation: { duration: 0 }
        }
    });
}

// DOM Refs
const globalStatus = document.getElementById('globalStatus');
const statusText = document.getElementById('statusText');
const pulseRing = document.querySelector('.pulse-ring');
const fireWarning = document.getElementById('fireWarning');
const dispatchOverlay = document.getElementById('dispatchOverlay');
const cpuVal = document.getElementById('cpuVal');
const cpuBar = document.getElementById('cpuBar');
const ramVal = document.getElementById('ramVal');
const ramBar = document.getElementById('ramBar');
const fpsValue = document.getElementById('fpsValue');
const snapGallery = document.getElementById('snapGallery');

// Settings Form Refs
const threshInput = document.getElementById('threshInput');
const threshDisplay = document.getElementById('threshDisplay');
const cameraSelector = document.getElementById('cameraSelector');
const emailInput = document.getElementById('emailInput');
const phoneInput = document.getElementById('phoneInput');
const modelSelect = document.getElementById('modelSelect');
const settingsForm = document.getElementById('settingsForm');

if (threshInput && threshDisplay) {
    threshInput.addEventListener('input', (e) => {
        threshDisplay.innerText = e.target.value + '%';
    });
}

if (settingsForm) {
    settingsForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const val = parseFloat(threshInput.value) / 100.0;
        const formData = new FormData();
        formData.append('threshold', val);
        formData.append('email', emailInput.value);
        formData.append('phone', phoneInput.value);
        formData.append('model_path', modelSelect.value);
        formData.append('camera_source_input', cameraSelector.value);

        fetch('/api/settings', { method: 'POST', body: formData })
            .then(res => res.json())
            .then(() => {
                const btn = settingsForm.querySelector('.btn.primary');
                btn.innerText = "Applied ✓";
                btn.style.borderColor = "var(--safe-green)";
                btn.style.color = "var(--safe-green)";

                setTimeout(() => {
                    btn.innerText = "Deploy Update";
                    btn.style.borderColor = "var(--accent-blue)";
                    btn.style.color = "var(--accent-blue)";
                }, 2000);
            })
            .catch(err => console.error('Settings failure', err));
    });
}

// Camera Selection Logic
function fetchCameras() {
    if (!cameraSelector) return;

    cameraSelector.innerHTML = '<option value="0">Probing hardware...</option>';

    fetch('/api/cameras')
        .then(res => res.json())
        .then(data => {
            if (data.cameras && data.cameras.length > 0) {
                cameraSelector.innerHTML = '';

                data.cameras.forEach(cam => {
                    const opt = document.createElement('option');
                    opt.value = cam.id;
                    opt.innerText = cam.name;
                    cameraSelector.appendChild(opt);
                });

                if (data.cameras.length === 1) {
                    const infoOpt = document.createElement('option');
                    infoOpt.disabled = true;
                    infoOpt.innerText = "— (Only 1 camera detected by system) —";
                    cameraSelector.appendChild(infoOpt);
                }
            } else {
                cameraSelector.innerHTML = '<option value="0">Default Camera (0) - Probe Failed</option>';
            }
        })
        .catch(() => {
            cameraSelector.innerHTML = '<option value="0">Default Camera (0) - Error</option>';
        });
}
fetchCameras();

// Full Screen Logic
const fullScreenBtn = document.getElementById('fullScreenBtn');
if (fullScreenBtn) {
    fullScreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen()
                .catch(err => console.log(`Fullscreen error: ${err.message}`));
            fullScreenBtn.innerText = "⛶ Exit Full Screen";
        } else {
            document.exitFullscreen();
            fullScreenBtn.innerText = "⛶ Full Screen";
        }
    });
}

// Gallery
function renderGallery(incidents) {
    if (!incidents || !snapGallery) return;

    snapGallery.innerHTML = '';

    if (incidents.length === 0) {
        snapGallery.innerHTML = '<div style="text-align:center;color:var(--text-secondary);padding:2rem;">No matching incidents found.</div>';
        return;
    }

    incidents.forEach(inc => {
        const confPercent = (inc.confidence * 100).toFixed(1);
        const card = document.createElement('div');
        card.className = 'snapshot-card';

        const displayPath = inc.snapshot_path.startsWith('static/')
            ? inc.snapshot_path.substring(7)
            : inc.snapshot_path;

        const safeTimestamp = String(inc.timestamp).replace(/'/g, "\\'");

        card.innerHTML = `
            <img src="/static/${displayPath}" alt="Fire Snapshot">
            <div class="snapshot-info">
                <span>Threat Confi.: <strong>${confPercent}%</strong></span>
                <span class="time">${inc.timestamp}</span>
            </div>
            <button class="btn btn-pdf" onclick="exportPDF(this, '${displayPath}', '${confPercent}', '${safeTimestamp}')">PDF</button>
        `;

        snapGallery.appendChild(card);
    });
}

// Corrected PDF Export
window.exportPDF = async function (btn, imgPath, conf, timestamp) {
    const originalText = btn.innerText;
    btn.innerText = "Preparing...";
    btn.disabled = true;

    try {
        if (typeof window.jspdf === 'undefined') {
            await new Promise((resolve, reject) => {
                const script = document.createElement('script');
                script.src = "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js";
                script.onload = resolve;
                script.onerror = reject;
                document.head.appendChild(script);
            });
        }

        const imgUrl = imgPath.startsWith('/static/') ? imgPath : `/static/${imgPath}`;
        console.log("PDF image URL:", imgUrl);

        const base64 = await new Promise((resolve, reject) => {
            const img = new Image();

            img.onload = function () {
                try {
                    const canvas = document.createElement('canvas');
                    canvas.width = img.naturalWidth || img.width;
                    canvas.height = img.naturalHeight || img.height;

                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);

                    const dataUrl = canvas.toDataURL('image/jpeg', 0.95);
                    resolve(dataUrl);
                } catch (err) {
                    reject(err);
                }
            };

            img.onerror = function () {
                reject(new Error(`Image failed to load: ${imgUrl}`));
            };

            img.src = imgUrl + (imgUrl.includes('?') ? '&' : '?') + 't=' + Date.now();
        });

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF({
            unit: 'pt',
            format: 'letter',
            orientation: 'portrait'
        });

        // Background
        doc.setFillColor(255, 255, 255);
        doc.rect(0, 0, 612, 792, 'F');

        // Header
        doc.setFont("helvetica", "bold");
        doc.setTextColor(220, 38, 38);
        doc.setFontSize(20);
        doc.text(`FireGuard Alert: Critical Threat Detected (${conf}%)`, 40, 55);

        // Line
        doc.setDrawColor(210, 210, 210);
        doc.setLineWidth(1);
        doc.line(40, 70, 572, 70);

        // Body text
        doc.setTextColor(0, 0, 0);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(15);
        doc.text("Emergency Dispatch Report", 40, 105);

        doc.setFont("helvetica", "normal");
        doc.setFontSize(12);
        doc.text("A critical fire threat was detected by the monitoring system.", 40, 132);

        doc.setFont("helvetica", "bold");
        doc.text("Status:", 40, 160);
        doc.setFont("helvetica", "normal");
        doc.text("Confirmed", 88, 160);

        doc.setFont("helvetica", "bold");
        doc.text("Time:", 40, 182);
        doc.setFont("helvetica", "normal");
        doc.text(String(timestamp), 78, 182);

        doc.setFont("helvetica", "bold");
        doc.text("Node:", 40, 204);
        doc.setFont("helvetica", "normal");
        doc.text("CAM-01", 78, 204);

        doc.setTextColor(90, 90, 90);
        doc.setFont("helvetica", "italic");
        doc.text("Attached below is the recorded incident snapshot.", 40, 232);

        // Image section
        doc.setDrawColor(210, 210, 210);
        doc.line(40, 248, 572, 248);

        const imgX = 56;
        const imgY = 270;
        const maxW = 500;
        const maxH = 340;

        const imgProps = doc.getImageProperties(base64);
        let drawW = maxW;
        let drawH = (imgProps.height * drawW) / imgProps.width;

        if (drawH > maxH) {
            drawH = maxH;
            drawW = (imgProps.width * drawH) / imgProps.height;
        }

        const centeredX = imgX + (maxW - drawW) / 2;
        const centeredY = imgY + (maxH - drawH) / 2;

        doc.setDrawColor(120, 120, 120);
        doc.rect(imgX, imgY, maxW, maxH);
        doc.addImage(base64, 'JPEG', centeredX, centeredY, drawW, drawH);

        // Footer
        doc.setDrawColor(210, 210, 210);
        doc.line(40, 650, 572, 650);

        doc.setFont("helvetica", "normal");
        doc.setFontSize(8);
        doc.setTextColor(130, 130, 130);
        doc.text("SECURE VERSION - GENERATED BY ENTERPRISE FIREGUARD V3.0", 306, 670, { align: 'center' });

        const incidentId = Math.random().toString(36).slice(2, 10).toUpperCase();
        doc.text(`INCIDENT_ID: ${incidentId}`, 306, 684, { align: 'center' });

        const safeFileName = `FireGuard_${String(timestamp).replace(/[\\/:*?"<>| ,]+/g, '_')}.pdf`;
        doc.save(safeFileName);

        btn.innerText = "Saved";
        setTimeout(() => {
            btn.innerText = originalText;
            btn.disabled = false;
        }, 2000);

    } catch (e) {
        console.error("PDF Gen Error:", e);
        btn.innerText = "PDF Error";

        setTimeout(() => {
            btn.innerText = originalText;
            btn.disabled = false;
        }, 2500);
    }
};

// Initial Database Fetch
fetch('/api/incidents')
    .then(r => r.json())
    .then(data => {
        if (data.incidents && data.incidents.length > 0) {
            renderGallery(data.incidents);
        }
    });

// Handle Server-Sent Events stream
const eventSource = new EventSource('/api/status');
let cachedIncidentsStr = "";

eventSource.onmessage = (event) => {
    let data;
    try {
        data = JSON.parse(event.data);
    } catch {
        return;
    }

    // Server Metrics
    if (cpuVal) {
        cpuVal.innerText = data.cpu_usage.toFixed(1) + '%';
        cpuBar.style.width = data.cpu_usage + '%';
    }

    if (ramVal) {
        ramVal.innerText = data.ram_usage.toFixed(1) + '%';
        ramBar.style.width = data.ram_usage + '%';
    }

    if (fpsValue) fpsValue.innerText = data.fps;

    // Initial form sync
    if (!window.isSettingsSynced) {
        if (data.threshold !== undefined && threshInput) {
            const srvThresh = Math.round(data.threshold * 100);
            threshInput.value = srvThresh;
            threshDisplay.innerText = srvThresh + '%';
        }
        if (data.receiver_email && emailInput) emailInput.value = data.receiver_email;
        if (data.receiver_phone && phoneInput) phoneInput.value = data.receiver_phone;
        if (data.model_path && modelSelect) modelSelect.value = data.model_path;
        window.isSettingsSynced = true;
    }

    // Live threshold sync
    if (
        data.threshold !== undefined &&
        threshInput &&
        document.activeElement !== threshInput
    ) {
        const srvThresh = Math.round(data.threshold * 100);
        if (Math.abs(srvThresh - Number(threshInput.value)) >= 1) {
            threshInput.value = srvThresh;
            threshDisplay.innerText = srvThresh + '%';
        }
    }

    // Live Chart Update
    if (confChart) {
        confChart.data.datasets[0].data.shift();
        confChart.data.datasets[0].data.push(data.confidence * 100);
        confChart.update();
    }

    // Alert Handling
    if (data.fire_detected) {
        document.body.classList.add('global-alert');

        if (globalStatus) globalStatus.className = 'global-status alert';
        if (statusText) statusText.innerText = 'CRITICAL THREAT';

        if (pulseRing) {
            pulseRing.style.backgroundColor = 'var(--alert-red)';
            pulseRing.style.boxShadow = '0 0 10px var(--alert-red)';
        }

        if (fireWarning) fireWarning.classList.add('active');

        if (!isMuted && alarmAudio && alarmAudio.paused) {
            const promise = alarmAudio.play();
            if (promise !== undefined) {
                promise.catch(err => console.log('Audio autoplay blocked', err));
            }
        }
    } else {
        document.body.classList.remove('global-alert');

        if (globalStatus) globalStatus.className = 'global-status';
        if (statusText) statusText.innerText = 'System Idle';

        if (pulseRing) {
            pulseRing.style.backgroundColor = 'var(--safe-green)';
            pulseRing.style.boxShadow = '0 0 10px var(--safe-green)';
        }

        if (fireWarning) fireWarning.classList.remove('active');
        if (alarmAudio) alarmAudio.pause();
    }

    // Dispatch
    if (dispatchOverlay) {
        if (data.dispatch_active) dispatchOverlay.classList.add('active');
        else dispatchOverlay.classList.remove('active');
    }

    // Live incident updates
    const currentIncidentsStr = JSON.stringify(data.recent_incidents);
    if (cachedIncidentsStr !== currentIncidentsStr) {
        cachedIncidentsStr = currentIncidentsStr;
        renderGallery(data.recent_incidents);
    }
};

eventSource.onerror = () => {
    if (statusText) statusText.innerText = 'Connection Offline';
    if (globalStatus) globalStatus.className = 'global-status';
    if (pulseRing) {
        pulseRing.style.backgroundColor = 'gray';
        pulseRing.style.boxShadow = 'none';
    }
};