window.addEventListener("DOMContentLoaded", () => {
    for (const el of document.getElementsByClassName("recaptcha")) {
        let form = el;
        const formId = el.dataset.form;
        if (formId) {
            form = document.getElementById(formId);
        } else if (el.form instanceof HTMLFormElement) {
            form = el.form;
        }
        if (!(form instanceof HTMLFormElement)) continue;

        const sitekey = el.dataset.sitekey;
        const action = el.dataset.action ?? "submit";

        if (!sitekey) {
            console.warn("An element with recaptcha class, but no data-sitekey exists.");
            continue;
        }

        form.addEventListener("submit", (e) => {
            e.preventDefault();
            if (!form.reportValidity() || !grecaptcha) return;

            grecaptcha.ready(() => {
                grecaptcha.execute(sitekey, { action })
                    .then(token => {
                        const responseInput = document.createElement("textarea");
                        responseInput.classList.add("d-none", "g-recaptcha-response");
                        responseInput.value = token;
                        responseInput.name = "g-recaptcha-response";

                        for (const res of form.getElementsByClassName("g-recaptcha-response")) {
                            res.parentNode.removeChild(res);
                        }
                        form.appendChild(responseInput);
                        form.submit();
                    });
            });
        });
    }
});
