#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для исправления вложенных {% trans %} тегов
"""

import os
import re

def fix_nested_trans(filepath):
    """Исправить вложенные {% trans %} в файле"""
    print(f"\nОбработка: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # Паттерн для поиска {% trans "...{% trans "..." %}..." %}
    # Ищем строки типа: {% trans "текст {% trans "вложенный" %} текст" %}
    pattern = r'{%\s*trans\s+"([^"]*{%\s*trans\s+"[^"]+"\s*%}[^"]*)"\s*%}'

    matches = list(re.finditer(pattern, content))

    for match in reversed(matches):  # Идем с конца, чтобы не сбить позиции
        full_match = match.group(0)
        inner_text = match.group(1)

        # Извлекаем внутренний {% trans "..." %}
        inner_trans = re.search(r'{%\s*trans\s+"([^"]+)"\s*%}', inner_text)
        if inner_trans:
            inner_value = inner_trans.group(1)
            # Заменяем внутренний {% trans %} на просто текст
            fixed_text = inner_text.replace(inner_trans.group(0), inner_value)
            fixed_full = f'{{% trans "{fixed_text}" %}}'

            content = content.replace(full_match, fixed_full)
            changes.append(f"  ✓ Исправлено: {full_match[:60]}...")
            print(f"  ✓ {full_match}")
            print(f"    → {fixed_full}")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Файл исправлен! Изменений: {len(changes)}")
        return len(changes)
    else:
        print(f"  ✓ Вложенных trans не найдено")
        return 0

def main():
    print("=" * 80)
    print("ИСПРАВЛЕНИЕ ВЛОЖЕННЫХ {% trans %} ТЕГОВ")
    print("=" * 80)

    html_files = [
        'templates/home.html',
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

    total = 0
    for filepath in html_files:
        if os.path.exists(filepath):
            total += fix_nested_trans(filepath)
        else:
            print(f"\n⚠️  Файл не найден: {filepath}")

    print("\n" + "=" * 80)
    print(f"✅ ГОТОВО! Всего исправлений: {total}")
    print("=" * 80)

    if total > 0:
        print("\nСледующие шаги:")
        print("1. python manage.py makemessages -l ro")
        print("2. python fix_po_file.py")
        print("3. python manage.py compilemessages")
        print("=" * 80)

if __name__ == '__main__':
    main()
