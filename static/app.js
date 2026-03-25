let currentSessionId = null;

function showError(msg) {
    const toast = document.getElementById("errorToast");
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(() => {
        toast.classList.remove("show");
    }, 5000);
}

function showLoading(show) {
    document.getElementById("loadingOverlay").style.display = show ? "flex" : "none";
}

function handleFileSelect() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) return;

    // Show loading UI
    showLoading(true);
    document.getElementById("file-status").textContent = `Uploading ${file.name}...`;

    const formData = new FormData();
    formData.append("file", file);

    fetch("/", {
        method: "POST",
        body: formData
    })
    .then(async res => {
        const data = await res.json().catch(() => null);
        
        if (!res.ok) {
            const errorMsg = data && data.error ? data.error : `Server processing error (${res.status})`;
            throw new Error(errorMsg);
        }
        return data;
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }

        currentSessionId = data.session_id;

        // Render Plotly
        renderPlot(data.x, data.y, data.z);

        // Update UI
        updateLayerUI(file.name);
        document.getElementById("export-controls").style.display = "flex";
        document.getElementById("file-status").textContent = "Upload complete";
    })
    .catch(err => {
        console.error(err);
        showError(err.message);
        document.getElementById("file-status").textContent = "Upload failed";
    })
    .finally(() => {
        showLoading(false);
        // Clear input safely
        fileInput.value = "";
    });
}

function renderPlot(x, y, z) {
    const container = document.getElementById("map-container");
    container.innerHTML = `
        <div style="display: flex; width: 100%; height: 100%; gap: 1rem; padding: 1rem;">
            <div id='plot2d' style='flex: 1; height: 100%;'></div>
            <div id='plot3d' style='flex: 1; height: 100%;'></div>
        </div>
    `;

    const plot2dDiv = document.getElementById("plot2d");
    const plot3dDiv = document.getElementById("plot3d");

    const contour = {
        z: z,
        x: x[0],
        y: y.map(row => row[0]),
        type: "contour",
        colorscale: "Viridis",
        showscale: false
    };

    const surface = {
        z: z,
        x: x,
        y: y,
        type: "surface",
        colorscale: "Viridis"
    };

    const layout2d = {
        title: "2D Bathymetry",
        margin: { l: 40, r: 20, b: 40, t: 50 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#f8fafc' },
        xaxis: { gridcolor: '#2d313b', zerolinecolor: '#2d313b' },
        yaxis: { gridcolor: '#2d313b', zerolinecolor: '#2d313b' }
    };

    const layout3d = {
        title: "3D Surface Map",
        margin: { l: 0, r: 0, b: 0, t: 50 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#f8fafc' },
        scene: {
            xaxis: { gridcolor: '#2d313b', zerolinecolor: '#2d313b' },
            yaxis: { gridcolor: '#2d313b', zerolinecolor: '#2d313b' },
            zaxis: { gridcolor: '#2d313b', zerolinecolor: '#2d313b' }
        }
    };

    Plotly.newPlot(plot2dDiv, [contour], layout2d, {responsive: true});
    Plotly.newPlot(plot3dDiv, [surface], layout3d, {responsive: true});
}

function updateLayerUI(name) {
    const list = document.getElementById("layerList");
    list.className = "layer-item";
    list.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 6px;"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
        ${name}
    `;
}

function exportPNG() {
    if (!currentSessionId) return showError("No session active");
    window.location.href = `/export/png/${currentSessionId}`;
}

function export3D() {
    if (!currentSessionId) return showError("No session active");
    const format = document.getElementById("format").value;
    window.location.href = `/export/3d/${currentSessionId}/${format}`;
}