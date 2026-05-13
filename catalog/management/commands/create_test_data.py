"""
Management command pentru crearea datelor de test.
Utilizare: python manage.py create_test_data
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from catalog.models import Category, Tool
import random


class Command(BaseCommand):
    help = 'Creează categorii și scule de test'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Șterge datele existente înainte de creare',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Ștergere date existente...')
            Tool.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('Datele au fost șterse'))

        self.stdout.write('Creare date de test...')

        # Creăm categoriile
        categories_data = [
            {
                'name': 'Scule electrice',
                'description': 'Bormașini, perforatoare, șurubelnițe și alte scule electrice',
                'icon': 'icon-drill',
            },
            {
                'name': 'Echipament de construcție',
                'description': 'Betoniere, plăci vibrante, generatoare',
                'icon': 'icon-construction',
            },
            {
                'name': 'Tehnică de grădină',
                'description': 'Mașini de tuns iarba, trimere, motocultoare',
                'icon': 'icon-garden',
            },
            {
                'name': 'Echipament de sudură',
                'description': 'Aparate de sudură, măști, electrozi',
                'icon': 'icon-welding',
            },
            {
                'name': 'Aparate de măsură',
                'description': 'Niveluri laser, telemetre, detectoare',
                'icon': 'icon-measure',
            },
            {
                'name': 'Echipament de curățenie',
                'description': 'Aparate de spălat cu presiune, aspiratoare, mașini de spălat pardoseli',
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
            status = 'creată' if created else 'există deja'
            self.stdout.write(f'  Categoria "{cat.name}" - {status}')

        # Scule de test
        tools_data = [
            # Scule electrice
            {
                'category': 'Scule electrice',
                'name': 'Perforator Bosch GBH 2-26 DRE',
                'brand': 'Bosch',
                'model_name': 'GBH 2-26 DRE',
                'description': 'Perforator profesional pentru găurire și dăltuire. Putere 800 W, energie de impact 2.7 J. Ideal pentru lucrul cu beton, cărămidă și piatră.',
                'price_per_day': 150,
                'specifications': {
                    'Putere': '800 W',
                    'Energie de impact': '2.7 J',
                    'Frecvența loviturilor': '4000 lov/min',
                    'Diametru max. de găurire': '26 mm',
                    'Greutate': '2.7 kg',
                },
            },
            {
                'category': 'Scule electrice',
                'name': 'Șurubelniță Makita DDF453',
                'brand': 'Makita',
                'model_name': 'DDF453',
                'description': 'Șurubelniță cu acumulator litiu-ion 18V. Două trepte de viteză, iluminare LED a zonei de lucru.',
                'price_per_day': 100,
                'specifications': {
                    'Tensiune': '18 V',
                    'Cuplu de strângere': '42 Nm',
                    'Viteză': '0-400/0-1300 rot/min',
                    'Mandrină': '13 mm',
                    'Greutate': '1.7 kg',
                },
            },
            {
                'category': 'Scule electrice',
                'name': 'Polizor unghiular DeWalt DWE4257',
                'brand': 'DeWalt',
                'model_name': 'DWE4257',
                'description': 'Polizor unghiular cu reglare a turației. Potrivit pentru tăierea și polizarea metalului, pietrei, plăcilor ceramice.',
                'price_per_day': 120,
                'specifications': {
                    'Putere': '1500 W',
                    'Diametru disc': '125 mm',
                    'Turație': '2800-10000 rot/min',
                    'Greutate': '2.5 kg',
                },
            },
            {
                'category': 'Scule electrice',
                'name': 'Fierăstrău pendular Bosch GST 150 BCE',
                'brand': 'Bosch',
                'model_name': 'GST 150 BCE',
                'description': 'Fierăstrău pendular profesional pentru tăieri figurate în lemn, metal, plastic. Mișcare pendulară, reglare a vitezei.',
                'price_per_day': 90,
                'specifications': {
                    'Putere': '780 W',
                    'Adâncime de tăiere (lemn)': '150 mm',
                    'Adâncime de tăiere (metal)': '20 mm',
                    'Cursa pânzei': '26 mm',
                },
            },

            # Echipament de construcție
            {
                'category': 'Echipament de construcție',
                'name': 'Betonieră Skiper CM-120',
                'brand': 'Skiper',
                'model_name': 'CM-120',
                'description': 'Betonieră cu capacitate de 120 litri. Ideală pentru lucrări mici de construcție, turnare fundație, prepararea mortarului.',
                'price_per_day': 200,
                'specifications': {
                    'Volum cuvă': '120 l',
                    'Amestec gata preparat': '90 l',
                    'Putere': '550 W',
                    'Tensiune': '220 V',
                    'Greutate': '45 kg',
                },
            },
            {
                'category': 'Echipament de construcție',
                'name': 'Placă vibrantă Wacker Neuson WP1550A',
                'brand': 'Wacker Neuson',
                'model_name': 'WP1550A',
                'description': 'Placă vibrantă pentru compactarea solului, nisipului, pietrișului. Motor pe benzină Honda.',
                'price_per_day': 350,
                'specifications': {
                    'Forță centrifugă': '15 kN',
                    'Dimensiune placă': '500x360 mm',
                    'Motor': 'Honda GX160',
                    'Greutate': '68 kg',
                },
            },
            {
                'category': 'Echipament de construcție',
                'name': 'Generator Fubag BS 6600',
                'brand': 'Fubag',
                'model_name': 'BS 6600',
                'description': 'Generator pe benzină cu putere de 6 kW. Sursă fiabilă de energie electrică pentru șantierul de construcții.',
                'price_per_day': 400,
                'specifications': {
                    'Putere': '6.0 kW',
                    'Tensiune': '220/380 V',
                    'Volum rezervor': '25 l',
                    'Timp de funcționare': '8-10 h',
                    'Greutate': '78 kg',
                },
            },

            # Tehnică de grădină
            {
                'category': 'Tehnică de grădină',
                'name': 'Mașină de tuns iarba Honda HRG 416 SK',
                'brand': 'Honda',
                'model_name': 'HRG 416 SK',
                'description': 'Mașină de tuns iarba autopropulsată pe benzină cu coș de colectare. Lățime de tăiere 41 cm.',
                'price_per_day': 180,
                'specifications': {
                    'Lățime de tăiere': '41 cm',
                    'Înălțime de tăiere': '20-74 mm',
                    'Volum coș': '50 l',
                    'Motor': 'Honda GCV160',
                },
            },
            {
                'category': 'Tehnică de grădină',
                'name': 'Trimmer Stihl FS 55',
                'brand': 'Stihl',
                'model_name': 'FS 55',
                'description': 'Trimmer pe benzină pentru tunderea ierbii în zone greu accesibile. Ușor și manevrabil.',
                'price_per_day': 100,
                'specifications': {
                    'Putere': '1.0 CP',
                    'Capacitate cilindrică': '27.2 cm³',
                    'Lățime de tăiere': '38 cm',
                    'Greutate': '5.0 kg',
                },
            },
            {
                'category': 'Tehnică de grădină',
                'name': 'Motocultor Husqvarna TF 230',
                'brand': 'Husqvarna',
                'model_name': 'TF 230',
                'description': 'Motocultor pe benzină pentru prelucrarea solului. Adâncime de lucru până la 30 cm.',
                'price_per_day': 250,
                'specifications': {
                    'Putere': '4.5 CP',
                    'Lățime de lucru': '60-80 cm',
                    'Adâncime de lucru': '30 cm',
                    'Greutate': '49 kg',
                },
            },

            # Echipament de sudură
            {
                'category': 'Echipament de sudură',
                'name': 'Invertor de sudură Resanta SAI 220',
                'brand': 'Resanta',
                'model_name': 'SAI 220',
                'description': 'Aparat de sudură invertor pentru sudura manuală cu arc electric. Curent până la 220A, lucru cu electrozi până la 5 mm.',
                'price_per_day': 150,
                'specifications': {
                    'Curent de sudură': '10-220 A',
                    'Tensiune': '220 V',
                    'Diametru electrod': '1.6-5.0 mm',
                    'Factor de utilizare': '70%',
                    'Greutate': '4.9 kg',
                },
            },
            {
                'category': 'Echipament de sudură',
                'name': 'Aparat semiautomat Svarog MIG 200',
                'brand': 'Svarog',
                'model_name': 'MIG 200',
                'description': 'Aparat de sudură semiautomat pentru sudare în mediu de gaz protector. Moduri MIG/MAG, MMA.',
                'price_per_day': 250,
                'specifications': {
                    'Curent de sudură MIG': '40-200 A',
                    'Curent de sudură MMA': '20-180 A',
                    'Diametru sârmă': '0.6-1.0 mm',
                    'Greutate': '12.5 kg',
                },
            },

            # Aparate de măsură
            {
                'category': 'Aparate de măsură',
                'name': 'Nivel laser Bosch GLL 3-80',
                'brand': 'Bosch',
                'model_name': 'GLL 3-80',
                'description': 'Nivel laser profesional cu trei planuri 360°. Precizie ±0.2 mm/m.',
                'price_per_day': 200,
                'specifications': {
                    'Număr de linii': '3 x 360°',
                    'Precizie': '±0.2 mm/m',
                    'Rază de acțiune': '30 m (80 m cu receptor)',
                    'Autonivelare': '±4°',
                },
            },
            {
                'category': 'Aparate de măsură',
                'name': 'Telemetru laser Leica DISTO D2',
                'brand': 'Leica',
                'model_name': 'DISTO D2',
                'description': 'Telemetru laser compact cu Bluetooth. Măsurarea distanțelor până la 100 m.',
                'price_per_day': 80,
                'specifications': {
                    'Rază de acțiune': '0.05-100 m',
                    'Precizie': '±1.5 mm',
                    'Bluetooth': 'Da',
                    'Memorie': '10 măsurători',
                },
            },
            {
                'category': 'Aparate de măsură',
                'name': 'Detector de cabluri Bosch GMS 120',
                'brand': 'Bosch',
                'model_name': 'GMS 120',
                'description': 'Detector universal pentru identificarea metalului, cablurilor, structurilor de lemn în pereți.',
                'price_per_day': 50,
                'specifications': {
                    'Adâncime de detectare (oțel)': '120 mm',
                    'Adâncime de detectare (cupru)': '80 mm',
                    'Adâncime de detectare (cabluri)': '50 mm',
                    'Adâncime de detectare (lemn)': '38 mm',
                },
            },

            # Echipament de curățenie
            {
                'category': 'Echipament de curățenie',
                'name': 'Aparat de spălat cu presiune Karcher K5',
                'brand': 'Karcher',
                'model_name': 'K5 Premium',
                'description': 'Aparat de spălat cu presiune puternic pentru automobile, fațade, mobilier de grădină. Presiune până la 145 bar.',
                'price_per_day': 180,
                'specifications': {
                    'Presiune': '20-145 bar',
                    'Debit': '500 l/h',
                    'Putere': '2.1 kW',
                    'Lungime furtun': '8 m',
                },
            },
            {
                'category': 'Echipament de curățenie',
                'name': 'Aspirator industrial Karcher NT 30/1',
                'brand': 'Karcher',
                'model_name': 'NT 30/1 Tact L',
                'description': 'Aspirator profesional pentru curățare uscată și umedă. Volum rezervor 30 l, curățare automată a filtrului.',
                'price_per_day': 150,
                'specifications': {
                    'Volum rezervor': '30 l',
                    'Putere': '1380 W',
                    'Vid': '254 mbar',
                    'Debit de aer': '74 l/s',
                },
            },
            {
                'category': 'Echipament de curățenie',
                'name': 'Mașină de spălat pardoseli Karcher BD 30/4 C',
                'brand': 'Karcher',
                'model_name': 'BD 30/4 C',
                'description': 'Mașină compactă de spălat pardoseli pentru curățarea spațiilor mici. Funcționare pe acumulator.',
                'price_per_day': 300,
                'specifications': {
                    'Productivitate': '630 m²/h',
                    'Lățime perie': '300 mm',
                    'Rezervor apă curată': '4 l',
                    'Timp de funcționare': '25 min',
                },
            },
        ]

        # Creăm sculele
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
                    'specifications': tool_data.get('specifications', {}),
                    'condition': random.choice(['new', 'excellent', 'good']),
                    'availability': 'available',
                    'is_featured': random.choice([True, False, False, False]),  # 25% șansă să fie featured
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'  + {tool.name}')
            else:
                self.stdout.write(f'  = {tool.name} (există deja)')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Gata! Categorii create: {len(categories)}, scule: {created_count}'
        ))
        self.stdout.write('')
        self.stdout.write('Notă: Imaginile nu au fost adăugate.')
        self.stdout.write('Adăugați imaginile prin panoul de admin: /admin/catalog/tool/')
