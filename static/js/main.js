/**
 * MoldTool - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    initMobileMenu();

    // Auto-hide alerts
    initAlerts();

    // Form validation
    initForms();

    // Rental price calculator
    initRentalCalculator();
});

/**
 * Inițializarea meniului mobil
 */
function initMobileMenu() {
    const toggle = document.getElementById('mobileMenuToggle');
    const navList = document.getElementById('navList');

    if (toggle && navList) {
        toggle.addEventListener('click', function() {
            toggle.classList.toggle('active');
            navList.classList.toggle('active');
        });

        // Închidem meniul la click pe link
        navList.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function() {
                toggle.classList.remove('active');
                navList.classList.remove('active');
            });
        });
    }
}

/**
 * Ascundere automată a alertelor
 */
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';

            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
}

/**
 * Validare formulare
 */
function initForms() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');

            if (submitBtn) {
                submitBtn.disabled = true;
                const label = (window.i18n && window.i18n.submitting) || 'Submitting…';
                submitBtn.innerHTML = '<span class="spinner"></span> ' + label;
            }
        });
    });

    // Validare telefon
    const phoneInputs = document.querySelectorAll('input[name="customer_phone"], input[name="phone"]');

    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.length > 0) {
                if (!value.startsWith('373')) {
                    value = '373' + value;
                }
                value = '+' + value;
            }

            e.target.value = value.slice(0, 12);
        });
    });
}

/**
 * Calculator cost închiriere
 */
function initRentalCalculator() {
    const startDateInput = document.getElementById('id_start_date');
    const endDateInput = document.getElementById('id_end_date');
    const summaryEl = document.querySelector('.rental-summary');

    if (!startDateInput || !endDateInput || !summaryEl) {
        return;
    }

    const priceStr = summaryEl.dataset.pricePerDay || '0';
    const pricePerDay = parseFloat(priceStr.toString().replace(',', '.')) || 0;

    const daysDisplay = document.getElementById('totalDays');
    const totalDisplay = document.getElementById('totalPrice');

    const calculateTotal = () => {
        const startValue = startDateInput.value;
        const endValue = endDateInput.value;

        console.log('Calculate:', { startValue, endValue, pricePerDay });

        // Verificăm că ambele date sunt selectate
        if (!startValue || !endValue) {
            if (daysDisplay) daysDisplay.textContent = '-';
            if (totalDisplay) totalDisplay.textContent = '-';
            return;
        }

        const start = new Date(startValue);
        const end = new Date(endValue);

        // Verificăm validitatea datelor
        if (isNaN(start.getTime()) || isNaN(end.getTime())) {
            if (daysDisplay) daysDisplay.textContent = '-';
            if (totalDisplay) totalDisplay.textContent = '-';
            return;
        }

        // Verificăm că sfârșitul nu este înaintea începutului
        if (end < start) {
            if (daysDisplay) daysDisplay.textContent = 'Eroare';
            if (totalDisplay) totalDisplay.textContent = '-';
            return;
        }

        // Calculăm numărul de zile (inclusiv)
        const timeDiff = end.getTime() - start.getTime();
        const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24)) + 1;
        const total = days * pricePerDay;

        console.log('Result:', { days, total });

        // Actualizăm afișarea
        if (daysDisplay) {
            daysDisplay.textContent = days + ' ' + getDaysWord(days);
        }
        if (totalDisplay) {
            totalDisplay.textContent = total.toFixed(2) + ' MDL';
        }
    };

    // Ascultăm modificările datelor
    startDateInput.addEventListener('change', calculateTotal);
    endDateInput.addEventListener('change', calculateTotal);
    startDateInput.addEventListener('input', calculateTotal);
    endDateInput.addEventListener('input', calculateTotal);

    // Data minimă - astăzi
    const today = new Date().toISOString().split('T')[0];
    startDateInput.setAttribute('min', today);
    endDateInput.setAttribute('min', today);

    // La modificarea datei de început, actualizăm minimul pentru data de sfârșit
    startDateInput.addEventListener('change', function() {
        if (this.value) {
            endDateInput.setAttribute('min', this.value);
            if (endDateInput.value && endDateInput.value < this.value) {
                endDateInput.value = this.value;
            }
            calculateTotal();
        }
    });

    // Calculul inițial dacă datele sunt deja completate
    calculateTotal();
}

/**
 * Forma de plural pentru cuvântul "zi"
 */
function getDaysWord(n) {
    return n === 1 ? 'zi' : 'zile';
}

/**
 * Galerie de imagini
 */
function initGallery() {
    const mainImage = document.querySelector('.tool-gallery-main img');
    const thumbs = document.querySelectorAll('.tool-gallery-thumb');

    if (mainImage && thumbs.length > 0) {
        thumbs.forEach(thumb => {
            thumb.addEventListener('click', function() {
                // Actualizăm imaginea principală
                mainImage.src = this.querySelector('img').src;

                // Actualizăm thumb-ul activ
                thumbs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
}

// Inițializăm galeria dacă suntem pe pagina uneltei
if (document.querySelector('.tool-gallery')) {
    initGallery();
}
