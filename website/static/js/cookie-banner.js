const BANNER_CLOSED_COOKIE = "cookie_closed";

function cookieBannerClosed() {
    return document.cookie
        .split(";")
        .map(c => c.split("="))
        .some(([k, v]) => k.trim() === BANNER_CLOSED_COOKIE && v.trim());
}

window.addEventListener("DOMContentLoaded", () => {
    const banner = document.getElementById("cookieBanner");
    const btnOptIn = document.getElementById("btnOptIn");
    const btnOptOut = document.getElementById("btnOptOut");

    function closeBanner() {
        document.cookie = BANNER_CLOSED_COOKIE + "=1";
        banner.classList.add("d-none");
    }

    btnOptIn.addEventListener("click", () => {
        _paq?.push(["forgetUserOptOut"]);
        closeBanner();
    });
    btnOptOut.addEventListener("click", () => {
        _paq?.push(["optUserOut"]);
        closeBanner();
    })

    _paq?.push([function () {
        if (!this.isUserOptedOut() && !cookieBannerClosed()) {
            banner.classList.remove("d-none");
        }
    }]);
});
