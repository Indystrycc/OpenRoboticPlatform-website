/**
 * @param {HTMLElement} fileElem
 * @param {(() => void) | null} revalidate
 */
function markDeleted(fileElem, revalidate) {
    const nameElem = fileElem.getElementsByClassName("existing-file-name")[0];
    const name = nameElem.textContent;
    // Add to removed files
    const removedFileInput = document.createElement("input");
    removedFileInput.name = "removedFiles";
    removedFileInput.value = name;
    removedFileInput.setAttribute("data-file-name", name);
    const removedFilesElem = document.getElementById("filesToRemove");
    removedFilesElem.appendChild(removedFileInput);
    fileElem.removeAttribute("data-file-not-deleted");
    // Show as deleted and change action icon
    nameElem.classList.add("text-decoration-line-through", "text-body-secondary");
    const btnText = document.createTextNode("Restore ");
    const restoreIcon = document.createElement("i");
    restoreIcon.classList.add("fa-solid", "fa-reply");
    const actionBtn = fileElem.getElementsByClassName("existing-file-action-btn")[0];
    actionBtn.replaceChildren(btnText, restoreIcon);
    actionBtn.classList.remove("btn-danger");
    actionBtn.classList.add("btn-success");
    // Allow restoring
    actionBtn.addEventListener("click", () => restore(fileElem, revalidate), { once: true });
    revalidate && revalidate();
}
/**
 * @param {HTMLElement} fileElem
 * @param {(() => void) | null} revalidate
 */
function restore(fileElem, revalidate) {
    const nameElem = fileElem.getElementsByClassName("existing-file-name")[0];
    const name = nameElem.textContent;
    // Remove from removed files
    const removedFilesElem = document.getElementById("filesToRemove");
    const removedFileInput = [...removedFilesElem.querySelectorAll(`[data-file-name]`)].find(e => e.getAttribute("data-file-name") === name);
    removedFilesElem.removeChild(removedFileInput);
    fileElem.setAttribute("data-file-not-deleted", "");
    // Show as a normal file and change action icon
    nameElem.classList.remove("text-decoration-line-through", "text-body-secondary");
    const btnText = document.createTextNode("Delete ");
    const restoreIcon = document.createElement("i");
    restoreIcon.classList.add("fa-solid", "fa-trash-can");
    const actionBtn = fileElem.getElementsByClassName("existing-file-action-btn")[0];
    actionBtn.replaceChildren(btnText, restoreIcon);
    actionBtn.classList.remove("btn-success");
    actionBtn.classList.add("btn-danger");
    // Allow deleting
    actionBtn.addEventListener("click", () => markDeleted(fileElem, revalidate), { once: true });
    revalidate && revalidate();
}

document.addEventListener("DOMContentLoaded", () => {
    const existingFiles = document.querySelectorAll("[data-existing-file]");
    for (const fileContainer of existingFiles) {
        const actionBtn = fileContainer.getElementsByClassName("existing-file-action-btn")[0];
        let parent = fileContainer;
        /** @type {(() => void) | null} */
        let revalidateInput = null;
        while (parent = parent.closest("[id]")) {
            /** @type {HTMLInputElement | null} */
            const connectedInput = document.querySelector(`input[data-preexisting-files="${parent.id}"]`);
            if (connectedInput) {
                revalidateInput = () => {
                    const e = new Event("existingFileChange");
                    connectedInput.dispatchEvent(e);
                };
                break;
            }
        }
        actionBtn.addEventListener("click", () => markDeleted(fileContainer, revalidateInput), { once: true });
    }
});
