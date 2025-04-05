function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.demo-container').forEach(container => {
        container.style.display = 'none';
    });

    // Show the selected page
    document.getElementById(pageId).style.display = 'block';

    // Update active state in navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-page') === pageId || 
            (link.getAttribute('onclick') && link.getAttribute('onclick').includes(`showPage('${pageId}')`))) {
            link.classList.add('active');
        }
    });

    // Scroll to top
    window.scrollTo(0, 0);
}

// Add event listeners to navigation links
document.addEventListener('DOMContentLoaded', function() {
    // Navigation link event listeners
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            // Only prevent default if using data-page attribute
            if (this.getAttribute('data-page')) {
                e.preventDefault();
                const pageId = this.getAttribute('data-page');
                showPage(pageId);
            }
            // For links with onclick attribute, the onclick handler will take care of it
        });
    });

    // Handle all buttons with onclick that calls showPage
    document.querySelectorAll('button[onclick], a[onclick]').forEach(element => {
        const onclickAttr = element.getAttribute('onclick');
        if (onclickAttr && onclickAttr.includes('showPage(')) {
            element.addEventListener('click', function(e) {
                // The onclick attribute already has the functionality
                // This is just to ensure we're using the same event handling approach
            });
        }
    });

    // Form validation for contact and listing forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Simple form validation
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (isValid) {
                // Simulate form submission
                const submitBtn = form.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
                
                // Simulate API call
                setTimeout(() => {
                    submitBtn.innerHTML = '<i class="bi bi-check-circle"></i> Success!';
                    form.reset();
                    
                    // Reset button after 2 seconds
                    setTimeout(() => {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalText;
                    }, 2000);
                }, 1500);
            }
        });
    });

    // Toggle price field when "free item" is checked
    const freeItemCheckbox = document.getElementById('freeItem');
    if (freeItemCheckbox) {
        freeItemCheckbox.addEventListener('change', function() {
            const priceInput = document.querySelector('input[name="price"]');
            if (priceInput) {
                if (this.checked) {
                    priceInput.value = '0';
                    priceInput.disabled = true;
                } else {
                    priceInput.value = '';
                    priceInput.disabled = false;
                }
            }
        });
    }

    // Filter functionality for marketplace
    const filterForm = document.querySelector('#marketplace form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Simulate filter application
            const submitBtn = filterForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Filtering...';
            
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
                // You could add code here to actually filter the listings
            }, 1000);
        });
    }

    // Show home page by default
    showPage('home');
});