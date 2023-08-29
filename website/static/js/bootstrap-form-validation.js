function initForms() {
    const forms = document.getElementsByClassName("needs-validation");

    for (const form of forms) {
        form.addEventListener("submit", event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.querySelector(":invalid")?.focus();
            }

            form.classList.add("was-validated");
        }, false);
    }
}

/** @param {string|null} size size with K/M/G suffix (KiB/MiB/GiB) */
function sizeToBytes(size) {
    if (!size) return null;
    const suffix = size[size.length - 1];
    let multiplier = 1;
    switch (suffix.toLowerCase()) {
        case 'k':
            multiplier = 1024;
            break;
        case 'm':
            multiplier = 1048576;
            break;
        case 'g':
            multiplier = 1073741824;
            break;
    }
    const bytes = Number.parseFloat(size) * multiplier;
    return bytes == NaN ? null : bytes;
}

/** @param {number} size size in bytes */
function sizeAddUnit(size) {
    const order = Math.floor(Math.log2(size) / 10);
    if (order < 1) return `${size} B`;
    const prefixes = ["", "Ki", "Mi", "Gi", "Ti"];
    return `${(size / Math.pow(2, 10 * order)).toFixed(1)} ${prefixes[order]}B`;
}

function initFileInputValidation() {
    /** @type {NodeListOf<HTMLInputElement>} */
    const fileInputs = document.querySelectorAll("input[type='file'][data-max-files], input[type='file'][data-max-size]");

    for (const input of fileInputs) {
        const maxFiles = Number.parseInt(input.getAttribute("data-max-files"));
        const maxSize = sizeToBytes(input.getAttribute("data-max-size"));
        const preexistingFiles = Number.parseInt(input.getAttribute("data-preexisting-files")) || 0;
        const feedbackFieldId = input.getAttribute("data-feedback");
        const feedbackField = feedbackFieldId ? document.getElementById(feedbackFieldId) : null;
        const validateField = () => {
            const tooManyFiles = maxFiles !== NaN && preexistingFiles + input.files.length > maxFiles;
            /** @type {{name: string; size: number}[]} */
            const tooLargeFiles = [];
            let feedback = document.createDocumentFragment();
            if (maxSize !== null) {
                for (const { size, name } of input.files) {
                    if (size > maxSize) tooLargeFiles.push({ name, size });
                }
            }
            if (tooManyFiles) {
                const validationMessage = `Too many files. (max ${maxFiles}, selected ${input.files.length})${preexistingFiles ? ` including ${preexistingFiles} previously uploaded` : ""}`;
                feedback.appendChild(new Text(validationMessage));
                input.setCustomValidity(validationMessage);
            }
            if (tooLargeFiles.length) {
                const maxSizeUnit = sizeAddUnit(maxSize);
                if (tooManyFiles) {
                    feedback.appendChild(document.createElement("br"));
                } else {
                    input.setCustomValidity(`Too large file selected. (max size ${maxSizeUnit})`);
                }
                feedback.appendChild(new Text(`Maximum file size is ${maxSizeUnit}. Following files are too large:`));
                const list = document.createElement("ul");
                for (const { name, size } of tooLargeFiles) {
                    const element = document.createElement("li");
                    element.textContent = `${name} — ${sizeAddUnit(size)}`;
                    list.appendChild(element);
                }
                feedback.appendChild(list);
            } else if (!tooManyFiles) {
                if (input.required && !input.files.length) {
                    const validationMessage = input.multiple ? "At least one file is required." : "A file is required";
                    input.setCustomValidity(validationMessage);
                    feedback.appendChild(new Text(validationMessage));
                } else {
                    input.setCustomValidity("");
                }
            }
            feedbackField.replaceChildren(feedback);
        }
        input.addEventListener("change", validateField);
        // Firefox preserves input content between reloads and we may not get the "change" event
        validateField();
    }
}

window.addEventListener("DOMContentLoaded", () => {
    initForms();
    initFileInputValidation();
});
