// script.js

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);

        // Implement additional JavaScript logic if needed before submitting the form
        // For example, you can show a loading spinner or disable the submit button

        // Simulate form submission (replace this with your actual AJAX request)
        setTimeout(function() {
            form.submit();
        }, 1000);
    });
});
