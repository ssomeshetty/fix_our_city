// You can add any custom JavaScript here for interactivity, such as smooth scrolling or animations.
// Example: Smooth Scroll for anchors

// base.js

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});