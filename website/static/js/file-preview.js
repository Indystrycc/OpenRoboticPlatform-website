/** @param {Event} event  */
function displayPreview(event) {
    const fileInput = event.target;
    const filePreview = document.getElementById("file-preview");
    if (!(fileInput instanceof HTMLInputElement && fileInput.files && filePreview)) return;

    const fragment = document.createDocumentFragment();
    for (const file of fileInput.files) {
        const fileItem = document.createElement("div");

        const fileIcon = document.createElement("i");
        fileIcon.classList.add("fa-solid", "fa-file", "me-2");

        const fileName = document.createElement("span");
        fileName.textContent = file.name;

        fileItem.appendChild(fileIcon);
        fileItem.appendChild(fileName);
        fragment.appendChild(fileItem);
    }

    filePreview.replaceChildren(fragment);
}

window.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("filesInput");
    if (fileInput instanceof HTMLInputElement) {
        fileInput.addEventListener("change", displayPreview);
        if (fileInput.files?.length) fileInput.dispatchEvent(new Event("change"));
    }
});
