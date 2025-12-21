#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для перевода всего русского текста в HTML файлах на румынский язык.
Использует тот же стиль, что и существующие переводы в locale/ro/LC_MESSAGES/django.po
"""

import os
import re

# Словарь переводов русский -> румынский (на основе существующих переводов)
TRANSLATIONS = {
    # Meta tags и keywords
    'Широкий выбор строительных инструментов в аренду по доступным ценам.': 'O gamă largă de instrumente de construcție de închiriat la prețuri accesibile.',
    'аренда инструментов, строительные инструменты, прокат инструментов, Молдова, Кишинёв': 'închiriere instrumente, instrumente de construcție, închiriere unelte, Moldova, Chișinău',

    # Комментарии (оставляем как есть или переводим)
    'Основные цвета бренда (из логотипа)': 'Culorile principale ale brandului (din logo)',
    'Тёмная тема': 'Tema întunecată',
    'Для обратной совместимости': 'Pentru compatibilitate inversă',
    'Legacy CSS (для совместимости с другими страницами)': 'Legacy CSS (pentru compatibilitate cu alte pagini)',

    # Часто используемые фразы
    'Главная': 'Acasă',
    'Каталог': 'Catalog',
    'О нас': 'Despre noi',
    'Контакты': 'Contacte',
    'Избранное': 'Favorite',
    'Панель управления': 'Panou de control',
    'Войти': 'Autentificare',

    # Страница создания заявки
    'Оформление аренды': 'Procesare închiriere',
    'Ваше имя': 'Numele dumneavoastră',
    'Телефон': 'Telefon',
    'Дата начала': 'Data de început',
    'Дата окончания': 'Data de sfârșit',
    'Комментарий': 'Comentariu',
    'Количество дней': 'Număr de zile',
    'Залог': 'Depozit',
    'Итого к оплате': 'Total de plată',

    # Страница успеха
    'Заявка отправлена': 'Cererea a fost trimisă',
    'Заявка отправлена!': 'Cererea a fost trimisă!',
    'Ваша заявка': 'Cererea dumneavoastră',
    'успешно создана.': 'a fost creată cu succes.',
    'Мы свяжемся с вами в ближайшее время для подтверждения.': 'Vă vom contacta în curând pentru confirmare.',
    'Инструмент': 'Unealtă',
    'Период аренды': 'Perioada de închiriere',
    'Сумма': 'Sumă',
    'Продолжить выбор': 'Continuați selecția',
    'Мои заявки': 'Cererile mele',
    'Если у вас есть вопросы, звоните:': 'Dacă aveți întrebări, sunați:',

    # Админ панель
    'Статистика и аналитика MoldTool': 'Statistici și analiză MoldTool',
    'Инструменты': 'Unelte',
    'доступно': 'disponibil',
    'Пользователи': 'Utilizatori',
    'за неделю': 'pe săptămână',
    'Отзывы': 'Recenzii',
    'на модерации': 'în moderare',
    'В избранном': 'În favorite',
    'Ср. рейтинг:': 'Rating mediu:',
    'Популярные инструменты': 'Instrumente populare',
    'просмотров': 'vizualizări',
    'Нет данных': 'Nu există date',
    'Чаще добавляют в избранное': 'Adăugate mai des la favorite',
    'в избранном': 'în favorite',
    'Последние отзывы': 'Ultimele recenzii',
    'На модерации': 'În moderare',
    'Нет отзывов': 'Nu există recenzii',
    'Категории': 'Categorii',
    'инструментов': 'instrumente',
    'Нет категорий': 'Nu există categorii',
    'Всего категорий:': 'Total categorii:',
    'Быстрые действия': 'Acțiuni rapide',
    'Добавить инструмент': 'Adaugă unealtă',
    'Управление категориями': 'Gestionare categorii',
    'Модерация отзывов': 'Moderare recenzii',

    # Деталь инструмента
    'отзывов': 'recenzii',
    'Калькулятор аренды': 'Calculator de închiriere',
    'Количество дней:': 'Număr de zile:',
    'Стоимость аренды:': 'Cost închiriere:',
    'Залог:': 'Depozit:',
    'Доступен для аренды': 'Disponibil pentru închiriere',
    'Сейчас в аренде': 'Acum în închiriere',
    'Недоступен': 'Indisponibil',
    'Характеристики': 'Caracteristici',
    'Описание': 'Descriere',
    'Оставить отзыв': 'Lăsați o recenzie',
    'Ваша оценка': 'Evaluarea dumneavoastră',
    'Ваш отзыв (необязательно)': 'Recenzia dumneavoastră (opțional)',
    'Войдите, чтобы оставить отзыв': 'Autentificați-vă pentru a lăsa o recenzie',
    'Войдите, чтобы добавить в избранное': 'Autentificați-vă pentru a adăuga la favorite',
    'Пожалуйста, выберите оценку': 'Vă rugăm să selectați o evaluare',
    'Ошибка при отправке отзыва': 'Eroare la trimiterea recenziei',
    'Пока нет отзывов. Будьте первым!': 'Încă nu există recenzii. Fiți primul!',
    'Похожие инструменты': 'Instrumente similare',
    'Все в категории': 'Toate în categorie',
    ' / день': ' / zi',

    # Каталог
    'Каталог инструментов': 'Catalog de instrumente',
    'Найдите подходящий инструмент для вашего проекта': 'Găsiți instrumentul potrivit pentru proiectul dumneavoastră',
    'Поиск инструментов...': 'Căutare instrumente...',
    'Все категории': 'Toate categoriile',
    'Новые': 'Noi',
    'Сначала дешевле': 'Mai întâi cele ieftine',
    'Сначала дороже': 'Mai întâi cele scumpe',
    'По названию': 'După nume',
    'Найти': 'Căutare',
    'Цена (MDL/день):': 'Preț (MDL/zi):',
    'Применить': 'Aplicare',
    'Сбросить': 'Resetare',
    'Найдено:': 'Găsite:',
    'Хит': 'Hit',
    'Подробнее': 'Mai multe detalii',
    'MDL/день': 'MDL/zi',
    'Доступен': 'Disponibil',
    'В аренде': 'În închiriere',
    'Инструменты не найдены': 'Instrumentele nu au fost găsite',
    'Попробуйте изменить параметры поиска или сбросьте фильтры': 'Încercați să schimbați parametrii de căutare sau resetați filtrele',
    'Сбросить фильтры': 'Resetare filtre',

    # Категория
    'В этой категории пока нет инструментов': 'În această categorie nu există încă instrumente',
    'Скоро здесь появятся новые позиции': 'În curând vor apărea noi articole',
    'Вернуться в каталог': 'Înapoi la catalog',

    # FAQ
    'Частые вопросы': 'Întrebări frecvente',

    # Избранное
    'Всего:': 'Total:',

    # Прочее
    'Арендовать': 'Închiriere',
    'Отправить отзыв': 'Trimite recenzia',
    'Отправить заявку': 'Trimite cererea',
    'Иван Иванов': 'Ion Popescu',
    'Дополнительные пожелания...': 'Dorințe suplimentare...',
    'Отправляя заявку, вы соглашаетесь с условиями аренды': 'Trimițând cererea, sunteți de acord cu condițiile de închiriere',
    'Поделитесь вашим опытом использования этого инструмента...': 'Împărtășiți experiența dumneavoastră cu această unealtă...',
}

def translate_file(file_path):
    """Перевод одного файла"""
    print(f"Обработка файла: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_count = 0

        # Заменяем все фразы из словаря
        for russian, romanian in TRANSLATIONS.items():
            if russian in content:
                content = content.replace(russian, romanian)
                changes_count += 1
                print(f"  ✓ Заменено: '{russian}' → '{romanian}'")

        # Сохраняем файл только если были изменения
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Файл сохранен. Всего замен: {changes_count}\n")
            return changes_count
        else:
            print(f"  ℹ️  Изменений не требуется\n")
            return 0

    except Exception as e:
        print(f"  ❌ Ошибка при обработке файла: {e}\n")
        return 0

def main():
    """Основная функция"""
    print("=" * 70)
    print("ПЕРЕВОД HTML ФАЙЛОВ С РУССКОГО НА РУМЫНСКИЙ")
    print("=" * 70)
    print()

    # Список всех HTML файлов для обработки
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
    processed_files = 0

    for html_file in html_files:
        if os.path.exists(html_file):
            changes = translate_file(html_file)
            total_changes += changes
            if changes > 0:
                processed_files += 1
        else:
            print(f"⚠️  Файл не найден: {html_file}\n")

    print("=" * 70)
    print(f"ЗАВЕРШЕНО!")
    print(f"Обработано файлов с изменениями: {processed_files}")
    print(f"Всего выполнено замен: {total_changes}")
    print("=" * 70)

if __name__ == '__main__':
    main()
