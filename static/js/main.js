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
 * Инициализация мобильного меню
 */
function initMobileMenu() {
    const toggle = document.getElementById('mobileMenuToggle');
    const navList = document.getElementById('navList');

    if (toggle && navList) {
        toggle.addEventListener('click', function() {
            toggle.classList.toggle('active');
            navList.classList.toggle('active');
        });

        // Закрываем меню при клике на ссылку
        navList.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function() {
                toggle.classList.remove('active');
                navList.classList.remove('active');
            });
        });
    }
}

/**
 * Автоскрытие алертов
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
 * Валидация форм
 */
function initForms() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner"></span> Отправка...';
            }
        });
    });

    // Валидация телефона
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
 * Калькулятор стоимости аренды
 */
function initRentalCalculator() {
    const startDate = document.querySelector('input[name="start_date"]');
    const endDate = document.querySelector('input[name="end_date"]');
    const pricePerDay = document.querySelector('[data-price-per-day]');
    const deposit = document.querySelector('[data-deposit]');

    if (startDate && endDate && pricePerDay) {
        const price = parseFloat(pricePerDay.dataset.pricePerDay);
        const depositAmount = deposit ? parseFloat(deposit.dataset.deposit) : 0;

        const calculateTotal = () => {
            const start = new Date(startDate.value);
            const end = new Date(endDate.value);

            if (start && end && end >= start) {
                const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
                const total = days * price;

                // Обновляем отображение
                const daysDisplay = document.getElementById('totalDays');
                const totalDisplay = document.getElementById('totalPrice');
                const depositDisplay = document.getElementById('depositAmount');

                if (daysDisplay) daysDisplay.textContent = days + ' ' + getDaysWord(days);
                if (totalDisplay) totalDisplay.textContent = total.toFixed(2) + ' MDL';
                if (depositDisplay) depositDisplay.textContent = depositAmount.toFixed(2) + ' MDL';
            }
        };

        startDate.addEventListener('change', calculateTotal);
        endDate.addEventListener('change', calculateTotal);

        // Минимальная дата - сегодня
        const today = new Date().toISOString().split('T')[0];
        startDate.setAttribute('min', today);
        endDate.setAttribute('min', today);

        // При изменении даты начала, обновляем минимум для даты окончания
        startDate.addEventListener('change', function() {
            endDate.setAttribute('min', this.value);
            if (endDate.value && endDate.value < this.value) {
                endDate.value = this.value;
            }
        });
    }
}

/**
 * Склонение слова "день"
 */
function getDaysWord(n) {
    const cases = [2, 0, 1, 1, 1, 2];
    const titles = ['день', 'дня', 'дней'];
    return titles[(n % 100 > 4 && n % 100 < 20) ? 2 : cases[Math.min(n % 10, 5)]];
}

/**
 * Галерея изображений
 */
function initGallery() {
    const mainImage = document.querySelector('.tool-gallery-main img');
    const thumbs = document.querySelectorAll('.tool-gallery-thumb');

    if (mainImage && thumbs.length > 0) {
        thumbs.forEach(thumb => {
            thumb.addEventListener('click', function() {
                // Обновляем главное изображение
                mainImage.src = this.querySelector('img').src;

                // Обновляем активный thumb
                thumbs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
}

// Инициализируем галерею если на странице инструмента
if (document.querySelector('.tool-gallery')) {
    initGallery();
}
