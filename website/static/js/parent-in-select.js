/** @param {HTMLOptionElement} element */
function getPrefix(element) {
    const parent = element.parentElement;
    if (!(parent instanceof HTMLOptGroupElement)) return "";
    return parent.label + " - ";
}

window.addEventListener("DOMContentLoaded", () => {
    const catSelect = document.getElementById("category");
    if (!(catSelect instanceof HTMLSelectElement)) return;

    function changeCurrentLabel() {
        /** @type {HTMLSelectElement} */
        const select = catSelect;

        for (const opt of select.querySelectorAll("[data-prefixed=true]")) {
            if (opt instanceof HTMLOptionElement) {
                const prefix = getPrefix(opt);
                if (opt.label.startsWith(prefix)) opt.label = opt.label.substring(prefix.length);
                opt.removeAttribute("data-prefixed");
            }
        }

        for (const opt of select.selectedOptions) {
            if (opt.dataset.prefixed === "true") continue;
            const prefix = getPrefix(opt);
            opt.label = prefix + opt.label;
            opt.dataset.prefixed = "true";
        }
    }

    catSelect.addEventListener("change", changeCurrentLabel);
    changeCurrentLabel();
});
