// ---------------- UPLOAD FILE (FIXED) ----------------
function uploadFile() {

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("/", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(html => {

        // Parse returned HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        // Extract only the plot section
        const newPlot = doc.querySelector(".map-container");

        if (newPlot) {
            document.querySelector(".map-container").innerHTML = newPlot.innerHTML;
        }

        // Add layer to sidebar
        addLayer(file.name);
    })
    .catch(error => {
        console.error("Upload failed:", error);
        alert("Upload failed");
    });
}


// ---------------- ADD LAYER ----------------
function addLayer(name) {

    const list = document.getElementById("layerList");

    if (list) {

        // Avoid duplicates
        const existing = Array.from(list.children).some(li => li.textContent === name);
        if (existing) return;

        const li = document.createElement("li");
        li.textContent = name;

        list.appendChild(li);
    }
}


// ---------------- EXPORT PNG ----------------
function exportPNG() {
    window.location.href = "/export/png";
}


// ---------------- EXPORT 3D ----------------
function export3D() {

    const format = document.getElementById("format").value;

    window.location.href = "/export/3d/" + format;
}