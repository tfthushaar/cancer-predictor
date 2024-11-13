document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[type="number"]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (input.value < 0) {
                    e.preventDefault();
                    isValid = false;
                    showError(input, 'Please enter a positive value');
                } else {
                    removeError(input);
                }
            });
            
            if (!isValid) {
                showAlert('Please correct the errors before submitting.', 'error');
            }
        });
    });

    // Input validation on change
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value < 0) {
                showError(this, 'Please enter a positive value');
            } else {
                removeError(this);
            }
        });
    });
});

function showError(input, message) {
    const formGroup = input.closest('.form-group');
    const existingError = formGroup.querySelector('.error-message');
    
    if (!existingError) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        formGroup.appendChild(errorDiv);
    }
    
    input.classList.add('error');
}

function removeError(input) {
    const formGroup = input.closest('.form-group');
    const errorDiv = formGroup.querySelector('.error-message');
    
    if (errorDiv) {
        errorDiv.remove();
    }
    
    input.classList.remove('error');
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// History page functionality
function toggleDetails(detailsId) {
    const details = document.getElementById(detailsId);
    const allDetails = document.querySelectorAll('.details-panel');
    
    allDetails.forEach(panel => {
        if (panel.id !== detailsId) {
            panel.style.display = 'none';
        }
    });
    
    if (details.style.display === 'none') {
        details.style.display = 'block';
    } else {
        details.style.display = 'none';
    }
}