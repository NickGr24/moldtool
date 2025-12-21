#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для добавления румынских переводов для непереведенных строк
"""

import re

# Словарь переводов с русского на румынский
translations = {
    # Общие
    "Статистика и аналитика MoldTool": "Statistici și analiză MoldTool",
    "за неделю": "pe săptămână",
    "Ср. рейтинг:": "Rating mediu:",
    "Нет данных": "Nu există date",
    "MDL/Zi": "MDL/zi",
    "/ Zi": "/ zi",

    # Каталог
    "Каталог инструментов": "Catalog de instrumente",
    "Найдите подходящий инструмент для вашего проекта": "Găsiți instrumentul potrivit pentru proiectul dumneavoastră",
    "Поиск инструментов...": "Căutare instrumente...",
    "Все категории": "Toate categoriile",
    "Новые": "Noi",
    "Сначала дешевле": "Mai întâi cele ieftine",
    "Цена (MDL/день):": "Preț (MDL/zi):",
    "Найдено:": "Găsite:",

    # Прочее
    "Единиц техники": "Unități de echipament",
    "Довольных клиентов": "Clienți mulțumiți",
    "Лет опыта": "Ani de experiență",
}

def add_translations():
    file_path = 'locale/ro/LC_MESSAGES/django.po'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Для каждого перевода
    for ru_text, ro_text in translations.items():
        # Ищем паттерн: msgid "текст"\nmsgstr ""
        pattern = rf'(msgid "{re.escape(ru_text)}"\nmsgstr ")("")'
        replacement = rf'\1{ro_text}"'
        content = re.sub(pattern, replacement, content)

        # Также обработаем fuzzy переводы
        pattern = rf'(#, fuzzy\n(?:#\| msgid.*\n)*msgid "{re.escape(ru_text)}"\nmsgstr ")([^"]*")'
        replacement = rf'msgid "{ru_text}"\nmsgstr "{ro_text}"'
        content = re.sub(pattern, replacement, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Добавлено {len(translations)} переводов в {file_path}")

if __name__ == '__main__':
    add_translations()
