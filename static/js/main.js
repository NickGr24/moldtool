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
    const startDateInput = document.getElementById('id_start_date');
    const endDateInput = document.getElementById('id_end_date');
    const summaryEl = document.querySelector('.rental-summary');

    if (!startDateInput || !endDateInput || !summaryEl) {
        return;
    }

    // Получаем цену и залог из data-атрибутов
    const pricePerDay = parseFloat(summaryEl.dataset.pricePerDay.replace(',', '.')) || 0;
    const depositAmount = parseFloat(summaryEl.dataset.deposit.replace(',', '.')) || 0;

    const daysDisplay = document.getElementById('totalDays');
    const totalDisplay = document.getElementById('totalPrice');

    const calculateTotal = () => {
        const startValue = startDateInput.value;
        const endValue = endDateInput.value;

        // Проверяем что обе даты выбраны
        if (!startValue || !endValue) {
            if (daysDisplay) daysDisplay.textContent = '-';
            if (totalDisplay) totalDisplay.textContent = '-';
            return;
        }

        const start = new Date(startValue);
        const end = new Date(endValue);

        // Проверяем валидность дат
        if (isNaN(start.getTime()) || isNaN(end.getTime())) {
            if (daysDisplay) daysDisplay.textContent = '-';
            if (totalDisplay) totalDisplay.textContent = '-';
            return;
        }

        // Проверяем что конец не раньше начала
        if (end < start) {
            if (daysDisplay) daysDisplay.textContent = 'Ошибка';
            if (totalDisplay) totalDisplay.textContent = '-';
            return;
        }

        // Рассчитываем количество дней (включительно)
        const timeDiff = end.getTime() - start.getTime();
        const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24)) + 1;
        const total = days * pricePerDay;

        // Обновляем отображение
        if (daysDisplay) {
            daysDisplay.textContent = days + ' ' + getDaysWord(days);
        }
        if (totalDisplay) {
            totalDisplay.textContent = total.toFixed(2) + ' MDL';
        }
    };

    // Слушаем изменения дат
    startDateInput.addEventListener('change', calculateTotal);
    endDateInput.addEventListener('change', calculateTotal);
    startDateInput.addEventListener('input', calculateTotal);
    endDateInput.addEventListener('input', calculateTotal);

    // Минимальная дата - сегодня
    const today = new Date().toISOString().split('T')[0];
    startDateInput.setAttribute('min', today);
    endDateInput.setAttribute('min', today);

    // При изменении даты начала, обновляем минимум для даты окончания
    startDateInput.addEventListener('change', function() {
        if (this.value) {
            endDateInput.setAttribute('min', this.value);
            if (endDateInput.value && endDateInput.value < this.value) {
                endDateInput.value = this.value;
            }
            calculateTotal();
        }
    });

    // Начальный расчёт если даты уже заполнены
    calculateTotal();
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
