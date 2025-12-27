#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для добавления длинных румынских переводов
"""

import re

# Длинные переводы
long_translations = {
    "Мы предоставляем профессиональное строительное оборудование в аренду уже более 5 лет, обеспечивая качество и надёжность для каждого клиента.":
    "Oferim echipamente profesionale de construcție în închiriere de peste 5 ani, asigurând calitate și fiabilitate pentru fiecare client.",

    "Весь инструмент проходит тщательную проверку перед каждой арендой. Мы гарантируем исправность и надёжность оборудования.":
    "Toate instrumentele trec printr-o verificare amănunțită înainte de fiecare închiriere. Garantăm funcționarea și fiabilitatea echipamentului.",

    "Конкурентные цены на рынке аренды инструментов. Гибкая система скидок при длительной аренде и для постоянных клиентов.":
    "Prețuri competitive pe piața de închiriere de instrumente. Sistem flexibil de reduceri pentru închirieri pe termen lung și pentru clienți permanenți.",

    "Доставляем инструменты по всей Молдове. Возможен самовывоз из нашего офиса в Кишинёве или доставка на объект.":
    "Livrăm instrumente în toată Moldova. Este posibilă ridicarea de la biroul nostru din Chișinău sau livrarea la șantier.",

    "Наши специалисты помогут подобрать подходящий инструмент и проконсультируют по вопросам эксплуатации.":
    "Specialiștii noștri vă vor ajuta să alegeți instrumentul potrivit și vă vor consulta cu privire la utilizare.",

    "Минимум документов и быстрое оформление аренды. Онлайн-бронирование доступно круглосуточно.":
    "Documente minime și procesare rapidă a închirierii. Rezervarea online este disponibilă non-stop.",

    "Индивидуальный подход к каждому заказу. Техническая поддержка на протяжении всего срока аренды.":
    "Abordare individuală pentru fiecare comandă. Suport tehnic pe toată durata închirierii.",

    "Поможем подобрать инструмент для вашей задачи. Звоните или оставьте заявку!":
    "Vă vom ajuta să alegeți instrumentul pentru sarcina dumneavoastră. Sunați sau lăsați o cerere!"
}

def add_long_translations():
    file_path = 'locale/ro/LC_MESSAGES/django.po'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Для каждого перевода
    count = 0
    for ru_text, ro_text in long_translations.items():
        # Ищем многострочный msgid
        # Заменяем пробелы и переносы на универсальный паттерн
        ru_escaped = re.escape(ru_text)
        ru_pattern = ru_escaped.replace('\\ ', '\\s+').replace('\\n', '\\s+')

        # Паттерн для поиска msgid с возможными переносами строк
        pattern = rf'(msgid\s+"[^"]*"(?:\s*"[^"]*")*\s*msgstr\s+)("")'

        # Более простой подход - ищем точное совпадение с учетом многострочности
        old_pattern = f'msgid "{ru_text}"\nmsgstr ""'
        new_value = f'msgid "{ru_text}"\nmsgstr "{ro_text}"'

        if old_pattern in content:
            content = content.replace(old_pattern, new_value)
            count += 1
            print(f"✓ Переведено: {ru_text[:50]}...")
        else:
            # Попробуем найти с переносами строк (многострочный msgid)
            # Django разбивает длинные строки на несколько
            lines = ru_text.split()
            # Ищем первые несколько слов
            first_words = ' '.join(lines[:5])
            if first_words in content:
                print(f"⚠ Найдена многострочная версия: {first_words}...")
                # Для многострочных нужна ручная обработка

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Обработано переводов: {count}/{len(long_translations)}")
    print(f"⚠ Для остальных требуется ручное добавление (многострочные msgid)")

if __name__ == '__main__':
    add_long_translations()
