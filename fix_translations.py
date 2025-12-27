#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для правильной локализации через Django i18n.
Возвращает русский текст в HTML файлы и оборачивает в {% trans %} теги.
"""

import os
import re

# Словарь: румынский текст → русский текст (для обратной замены)
REVERSE_TRANSLATIONS = {
    # Meta и ключевые слова
    'O gamă largă de instrumente de construcție de închiriat la prețuri accesibile.': 'Широкий выбор строительных инструментов в аренду по доступным ценам.',
    'închiriere instrumente, instrumente de construcție, închiriere unelte, Moldova, Chișinău': 'аренда инструментов, строительные инструменты, прокат инструментов, Молдова, Кишинёв',

    # Комментарии
    'Culorile principale ale brandului (din logo)': 'Основные цвета бренда (из логотипа)',
    'Tema întunecată': 'Тёмная тема',
    'Pentru compatibilitate inversă': 'Для обратной совместимости',
    'Legacy CSS (pentru compatibilitate cu alte pagini)': 'Legacy CSS (для совместимости с другими страницами)',

    # Навигация
    'Acasă': 'Главная',
    'Catalog': 'Каталог',
    'Despre noi': 'О нас',
    'Contacte': 'Контакты',
    'Favorite': 'Избранное',
    'Panou de control': 'Панель управления',
    'Autentificare': 'Войти',

    # Личный кабинет
    'Cont personal': 'Личный кабинет',
    'Bun venit': 'Добро пожаловать',
    'Total cereri': 'Всего заявок',
    'Active': 'Активных',
    'Finalizate': 'Завершённых',
    'Ultimele cereri': 'Последние заявки',
    'Număr': 'Номер',
    'Perioadă': 'Период',
    'Status': 'Статус',
    'Nu aveți încă cereri': 'У вас пока нет заявок',
    'Alegeți o unealtă și faceți prima închiriere': 'Выберите инструмент и оформите первую аренду',
    'Mergi la catalog': 'Перейти в каталог',

    # Формы и действия
    'Procesare închiriere': 'Оформление аренды',
    'Numele dumneavoastră': 'Ваше имя',
    'Telefon': 'Телефон',
    'Data de început': 'Дата начала',
    'Data de sfârșit': 'Дата окончания',
    'Comentariu': 'Комментарий',
    'Număr de zile': 'Количество дней',
    'Depozit': 'Залог',
    'Total de plată': 'Итого к оплате',
    'Închiriere': 'Арендовать',
    'Trimite cererea': 'Отправить заявку',
    'Ion Popescu': 'Иван Иванов',
    'Dorințe suplimentare...': 'Дополнительные пожелания...',
    'Trimițând cererea, sunteți de acord cu condițiile de închiriere': 'Отправляя заявку, вы соглашаетесь с условиями аренды',

    # Страница успеха
    'Cererea a fost trimisă': 'Заявка отправлена',
    'Cererea dumneavoastră': 'Ваша заявка',
    'a fost creată cu succes.': 'успешно создана.',
    'Vă vom contacta în curând pentru confirmare.': 'Мы свяжемся с вами в ближайшее время для подтверждения.',
    'Unealtă': 'Инструмент',
    'Perioada de închiriere': 'Период аренды',
    'Sumă': 'Сумма',
    'Continuați selecția': 'Продолжить выбор',
    'Cererile mele': 'Мои заявки',
    'Dacă aveți întrebări, sunați:': 'Если у вас есть вопросы, звоните:',

    # Админ панель
    'Statistici și analiză MoldTool': 'Статистика и аналитика MoldTool',
    'Unelte': 'Инструменты',
    'disponibil': 'доступно',
    'Utilizatori': 'Пользователи',
    'pe săptămână': 'за неделю',
    'Recenzii': 'Отзывы',
    'în moderare': 'на модерации',
    'În favorite': 'В избранном',
    'Rating mediu:': 'Ср. рейтинг:',
    'Instrumente populare': 'Популярные инструменты',
    'vizualizări': 'просмотров',
    'Nu există date': 'Нет данных',
    'Adăugate mai des la favorite': 'Чаще добавляют в избранное',
    'în favorite': 'в избранном',
    'Ultimele recenzii': 'Последние отзывы',
    'În moderare': 'На модерации',
    'Nu există recenzii': 'Нет отзывов',
    'Categorii': 'Категории',
    'instrumente': 'инструментов',
    'Nu există categorii': 'Нет категорий',
    'Total categorii:': 'Всего категорий:',
    'Acțiuni rapide': 'Быстрые действия',
    'Adaugă unealtă': 'Добавить инструмент',
    'Gestionare categorii': 'Управление категориями',
    'Moderare recenzii': 'Модерация отзывов',

    # Детали инструмента
    'recenzii': 'отзывов',
    'Calculator de închiriere': 'Калькулятор аренды',
    'Număr de zile:': 'Количество дней:',
    'Cost închiriere:': 'Стоимость аренды:',
    'Depozit:': 'Залог:',
    'Disponibil pentru închiriere': 'Доступен для аренды',
    'Acum în închiriere': 'Сейчас в аренде',
    'Indisponibil': 'Недоступен',
    'Caracteristici': 'Характеристики',
    'Descriere': 'Описание',
    'Lăsați o recenzie': 'Оставить отзыв',
    'Evaluarea dumneavoastră': 'Ваша оценка',
    'Recenzia dumneavoastră (opțional)': 'Ваш отзыв (необязательно)',
    'Autentificați-vă pentru a lăsa o recenzie': 'Войдите, чтобы оставить отзыв',
    'Autentificați-vă pentru a adăuga la favorite': 'Войдите, чтобы добавить в избранное',
    'Vă rugăm să selectați o evaluare': 'Пожалуйста, выберите оценку',
    'Eroare la trimiterea recenziei': 'Ошибка при отправке отзыва',
    'Încă nu există recenzii. Fiți primul!': 'Пока нет отзывов. Будьте первым!',
    'Instrumente similare': 'Похожие инструменты',
    'Toate în categorie': 'Все в категории',
    ' / zi': ' / день',
    'Hit': 'Хит',
    'Trimite recenzia': 'Отправить отзыв',
    'Împărtășiți experiența dumneavoastră cu această unealtă...': 'Поделитесь вашим опытом использования этого инструмента...',

    # Каталог
    'Catalog de instrumente': 'Каталог инструментов',
    'Găsiți instrumentul potrivit pentru proiectul dumneavoastră': 'Найдите подходящий инструмент для вашего проекта',
    'Căutare instrumente...': 'Поиск инструментов...',
    'Toate categoriile': 'Все категории',
    'Noi': 'Новые',
    'Mai întâi cele ieftine': 'Сначала дешевле',
    'Mai întâi cele scumpe': 'Сначала дороже',
    'După nume': 'По названию',
    'Căutare': 'Найти',
    'Preț (MDL/zi):': 'Цена (MDL/день):',
    'Aplicare': 'Применить',
    'Resetare': 'Сбросить',
    'Găsite:': 'Найдено:',
    'Mai multe detalii': 'Подробнее',
    'MDL/zi': 'MDL/день',
    'Disponibil': 'Доступен',
    'În închiriere': 'В аренде',
    'Instrumentele nu au fost găsite': 'Инструменты не найдены',
    'Încercați să schimbați parametrii de căutare sau resetați filtrele': 'Попробуйте изменить параметры поиска или сбросьте фильтры',
    'Resetare filtre': 'Сбросить фильтры',

    # Категории
    'În această categorie nu există încă instrumente': 'В этой категории пока нет инструментов',
    'În curând vor apărea noi articole': 'Скоро здесь появятся новые позиции',
    'Înapoi la catalog': 'Вернуться в каталог',

    # FAQ
    'Întrebări frecvente': 'Частые вопросы',

    # Избранное
    'Total:': 'Всего:',
}

def wrap_in_trans(text):
    """Обернуть текст в {% trans %} тег"""
    # Экранируем кавычки внутри текста
    escaped_text = text.replace('"', '\\"')
    return f'{{% trans "{escaped_text}" %}}'

def fix_file(file_path):
    """Исправить один файл"""
    print(f"Обработка: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes = []

        # Заменяем румынский текст обратно на русский с {% trans %}
        for romanian, russian in REVERSE_TRANSLATIONS.items():
            if romanian in content:
                # Проверяем, не обернут ли уже в {% trans %}
                if f'{{% trans "{romanian}" %}}' not in content and f"{{% trans '{romanian}' %}}" not in content:
                    # Заменяем на русский с {% trans %}
                    trans_wrapped = wrap_in_trans(russian)
                    content = content.replace(romanian, trans_wrapped)
                    changes.append(f"  ✓ {romanian} → {trans_wrapped}")

        if content != original_content:
            # Проверяем, загружен ли i18n
            if '{% load i18n %}' not in content and '{% load static i18n %}' not in content:
                # Добавляем загрузку i18n после первой строки {% load ... %}
                content = re.sub(
                    r'({% load[^%]*%})',
                    r'\1\n{% load i18n %}',
                    content,
                    count=1
                )
                changes.append("  ✓ Добавлен {% load i18n %}")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  ✅ Изменений: {len(changes)}")
            for change in changes:
                print(change)
            print()
            return len(changes)
        else:
            print("  ℹ️  Изменений не требуется\n")
            return 0

    except Exception as e:
        print(f"  ❌ Ошибка: {e}\n")
        return 0

def main():
    """Основная функция"""
    print("=" * 80)
    print("ИСПРАВЛЕНИЕ ПЕРЕВОДОВ: переход на Django i18n систему")
    print("=" * 80)
    print()

    html_files = [
        'templates/base.html',
        'templates/includes/header.html',
        'templates/includes/footer.html',
        'templates/core/admin_dashboard.html',
        'templates/rentals/create_request.html',
        'templates/rentals/request_success.html',
        'templates/dashboard/index.html',
        'templates/catalog/catalog.html',
        'templates/catalog/category.html',
        'templates/catalog/favorites.html',
        'templates/catalog/faq.html',
        'templates/catalog/tool_detail.html',
    ]

    total_changes = 0
    processed = 0

    for html_file in html_files:
        if os.path.exists(html_file):
            changes = fix_file(html_file)
            total_changes += changes
            if changes > 0:
                processed += 1
        else:
            print(f"⚠️  Файл не найден: {html_file}\n")

    print("=" * 80)
    print(f"✅ ГОТОВО!")
    print(f"Обработано файлов: {processed}")
    print(f"Всего изменений: {total_changes}")
    print()
    print("Следующие шаги:")
    print("1. python manage.py makemessages -l ro")
    print("2. Отредактировать locale/ro/LC_MESSAGES/django.po")
    print("3. python manage.py compilemessages")
    print("=" * 80)

if __name__ == '__main__':
    main()
