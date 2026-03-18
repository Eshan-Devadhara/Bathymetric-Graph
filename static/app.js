function uploadFile() {

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    fetch("/", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(html => {
        document.open();
        document.write(html);
        document.close();

        addLayer(file.name);
    });
}

function addLayer(name) {

    const list = document.getElementById("layerList");

    if (list) {
        const li = document.createElement("li");
        li.textContent = name;
        list.appendChild(li);
    }
}
function exportOBJ() {
    window.open("/export/obj", "_blank");
}

function exportPNG() {
    window.open("/export/png", "_blank");
}