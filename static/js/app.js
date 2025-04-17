// Main JavaScript file for the application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Initialize datepickers if any
    const datepickers = document.querySelectorAll('.datepicker');
    if (datepickers.length > 0) {
        datepickers.forEach(function(elem) {
            // This is just a placeholder - in a real app, we'd initialize a date picker library
            // For example: new Datepicker(elem, { /* options */ });
            elem.addEventListener('focus', function() {
                this.type = 'date';
            });
            elem.addEventListener('blur', function() {
                if (!this.value) {
                    this.type = 'text';
                }
            });
        });
    }
    
    // Handle image preview for file uploads
    const imageInputs = document.querySelectorAll('.image-upload');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                const preview = document.querySelector(input.dataset.preview);
                
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                
                reader.readAsDataURL(file);
            }
        });
    });
    
    // Handle confirmation dialogs
    const confirmForms = document.querySelectorAll('form[data-confirm]');
    confirmForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm(form.dataset.confirm)) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Handle filter forms that should auto-submit on change
    const autoSubmitSelects = document.querySelectorAll('select[data-auto-submit]');
    autoSubmitSelects.forEach(function(select) {
        select.addEventListener('change', function() {
            this.closest('form').submit();
        });
    });
});
