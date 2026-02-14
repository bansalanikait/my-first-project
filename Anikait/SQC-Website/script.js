function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({
        behavior: "smooth"
    });
}

/* Boot loader */
window.addEventListener("load", () => {
    setTimeout(() => {
        document.getElementById("loader").style.display = "none";
    }, 3000);
});

/* Neon flicker logo */
setInterval(() => {
    const logo = document.querySelector(".logo");
    if (logo) {
        logo.style.opacity = Math.random() > 0.1 ? "1" : "0.5";
    }
}, 150);


