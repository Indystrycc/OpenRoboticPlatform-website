/*!
* Start Bootstrap - Agency v7.0.12 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
//

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    //  Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    const form = document.getElementById("newsletter_form");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const data = new FormData(form); 
        try {
            const response = await fetch("/newsletterAdd", {method: "POST", body: data, credentials: "same-origin"});
            const { success } = await response.json()
            if (success){
                addBootstrapAlert("alert-success", "Congratulations! You're now subscribed to our newsletter.")
            }else{
                addBootstrapAlert("alert-danger", "Something went wrong while adding your email to our newsletter, please try again.")
            }
        } catch (e) {
            addBootstrapAlert("alert-danger", "There was an error, please try again.")
            console.log(e)
        }
    });
    
    // Add reply button functionality
    document.querySelectorAll('.reply-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const form = btn.nextElementSibling;
            form.classList.toggle('d-none');
        });
    });
});

function addBootstrapAlert(type, message) {
    const alertDiv = document.createElement("div");
    alertDiv.classList.add("alert", type , "alert-dismissible", "fade", "show", "fixed-bottom", "col-11", "m-auto", "mb-2");
    alertDiv.setAttribute("role", "alert");
    alertDiv.textContent = message;

    const closeButton = document.createElement("button");
    closeButton.setAttribute("type", "button");
    closeButton.classList.add("btn-close");
    closeButton.setAttribute("data-bs-dismiss", "alert");
    closeButton.setAttribute("aria-label", "Close");

    alertDiv.appendChild(closeButton);
    document.body.appendChild(alertDiv);
}