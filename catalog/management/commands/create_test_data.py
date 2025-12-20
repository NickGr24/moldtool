"""
Management command для создания тестовых данных.
Использование: python manage.py create_test_data
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from catalog.models import Category, Tool
import random


class Command(BaseCommand):
    help = 'Создаёт тестовые категории и инструменты'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Удалить существующие данные перед созданием',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Удаление существующих данных...')
            Tool.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('Данные удалены'))

        self.stdout.write('Создание тестовых данных...')

        # Создаём категории
        categories_data = [
            {
                'name': 'Электроинструменты',
                'description': 'Дрели, перфораторы, шуруповёрты и другие электрические инструменты',
                'icon': 'icon-drill',
            },
            {
                'name': 'Строительное оборудование',
                'description': 'Бетономешалки, виброплиты, генераторы',
                'icon': 'icon-construction',
            },
            {
                'name': 'Садовая техника',
                'description': 'Газонокосилки, триммеры, культиваторы',
                'icon': 'icon-garden',
            },
            {
                'name': 'Сварочное оборудование',
                'description': 'Сварочные аппараты, маски, электроды',
                'icon': 'icon-welding',
            },
            {
                'name': 'Измерительные приборы',
                'description': 'Лазерные уровни, дальномеры, детекторы',
                'icon': 'icon-measure',
            },
            {
                'name': 'Клининговое оборудование',
                'description': 'Мойки высокого давления, пылесосы, поломоечные машины',
                'icon': 'icon-cleaning',
            },
        ]

        categories = []
        for i, cat_data in enumerate(categories_data):
            cat, created = Category.objects.get_or_create(
                slug=slugify(cat_data['name'], allow_unicode=True),
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'order': i,
                }
            )
            categories.append(cat)
            status = 'создана' if created else 'уже существует'
            self.stdout.write(f'  Категория "{cat.name}" - {status}')

        # Тестовые инструменты
        tools_data = [
            # Электроинструменты
            {
                'category': 'Электроинструменты',
                'name': 'Перфоратор Bosch GBH 2-26 DRE',
                'brand': 'Bosch',
                'model_name': 'GBH 2-26 DRE',
                'description': 'Профессиональный перфоратор для сверления и долбления. Мощность 800 Вт, энергия удара 2.7 Дж. Идеален для работы с бетоном, кирпичом и камнем.',
                'price_per_day': 150,
                'deposit': 1500,
                'specifications': {
                    'Мощность': '800 Вт',
                    'Энергия удара': '2.7 Дж',
                    'Частота ударов': '4000 уд/мин',
                    'Макс. диаметр сверления': '26 мм',
                    'Вес': '2.7 кг',
                },
            },
            {
                'category': 'Электроинструменты',
                'name': 'Шуруповёрт Makita DDF453',
                'brand': 'Makita',
                'model_name': 'DDF453',
                'description': 'Аккумуляторный шуруповёрт с литий-ионным аккумулятором 18V. Два режима скорости, LED подсветка рабочей зоны.',
                'price_per_day': 100,
                'deposit': 1000,
                'specifications': {
                    'Напряжение': '18 В',
                    'Крутящий момент': '42 Нм',
                    'Скорость': '0-400/0-1300 об/мин',
                    'Патрон': '13 мм',
                    'Вес': '1.7 кг',
                },
            },
            {
                'category': 'Электроинструменты',
                'name': 'Болгарка DeWalt DWE4257',
                'brand': 'DeWalt',
                'model_name': 'DWE4257',
                'description': 'Угловая шлифмашина с регулировкой оборотов. Подходит для резки и шлифовки металла, камня, плитки.',
                'price_per_day': 120,
                'deposit': 1200,
                'specifications': {
                    'Мощность': '1500 Вт',
                    'Диаметр диска': '125 мм',
                    'Обороты': '2800-10000 об/мин',
                    'Вес': '2.5 кг',
                },
            },
            {
                'category': 'Электроинструменты',
                'name': 'Лобзик Bosch GST 150 BCE',
                'brand': 'Bosch',
                'model_name': 'GST 150 BCE',
                'description': 'Профессиональный электролобзик для фигурной резки дерева, металла, пластика. Маятниковый ход, регулировка скорости.',
                'price_per_day': 90,
                'deposit': 900,
                'specifications': {
                    'Мощность': '780 Вт',
                    'Глубина пропила (дерево)': '150 мм',
                    'Глубина пропила (металл)': '20 мм',
                    'Ход пилки': '26 мм',
                },
            },

            # Строительное оборудование
            {
                'category': 'Строительное оборудование',
                'name': 'Бетономешалка Skiper CM-120',
                'brand': 'Skiper',
                'model_name': 'CM-120',
                'description': 'Бетономешалка объёмом 120 литров. Идеальна для небольших строительных работ, заливки фундамента, приготовления раствора.',
                'price_per_day': 200,
                'deposit': 2000,
                'specifications': {
                    'Объём барабана': '120 л',
                    'Готовая смесь': '90 л',
                    'Мощность': '550 Вт',
                    'Напряжение': '220 В',
                    'Вес': '45 кг',
                },
            },
            {
                'category': 'Строительное оборудование',
                'name': 'Виброплита Wacker Neuson WP1550A',
                'brand': 'Wacker Neuson',
                'model_name': 'WP1550A',
                'description': 'Виброплита для уплотнения грунта, песка, щебня. Бензиновый двигатель Honda.',
                'price_per_day': 350,
                'deposit': 5000,
                'specifications': {
                    'Центробежная сила': '15 кН',
                    'Размер плиты': '500x360 мм',
                    'Двигатель': 'Honda GX160',
                    'Вес': '68 кг',
                },
            },
            {
                'category': 'Строительное оборудование',
                'name': 'Генератор Fubag BS 6600',
                'brand': 'Fubag',
                'model_name': 'BS 6600',
                'description': 'Бензиновый генератор мощностью 6 кВт. Надёжный источник электроэнергии для строительной площадки.',
                'price_per_day': 400,
                'deposit': 5000,
                'specifications': {
                    'Мощность': '6.0 кВт',
                    'Напряжение': '220/380 В',
                    'Объём бака': '25 л',
                    'Время работы': '8-10 ч',
                    'Вес': '78 кг',
                },
            },

            # Садовая техника
            {
                'category': 'Садовая техника',
                'name': 'Газонокосилка Honda HRG 416 SK',
                'brand': 'Honda',
                'model_name': 'HRG 416 SK',
                'description': 'Самоходная бензиновая газонокосилка с травосборником. Ширина скашивания 41 см.',
                'price_per_day': 180,
                'deposit': 2500,
                'specifications': {
                    'Ширина скашивания': '41 см',
                    'Высота скашивания': '20-74 мм',
                    'Объём травосборника': '50 л',
                    'Двигатель': 'Honda GCV160',
                },
            },
            {
                'category': 'Садовая техника',
                'name': 'Триммер Stihl FS 55',
                'brand': 'Stihl',
                'model_name': 'FS 55',
                'description': 'Бензиновый триммер для кошения травы в труднодоступных местах. Лёгкий и манёвренный.',
                'price_per_day': 100,
                'deposit': 1500,
                'specifications': {
                    'Мощность': '1.0 л.с.',
                    'Объём двигателя': '27.2 см³',
                    'Ширина скашивания': '38 см',
                    'Вес': '5.0 кг',
                },
            },
            {
                'category': 'Садовая техника',
                'name': 'Культиватор Husqvarna TF 230',
                'brand': 'Husqvarna',
                'model_name': 'TF 230',
                'description': 'Бензиновый культиватор для обработки почвы. Глубина обработки до 30 см.',
                'price_per_day': 250,
                'deposit': 3000,
                'specifications': {
                    'Мощность': '4.5 л.с.',
                    'Ширина обработки': '60-80 см',
                    'Глубина обработки': '30 см',
                    'Вес': '49 кг',
                },
            },

            # Сварочное оборудование
            {
                'category': 'Сварочное оборудование',
                'name': 'Сварочный инвертор Ресанта САИ 220',
                'brand': 'Ресанта',
                'model_name': 'САИ 220',
                'description': 'Инверторный сварочный аппарат для ручной дуговой сварки. Ток до 220А, работа с электродами до 5 мм.',
                'price_per_day': 150,
                'deposit': 2000,
                'specifications': {
                    'Сварочный ток': '10-220 А',
                    'Напряжение': '220 В',
                    'Диаметр электрода': '1.6-5.0 мм',
                    'ПВ': '70%',
                    'Вес': '4.9 кг',
                },
            },
            {
                'category': 'Сварочное оборудование',
                'name': 'Полуавтомат Сварог MIG 200',
                'brand': 'Сварог',
                'model_name': 'MIG 200',
                'description': 'Сварочный полуавтомат для сварки в среде защитного газа. MIG/MAG, MMA режимы.',
                'price_per_day': 250,
                'deposit': 3500,
                'specifications': {
                    'Сварочный ток MIG': '40-200 А',
                    'Сварочный ток MMA': '20-180 А',
                    'Диаметр проволоки': '0.6-1.0 мм',
                    'Вес': '12.5 кг',
                },
            },

            # Измерительные приборы
            {
                'category': 'Измерительные приборы',
                'name': 'Лазерный уровень Bosch GLL 3-80',
                'brand': 'Bosch',
                'model_name': 'GLL 3-80',
                'description': 'Профессиональный лазерный уровень с тремя плоскостями 360°. Точность ±0.2 мм/м.',
                'price_per_day': 200,
                'deposit': 3000,
                'specifications': {
                    'Количество линий': '3 x 360°',
                    'Точность': '±0.2 мм/м',
                    'Дальность': '30 м (80 м с приёмником)',
                    'Самонивелирование': '±4°',
                },
            },
            {
                'category': 'Измерительные приборы',
                'name': 'Лазерный дальномер Leica DISTO D2',
                'brand': 'Leica',
                'model_name': 'DISTO D2',
                'description': 'Компактный лазерный дальномер с Bluetooth. Измерение расстояний до 100 м.',
                'price_per_day': 80,
                'deposit': 1500,
                'specifications': {
                    'Дальность': '0.05-100 м',
                    'Точность': '±1.5 мм',
                    'Bluetooth': 'Да',
                    'Память': '10 измерений',
                },
            },
            {
                'category': 'Измерительные приборы',
                'name': 'Детектор проводки Bosch GMS 120',
                'brand': 'Bosch',
                'model_name': 'GMS 120',
                'description': 'Универсальный детектор для поиска металла, проводки, деревянных конструкций в стенах.',
                'price_per_day': 50,
                'deposit': 800,
                'specifications': {
                    'Глубина обнаружения (сталь)': '120 мм',
                    'Глубина обнаружения (медь)': '80 мм',
                    'Глубина обнаружения (проводка)': '50 мм',
                    'Глубина обнаружения (дерево)': '38 мм',
                },
            },

            # Клининговое оборудование
            {
                'category': 'Клининговое оборудование',
                'name': 'Мойка высокого давления Karcher K5',
                'brand': 'Karcher',
                'model_name': 'K5 Premium',
                'description': 'Мощная мойка высокого давления для автомобилей, фасадов, садовой мебели. Давление до 145 бар.',
                'price_per_day': 180,
                'deposit': 2500,
                'specifications': {
                    'Давление': '20-145 бар',
                    'Производительность': '500 л/ч',
                    'Мощность': '2.1 кВт',
                    'Длина шланга': '8 м',
                },
            },
            {
                'category': 'Клининговое оборудование',
                'name': 'Промышленный пылесос Karcher NT 30/1',
                'brand': 'Karcher',
                'model_name': 'NT 30/1 Tact L',
                'description': 'Профессиональный пылесос для сухой и влажной уборки. Объём бака 30 л, автоматическая очистка фильтра.',
                'price_per_day': 150,
                'deposit': 2000,
                'specifications': {
                    'Объём бака': '30 л',
                    'Мощность': '1380 Вт',
                    'Разрежение': '254 мбар',
                    'Расход воздуха': '74 л/с',
                },
            },
            {
                'category': 'Клининговое оборудование',
                'name': 'Поломоечная машина Karcher BD 30/4 C',
                'brand': 'Karcher',
                'model_name': 'BD 30/4 C',
                'description': 'Компактная поломоечная машина для уборки небольших помещений. Работа от аккумулятора.',
                'price_per_day': 300,
                'deposit': 5000,
                'specifications': {
                    'Производительность': '630 м²/ч',
                    'Ширина щётки': '300 мм',
                    'Бак чистой воды': '4 л',
                    'Время работы': '25 мин',
                },
            },
        ]

        # Создаём инструменты
        created_count = 0
        for tool_data in tools_data:
            category = Category.objects.get(name=tool_data['category'])
            slug = slugify(tool_data['name'], allow_unicode=True)

            tool, created = Tool.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': tool_data['name'],
                    'category': category,
                    'brand': tool_data.get('brand', ''),
                    'model_name': tool_data.get('model_name', ''),
                    'description': tool_data['description'],
                    'short_description': tool_data['description'][:150] + '...' if len(tool_data['description']) > 150 else tool_data['description'],
                    'price_per_day': tool_data['price_per_day'],
                    'deposit': tool_data.get('deposit', 0),
                    'specifications': tool_data.get('specifications', {}),
                    'condition': random.choice(['new', 'excellent', 'good']),
                    'availability': 'available',
                    'is_featured': random.choice([True, False, False, False]),  # 25% шанс быть featured
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'  + {tool.name}')
            else:
                self.stdout.write(f'  = {tool.name} (уже существует)')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Готово! Создано категорий: {len(categories)}, инструментов: {created_count}'
        ))
        self.stdout.write('')
        self.stdout.write('Примечание: Изображения не добавлены.')
        self.stdout.write('Добавьте изображения через админ-панель: /admin/catalog/tool/')
