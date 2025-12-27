#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для добавления румынских переводов для многострочных msgid
"""

# Словарь переводов
translations = [
    {
        "ru": 'msgid ""\n"Мы предоставляем профессиональное строительное оборудование в аренду уже "\n"более 5 лет, обеспечивая качество и надёжность для каждого клиента."\nmsgstr ""',
        "ro": 'msgid ""\n"Мы предоставляем профессиональное строительное оборудование в аренду уже "\n"более 5 лет, обеспечивая качество и надёжность для каждого клиента."\nmsgstr ""\n"Oferim echipamente profesionale de construcție în închiriere de peste 5 ani, "\n"asigurând calitate și fiabilitate pentru fiecare client."'
    },
    {
        "ru": 'msgid ""\n"Весь инструмент проходит тщательную проверку перед каждой арендой. Мы "\n"гарантируем исправность и надёжность оборудования."\nmsgstr ""',
        "ro": 'msgid ""\n"Весь инструмент проходит тщательную проверку перед каждой арендой. Мы "\n"гарантируем исправность и надёжность оборудования."\nmsgstr ""\n"Toate instrumentele trec printr-o verificare amănunțită înainte de fiecare "\n"închiriere. Garantăm funcționarea și fiabilitatea echipamentului."'
    },
    {
        "ru": 'msgid ""\n"Конкурентные цены на рынке аренды инструментов. Гибкая система скидок при "\n"длительной аренде и для постоянных клиентов."\nmsgstr ""',
        "ro": 'msgid ""\n"Конкурентные цены на рынке аренды инструментов. Гибкая система скидок при "\n"длительной аренде и для постоянных клиентов."\nmsgstr ""\n"Prețuri competitive pe piața de închiriere de instrumente. Sistem flexibil "\n"de reduceri pentru închirieri pe termen lung și pentru clienți permanenți."'
    },
    {
        "ru": 'msgid ""\n"Доставляем инструменты по всей Молдове. Возможен самовывоз из нашего офиса в "\n"Кишинёве или доставка на объект."\nmsgstr ""',
        "ro": 'msgid ""\n"Доставляем инструменты по всей Молдове. Возможен самовывоз из нашего офиса в "\n"Кишинёве или доставка на объект."\nmsgstr ""\n"Livrăm instrumente în toată Moldova. Este posibilă ridicarea de la biroul "\n"nostru din Chișinău sau livrarea la șantier."'
    },
    {
        "ru": 'msgid ""\n"Наши специалисты помогут подобрать подходящий инструмент и проконсультируют "\n"по вопросам эксплуатации."\nmsgstr ""',
        "ro": 'msgid ""\n"Наши специалисты помогут подобрать подходящий инструмент и проконсультируют "\n"по вопросам эксплуатации."\nmsgstr ""\n"Specialiștii noștri vă vor ajuta să alegeți instrumentul potrivit și vă vor "\n"consulta cu privire la utilizare."'
    },
    {
        "ru": 'msgid ""\n"Минимум документов и быстрое оформление аренды. Онлайн-бронирование доступно "\n"круглосуточно."\nmsgstr ""',
        "ro": 'msgid ""\n"Минимум документов и быстрое оформление аренды. Онлайн-бронирование доступно "\n"круглосуточно."\nmsgstr ""\n"Documente minime și procesare rapidă a închirierii. Rezervarea online este "\n"disponibilă non-stop."'
    },
    {
        "ru": 'msgid ""\n"Индивидуальный подход к каждому заказу. Техническая поддержка на протяжении "\n"всего срока аренды."\nmsgstr ""',
        "ro": 'msgid ""\n"Индивидуальный подход к каждому заказу. Техническая поддержка на протяжении "\n"всего срока аренды."\nmsgstr ""\n"Abordare individuală pentru fiecare comandă. Suport tehnic pe toată durata "\n"închirierii."'
    },
    {
        "ru": 'msgid ""\n"Поможем подобрать инструмент для вашей задачи. Звоните или оставьте заявку!"\nmsgstr ""',
        "ro": 'msgid ""\n"Поможем подобрать инструмент для вашей задачи. Звоните или оставьте заявку!"\nmsgstr ""\n"Vă vom ajuta să alegeți instrumentul pentru sarcina dumneavoastră. Sunați sau "\n"lăsați o cerere!"'
    }
]

def fix_translations():
    file_path = 'locale/ro/LC_MESSAGES/django.po'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    count = 0
    for item in translations:
        if item['ru'] in content:
            content = content.replace(item['ru'], item['ro'])
            count += 1
            print(f"✓ Добавлен перевод {count}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Добавлено переводов: {count}/{len(translations)}")

if __name__ == '__main__':
    fix_translations()
