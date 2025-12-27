#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для исправления смешанного русско-румынского текста в {% trans %}
"""

import os

FIXES = {
    'templates/catalog/tool_detail.html': [
        ('{% trans "Inдоступно" %}', '{% trans "Недоступен" %}'),
        ('{% trans "Доступен pentru închiriere" %}', '{% trans "Доступен для аренды" %}'),
        ('{% trans "Номер de zile:" %}', '{% trans "Количество дней:" %}'),
    ],
    'templates/catalog/favorites.html': [
        ('{% trans "Total:" %}', '{% trans "Всего:" %}'),
        ('{% trans "instrumente" %}', '{% trans "инструментов" %}'),
        ('{% trans "Disponibil" %}', '{% trans "Доступен" %}'),
        ('{% trans "În închiriere" %}', '{% trans "В аренде" %}'),
    ],
    'templates/catalog/category.html': [
        ('{% trans "Găsite:" %}', '{% trans "Найдено:" %}'),
        ('{% trans "instrumente" %}', '{% trans "инструментов" %}'),
        ('{% trans "Disponibil" %}', '{% trans "Доступен" %}'),
        ('{% trans "În închiriere" %}', '{% trans "В аренде" %}'),
    ],
    'templates/catalog/catalog.html': [
        ('{% trans "Găsite:" %}', '{% trans "Найдено:" %}'),
        ('{% trans "instrumente" %}', '{% trans "инструментов" %}'),
        ('{% trans "Disponibil" %}', '{% trans "Доступен" %}'),
        ('{% trans "În închiriere" %}', '{% trans "В аренде" %}'),
    ],
}

def fix_file(filepath, replacements):
    """Исправить файл"""
    print(f"\nОбработка: {filepath}")

    if not os.path.exists(filepath):
        print(f"  ⚠️  Файл не найден")
        return 0

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    count = 0

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            count += 1
            print(f"  ✓ {old} → {new}")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Исправлено: {count} замен")
        return count
    else:
        print(f"  ℹ️  Изменений не требуется")
        return 0

def main():
    print("=" * 80)
    print("ИСПРАВЛЕНИЕ СМЕШАННОГО РУССКО-РУМЫНСКОГО ТЕКСТА")
    print("=" * 80)

    total = 0
    for filepath, replacements in FIXES.items():
        total += fix_file(filepath, replacements)

    print("\n" + "=" * 80)
    print(f"✅ ГОТОВО! Всего исправлений: {total}")
    print("=" * 80)

if __name__ == '__main__':
    main()
