window.onSubmitCaptcha = () => {
    const captchaBtn = document.querySelector(".g-recaptcha[data-callback=onSubmitCaptcha]");
    if (!(captchaBtn instanceof HTMLElement)) return;
    const form = document.getElementById(captchaBtn.dataset.form);
    if (form instanceof HTMLFormElement) form.submit();
}
