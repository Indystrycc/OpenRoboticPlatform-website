/** @param {Event} event  */
function displayPreview(event) {
    const fileInput = event.target;
    if (!(fileInput instanceof HTMLInputElement)) return;

    const file = fileInput.files?.item(0);
    if (!file) return;

    const reader = new FileReader();
    reader.addEventListener("load", (loadEvent) => {
        const imagePreview = document.getElementById("image-preview");
        const imageElement = document.createElement("img");
        imageElement.src = loadEvent.target.result;
        imageElement.classList.add("uploaded-image");

        imagePreview.replaceChildren(imageElement);
    });
    reader.readAsDataURL(file);
}

window.addEventListener("DOMContentLoaded", () => {
    const imageInput = document.getElementById("image");
    if (imageInput instanceof HTMLInputElement) {
        imageInput.addEventListener("change", displayPreview);
        if (imageInput.files?.length) imageInput.dispatchEvent(new Event("change"));
    }
});
