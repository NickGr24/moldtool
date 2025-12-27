#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для исправления двойных {% trans %} тегов
"""

import os
import re

def fix_double_trans(filepath):
    """Исправить двойные {% trans %} в файле"""
    print(f"Проверка: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # Паттерн для поиска {% trans "{% trans "..." %}" %}
    pattern = r'{%\s*trans\s+"({%\s*trans\s+"[^"]+"\s*%})"\s*%}'

    # Находим все совпадения
    matches = re.findall(pattern, content)
    if matches:
        for match in matches:
            print(f"  ⚠️  Найден двойной trans: {match}")
            # Заменяем на внутренний trans
            content = content.replace(f'{{% trans "{match}" %}}', match)
            changes.append(f"  ✓ Исправлено: {match}")

    # Также ищем случаи вроде {% trans "Catalog" %} где Catalog это румынское слово
    # которое должно быть русским

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ Файл исправлен!")
        for change in changes:
            print(change)
        print()
        return True
    else:
        print(f"  ✓ Ок, двойных trans не найдено\n")
        return False

def main():
    print("=" * 80)
    print("ПОИСК И ИСПРАВЛЕНИЕ ДВОЙНЫХ {% trans %} ТЕГОВ")
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

    fixed = 0
    for filepath in html_files:
        if os.path.exists(filepath):
            if fix_double_trans(filepath):
                fixed += 1
        else:
            print(f"⚠️  Файл не найден: {filepath}\n")

    print("=" * 80)
    print(f"✅ Исправлено файлов: {fixed}")
    print("=" * 80)

if __name__ == '__main__':
    main()
