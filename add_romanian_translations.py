#!/usr/bin/env python3
"""
Автоматическое добавление румынских переводов
"""

import re

# Словарь русско-румынских переводов
TRANSLATIONS = {
    # Основные
    "Главная": "Acasă",
    "Каталог": "Catalog",
    "Каталог инструментов": "Catalog de unelte",
    "Частые вопросы": "Întrebări frecvente",
    "Оформление аренды": "Procesare închiriere",
    "Личный кабинет": "Cont personal",

    # Поиск и фильтры
    "Найдите подходящий инструмент для вашего проекта": "Găsiți unealta potrivită pentru proiectul dvs.",
    "Поиск инструментов...": "Căutare unelte...",
    "Все категории": "Toate categoriile",
    "Новые": "Noi",
    "Сначала дешевле": "Mai întâi cele ieftine",
    "Сначала дороже": "Mai întâi cele scumpe",
    "По названию": "După nume",
    "Популярные": "Populare",
    "Найти": "Căutare",
    "Цена (MDL/день):": "Preț (MDL/zi):",
    "Применить": "Aplică",
    "Сбросить": "Resetare",
    "Сбросить фильтры": "Resetare filtre",

    # Результаты
    "Найдено:": "Găsite:",
    "инструментов": "unelte",
    "Хит": "Hit",
    "Подробнее": "Detalii",
    "MDL/день": "MDL/zi",
    "Доступен": "Disponibil",
    "В аренде": "Închiriat",
    "Инструменты не найдены": "Unelte nu au fost găsite",
    "Попробуйте изменить параметры поиска или сбросьте фильтры": "Încercați să schimbați parametrii de căutare sau resetați filtrele",

    # Детали инструмента
    "Залог:": "Depozit:",
    "Залог": "Depozit",
    "Калькулятор аренды": "Calculator de închiriere",
    "Дата начала": "Data de început",
    "Дата окончания": "Data de încheiere",
    "Количество дней:": "Număr de zile:",
    "Количество дней": "Număr de zile",
    "Стоимость аренды:": "Cost închiriere:",
    "Итого к оплате:": "Total de plată:",
    "Итого к оплате": "Total de plată",
    "Доступен для аренды": "Disponibil pentru închiriere",
    "Сейчас в аренде": "Acum închiriat",
    "Арендовать": "Închiriază",
    "Недоступен": "Indisponibil",
    "Характеристики": "Caracteristici",
    "Описание": "Descriere",

    # Отзывы
    "Отзывы": "Recenzii",
    "отзывов": "recenzii",
    "Оставить отзыв": "Lăsați o recenzie",
    "Ваша оценка": "Evaluarea dumneavoastră",
    "Ваш отзыв (необязательно)": "Recenzia dumneavoastră (opțional)",
    "Поделитесь вашим опытом использования этого инструмента...": "Împărtășiți experiența dumneavoastră cu această unealtă...",
    "Отправить отзыв": "Trimite recenzia",
    "Войдите, чтобы оставить отзыв": "Autentificați-vă pentru a lăsa o recenzie",
    "Войти": "Autentificare",
    "Пока нет отзывов. Будьте первым!": "Încă nu există recenzii. Fiți primul!",
    "Похожие инструменты": "Unelte similare",
    "Все в категории": "Toate din categorie",

    # FAQ
    "Ответы на популярные вопросы об аренде инструментов": "Răspunsuri la întrebările frecvente despre închirierea uneltelor",
    "Не нашли ответ на свой вопрос?": "Nu ați găsit răspuns la întrebarea dumneavoastră?",
    "Свяжитесь с нами любым удобным способом": "Contactați-ne în orice mod convenabil",
    "WhatsApp": "WhatsApp",
    "Telegram": "Telegram",
    "Позвонить": "Sună",
    "FAQ пока пусто": "FAQ încă gol",
    "Скоро здесь появятся ответы на частые вопросы": "În curând vor apărea răspunsuri la întrebările frecvente",
    "Перейти в каталог": "Mergi la catalog",

    # Форма заявки
    "Ваше имя": "Numele dumneavoastră",
    "Иван Иванов": "Ion Popescu",
    "Email": "Email",
    "Телефон": "Telefon",
    "Комментарий": "Comentariu",
    "Дополнительные пожелания...": "Dorințe suplimentare...",
    "Цена за день": "Preț pe zi",
    "Отправить заявку": "Trimite cererea",
    "Отправляя заявку, вы соглашаетесь с условиями аренды": "Trimițând cererea, sunteți de acord cu condițiile de închiriere",

    # Дашборд
    "Добро пожаловать,": "Bine ați venit,",
    "Всего заявок": "Total cereri",
    "Активных": "Active",
    "Завершённых": "Finalizate",
    "Каталог инструментов": "Catalog de unelte",
    "Редактировать профиль": "Editează profilul",
    "Все заявки": "Toate cererile",
    "Последние заявки": "Ultimele cereri",
    "Номер": "Număr",
    "Инструмент": "Unealtă",
    "Период": "Perioadă",
    "Сумма": "Sumă",
    "Статус": "Status",
    "У вас пока нет заявок": "Nu aveți încă cereri",
    "Выберите инструмент и оформите первую аренду": "Alegeți o unealtă și creați prima închiriere",
}


def add_romanian_translations(po_file_path):
    """Добавляет румынские переводы в .po файл"""
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Для каждого перевода
    for ru_text, ro_text in TRANSLATIONS.items():
        # Ищем паттерн: msgid "русский текст"\nmsgstr ""
        pattern = re.compile(
            rf'(msgid "{re.escape(ru_text)}"\s*\nmsgstr) ""',
            re.MULTILINE
        )
        # Заменяем на: msgid "русский текст"\nmsgstr "румынский текст"
        replacement = rf'\1 "{ro_text}"'
        content = pattern.sub(replacement, content)

    # Сохраняем
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Румынские переводы добавлены в {po_file_path}")


def fill_russian_translations(po_file_path):
    """Заполняет русские переводы (копирует msgid в msgstr)"""
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        result.append(line)

        # Если это msgid с русским текстом и следующий msgstr пустой
        if line.startswith('msgid "') and i + 1 < len(lines):
            next_line = lines[i + 1]
            if next_line.strip() == 'msgstr ""':
                # Извлекаем текст из msgid
                match = re.match(r'msgid "(.*)"', line)
                if match:
                    text = match.group(1)
                    # Если в тексте есть кириллица - это русский текст
                    if any('\u0400' <= c <= '\u04FF' for c in text):
                        # Копируем msgid в msgstr
                        result.append(f'msgstr "{text}"\n')
                        i += 2  # Пропускаем следующую строку
                        continue

        i += 1

    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.writelines(result)

    print(f"✅ Русские переводы заполнены в {po_file_path}")


if __name__ == '__main__':
    print("🚀 Начинаю добавление переводов...\n")

    # Добавляем румынские переводы
    add_romanian_translations('/home/alex/moldtool/locale/ro/LC_MESSAGES/django.po')

    # Заполняем русские переводы
    fill_russian_translations('/home/alex/moldtool/locale/ru/LC_MESSAGES/django.po')

    print("\n✨ Готово! Переводы добавлены.")
    print("\n📝 Следующий шаг: python manage.py compilemessages")
