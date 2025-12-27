#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для замены румынского текста на русский в {% trans %} тегах
"""

import os

def fix_file(filepath, replacements):
    """Исправить файл"""
    print(f"Обработка: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    count = 0

    for romanian, russian in replacements:
        if romanian in content:
            content = content.replace(romanian, russian)
            count += 1
            print(f"  ✓ {romanian} → {russian}")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Исправлено: {count} замен\n")
        return count
    else:
        print(f"  ℹ️  Изменений не требуется\n")
        return 0

def main():
    print("=" * 80)
    print("ИСПРАВЛЕНИЕ РУМЫНСКОГО ТЕКСТА В {% trans %} ТЕГАХ")
    print("=" * 80)
    print()

    # Файлы и их замены
    files_to_fix = {
        'templates/catalog/catalog.html': [
            ('{% trans "Catalog instrumente" %}', '{% trans "Каталог инструментов" %}'),
            ('<span class="text-white">{% trans "Catalog" %}</span>', '<span class="text-white">{% trans "Каталог" %}</span>'),
        ],
        'templates/catalog/category.html': [
            ('{% trans "Catalog" %}', '{% trans "Каталог" %}'),
        ],
        'templates/catalog/tool_detail.html': [
            ('{% trans "Catalog" %}', '{% trans "Каталог" %}'),
        ],
        'templates/includes/header.html': [
            ('<span class="relative">{% trans "Catalog" %}</span>', '<span class="relative">{% trans "Каталог" %}</span>'),
            ('<span class="font-medium">{% trans "Catalog" %}</span>', '<span class="font-medium">{% trans "Каталог" %}</span>'),
        ],
        'templates/includes/footer.html': [
            ('{% trans "Catalog" %}', '{% trans "Каталог" %}'),
        ],
    }

    total = 0
    for filepath, replacements in files_to_fix.items():
        if os.path.exists(filepath):
            total += fix_file(filepath, replacements)
        else:
            print(f"⚠️  Файл не найден: {filepath}\n")

    print("=" * 80)
    print(f"✅ ГОТОВО! Всего исправлений: {total}")
    print("=" * 80)
    print()
    print("Следующие шаги:")
    print("1. python manage.py makemessages -l ro")
    print("2. python fix_po_file.py")
    print("3. python manage.py compilemessages")
    print("=" * 80)

if __name__ == '__main__':
    main()
