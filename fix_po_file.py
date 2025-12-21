#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Улучшенный скрипт для добавления переводов в .po файл
"""

import re

# Полный словарь переводов
TRANSLATIONS = {
    'Широкий выбор строительных инструментов в аренду по доступным ценам.': 'O gamă largă de instrumente de construcție de închiriat la prețuri accesibile.',
    'аренда инструментов, строительные инструменты, прокат инструментов, Молдова, Кишинёв': 'închiriere instrumente, instrumente de construcție, închiriere unelte, Moldova, Chișinău',
    'Основные цвета бренда (из логотипа)': 'Culorile principale ale brandului (din logo)',
    'Тёмная тема': 'Tema întunecată',
    'Для обратной совместимости': 'Pentru compatibilitate inversă',
    'Legacy CSS (для совместимости с другими страницами)': 'Legacy CSS (pentru compatibilitate cu alte pagini)',
    'Главная': 'Acasă',
    'Каталог': 'Catalog',
    'О нас': 'Despre noi',
    'Контакты': 'Contacte',
    'Избранное': 'Favorite',
    'Панель управления': 'Panou de control',
    'Войти': 'Autentificare',
    'Личный кабинет': 'Cont personal',
    'Добро пожаловать': 'Bun venit',
    'Всего заявок': 'Total cereri',
    'Активных': 'Active',
    'Завершённых': 'Finalizate',
    'Последние заявки': 'Ultimele cereri',
    'Номер': 'Număr',
    'Период': 'Perioadă',
    'Статус': 'Status',
    'У вас пока нет заявок': 'Nu aveți încă cereri',
    'Выберите инструмент и оформите первую аренду': 'Alegeți o unealtă și faceți prima închiriere',
    'Перейти в каталог': 'Mergi la catalog',
    'Оформление аренды': 'Procesare închiriere',
    'Ваше имя': 'Numele dumneavoastră',
    'Телефон': 'Telefon',
    'Дата начала': 'Data de început',
    'Дата окончания': 'Data de sfârșit',
    'Комментарий': 'Comentariu',
    'Количество дней': 'Număr de zile',
    'Залог': 'Depozit',
    'Итого к оплате': 'Total de plată',
    'Арендовать': 'Închiriere',
    'Отправить заявку': 'Trimite cererea',
    'Иван Иванов': 'Ion Popescu',
    'Дополнительные пожелания...': 'Dorințe suplimentare...',
    'Отправляя заявку, вы соглашаетесь с условиями аренды': 'Trimițând cererea, sunteți de acord cu condițiile de închiriere',
    'Заявка отправлена': 'Cererea a fost trimisă',
    'Ваша заявка': 'Cererea dumneavoastră',
    'успешно создана.': 'a fost creată cu succes.',
    'Мы свяжемся с вами в ближайшее время для подтверждения.': 'Vă vom contacta în curând pentru confirmare.',
    'Инструмент': 'Unealtă',
    'Период аренды': 'Perioada de închiriere',
    'Сумма': 'Sumă',
    'Продолжить выбор': 'Continuați selecția',
    'Мои заявки': 'Cererile mele',
    'Если у вас есть вопросы, звоните:': 'Dacă aveți întrebări, sunați:',
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
    'Хит': 'Hit',
    'Отправить отзыв': 'Trimite recenzia',
    'Поделитесь вашим опытом использования этого инструмента...': 'Împărtășiți experiența dumneavoastră cu această unealtă...',
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
    'Подробнее': 'Mai multe detalii',
    'MDL/день': 'MDL/zi',
    'Доступен': 'Disponibil',
    'В аренде': 'În închiriere',
    'Инструменты не найдены': 'Instrumentele nu au fost găsite',
    'Попробуйте изменить параметры поиска или сбросьте фильтры': 'Încercați să schimbați parametrii de căutare sau resetați filtrele',
    'Сбросить фильтры': 'Resetare filtre',
    'В этой категории пока нет инструментов': 'În această categorie nu există încă instrumente',
    'Скоро здесь появятся новые позиции': 'În curând vor apărea noi articole',
    'Вернуться в каталог': 'Înapoi la catalog',
    'Частые вопросы': 'Întrebări frecvente',
    'Всего:': 'Total:',
    'Все заявки': 'Toate cererile',
    'Редактировать профиль': 'Editare profil',
    'Catalog': 'Catalog',
}

def fix_po_file(filepath):
    """Обновить .po файл с переводами"""
    print(f"Читаем файл: {filepath}\n")

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    updated_count = 0
    i = 0

    while i < len(lines):
        line = lines[i]

        # Ищем строки msgid
        if line.startswith('msgid "') and not line.startswith('msgid ""'):
            # Извлекаем текст между кавычками
            msgid_match = re.match(r'msgid "(.+)"', line)
            if msgid_match:
                msgid_text = msgid_match.group(1)

                # Добавляем текущую строку msgid
                new_lines.append(line)
                i += 1

                # Проверяем следующую строку (должна быть msgstr)
                if i < len(lines) and lines[i].startswith('msgstr "'):
                    msgstr_match = re.match(r'msgstr "(.*)"\s*$', lines[i])
                    if msgstr_match:
                        current_msgstr = msgstr_match.group(1)

                        # Если перевод пустой и есть в словаре
                        if not current_msgstr and msgid_text in TRANSLATIONS:
                            translation = TRANSLATIONS[msgid_text]
                            new_lines.append(f'msgstr "{translation}"\n')
                            updated_count += 1
                            print(f"✓ {msgid_text} → {translation}")
                            i += 1
                        else:
                            new_lines.append(lines[i])
                            i += 1
                    else:
                        new_lines.append(lines[i])
                        i += 1
                else:
                    continue
            else:
                new_lines.append(line)
                i += 1
        else:
            new_lines.append(line)
            i += 1

    # Записываем обратно
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"\n✅ Обновлено переводов: {updated_count}")
    return updated_count

def main():
    print("=" * 80)
    print("АВТОМАТИЧЕСКОЕ ДОБАВЛЕНИЕ ПЕРЕВОДОВ В .PO ФАЙЛ")
    print("=" * 80)
    print()

    po_file = 'locale/ro/LC_MESSAGES/django.po'

    if not os.path.exists(po_file):
        print(f"❌ Файл не найден: {po_file}")
        return

    updated = fix_po_file(po_file)

    print()
    print("=" * 80)
    print(f"✅ ГОТОВО! Добавлено переводов: {updated}")
    print()
    print("Следующий шаг:")
    print("  python manage.py compilemessages")
    print("=" * 80)

if __name__ == '__main__':
    import os
    main()
