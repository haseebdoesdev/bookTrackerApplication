// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Progress Form Handling
    const progressForm = document.getElementById('progress-form');
    if (progressForm) {
        const statusSelect = document.getElementById('status');
        const progressContainer = document.getElementById('progress-container');
        
        // Show/hide progress input based on status
        if (statusSelect) {
            statusSelect.addEventListener('change', function() {
                if (this.value === 'reading') {
                    progressContainer.classList.remove('d-none');
                } else if (this.value === 'finished') {
                    progressContainer.classList.remove('d-none');
                    document.getElementById('progress').value = 100;
                } else {
                    progressContainer.classList.add('d-none');
                    document.getElementById('progress').value = 0;
                }
            });
            
            // Trigger on load
            if (statusSelect.value === 'reading' || statusSelect.value === 'finished') {
                progressContainer.classList.remove('d-none');
            } else {
                progressContainer.classList.add('d-none');
            }
        }
    }

    // Handle star rating clicks
    const starContainer = document.getElementById('star-container');
    const ratingInput = document.querySelector('input[name="rating"]');
    
    if (starContainer && ratingInput) {
        const stars = starContainer.querySelectorAll('.star-rating');
        
        // Set initial value if one exists
        if (ratingInput.value) {
            highlightStars(ratingInput.value);
        }
        
        stars.forEach(star => {
            star.addEventListener('click', function() {
                const value = this.getAttribute('data-value');
                ratingInput.value = value;
                highlightStars(value);
            });
            
            star.addEventListener('mouseover', function() {
                const value = this.getAttribute('data-value');
                highlightStarsTemp(value);
            });
            
            star.addEventListener('mouseout', function() {
                resetStars();
                if (ratingInput.value) {
                    highlightStars(ratingInput.value);
                }
            });
        });
    }
    
    function highlightStars(count) {
        const stars = starContainer.querySelectorAll('.star-rating');
        stars.forEach((star, index) => {
            if (index < count) {
                star.classList.remove('far');
                star.classList.add('fas');
            } else {
                star.classList.remove('fas');
                star.classList.add('far');
            }
        });
    }
    
    function highlightStarsTemp(count) {
        const stars = starContainer.querySelectorAll('.star-rating');
        stars.forEach((star, index) => {
            if (index < count) {
                star.classList.remove('far');
                star.classList.add('fas');
            } else {
                star.classList.remove('fas');
                star.classList.add('far');
            }
        });
    }
    
    function resetStars() {
        const stars = starContainer.querySelectorAll('.star-rating');
        stars.forEach(star => {
            star.classList.remove('fas');
            star.classList.add('far');
        });
    }
    
    // Handle progress bars - replace inline styles with CSS classes
    document.querySelectorAll('.progress-bar').forEach(bar => {
        // Get the progress percentage from aria-valuenow or data attribute
        let progressPercent = parseInt(bar.getAttribute('aria-valuenow') || 
                              bar.getAttribute('data-progress') || '0');
        
        // Clear existing inline style
        bar.style.width = '';
        
        // Apply appropriate class based on percentage
        if (progressPercent <= 10) {
            bar.classList.add('progress-width-10');
        } else if (progressPercent <= 20) {
            bar.classList.add('progress-width-20');
        } else if (progressPercent <= 30) {
            bar.classList.add('progress-width-30');
        } else if (progressPercent <= 40) {
            bar.classList.add('progress-width-40');
        } else if (progressPercent <= 50) {
            bar.classList.add('progress-width-50');
        } else if (progressPercent <= 60) {
            bar.classList.add('progress-width-60');
        } else if (progressPercent <= 70) {
            bar.classList.add('progress-width-70');
        } else if (progressPercent <= 80) {
            bar.classList.add('progress-width-80');
        } else if (progressPercent <= 90) {
            bar.classList.add('progress-width-90');
        } else {
            bar.classList.add('progress-width-100');
        }
    });
    
    // Toggle mobile menu collapsed state after clicking a nav link (mobile only)
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }

    // Filter form in library
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        const filterInputs = filterForm.querySelectorAll('select');
        filterInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }
    
    // Bootstrap dismissible alerts auto-close after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = new bootstrap.Alert(alert);
            closeButton.close();
        }, 5000);
    });
}); 