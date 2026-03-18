// ---------------- UPLOAD FILE (FIXED PROPERLY) ----------------
function uploadFile() {

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Select a file first");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("/", {
        method: "POST",
        body: formData
    })
    .then(res => res.text())
    .then(html => {

        // Parse HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        // Get new map container
        const newContainer = doc.querySelector(".map-container");

        if (newContainer) {

            const target = document.querySelector(".map-container");

            // Replace HTML
            target.innerHTML = newContainer.innerHTML;

            // 🔥 EXECUTE ALL SCRIPTS (CRITICAL FIX)
            const scripts = target.querySelectorAll("script");

            scripts.forEach(oldScript => {
                const newScript = document.createElement("script");

                if (oldScript.src) {
                    newScript.src = oldScript.src;
                } else {
                    newScript.textContent = oldScript.textContent;
                }

                document.body.appendChild(newScript);
            });
        }

        addLayer(file.name);
    })
    .catch(err => {
        console.error(err);
        alert("Upload failed");
    });
}


// ---------------- ADD LAYER ----------------
function addLayer(name) {

    const list = document.getElementById("layerList");

    if (list) {

        // Remove "No layers loaded"
        if (list.children.length === 1 &&
            list.children[0].textContent === "No layers loaded") {
            list.innerHTML = "";
        }

        // Prevent duplicates
        const exists = Array.from(list.children)
            .some(li => li.textContent === name);

        if (exists) return;

        const li = document.createElement("li");
        li.textContent = name;

        list.appendChild(li);
    }
}


// ---------------- EXPORT ----------------
function exportPNG() {
    window.location.href = "/export/png";
}

function export3D() {
    const format = document.getElementById("format").value;
    window.location.href = "/export/3d/" + format;
}