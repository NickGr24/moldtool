# MoldTool

Platformă online pentru închirierea de scule și unelte profesionale în Republica Moldova. Permite vizitatorilor să răsfoiască catalogul, să rezerve unelte pe perioade alese de ei și să primească pe email contractul împreună cu factura proformă în format PDF.

## Funcționalități

- **Catalog de unelte** structurat pe categorii, cu pagină de detaliu, sistem de favorite și comparator.
- **Cerere de închiriere** atât pentru utilizatori autentificați, cât și pentru vizitatori (date de contact preluate din profil sau introduse manual).
- **Calcul automat al costurilor** pe baza intervalului `start_date` – `end_date`, cu garanție returnabilă, livrare opțională (ridicare gratuită din depozit sau livrare la adresă cu tarif fix de 200 MDL) și total final inclus în `total_price`.
- **Generare PDF** pentru contractul de închiriere și factura proformă (WeasyPrint), atașate la emailul de confirmare.
- **Notificări prin email**:
  - confirmarea cererii imediat după creare,
  - mementou automat cu 2 ore înainte de expirarea închirierii (`end_date`), trimis printr-o comandă programată.
- **Panou administrativ Django** pentru gestionarea cererilor (confirmare, anulare, respingere, marcarea ca livrată / returnată).
- **Cabinet personal** (dashboard) cu istoricul cererilor, favorite și editare profil.
- **Autentificare** prin email + parolă (django-allauth) și opțional Google OAuth.
- **Multilingv**: română (limbă principală) și rusă, configurate prin sistemul Django i18n (`locale/ro`, `locale/ru`).

## Stack tehnologic

- **Python 3.11+**, **Django 5.x**
- **django-allauth** pentru autentificare
- **WeasyPrint** pentru generarea documentelor PDF
- **APScheduler** pentru planificator de fundal (memento email)
- **Pillow** pentru procesarea imaginilor
- **SQLite** în dezvoltare, **PostgreSQL** recomandat în producție
- **Gunicorn** ca server WSGI în producție

## Aplicații Django

| Aplicație   | Responsabilitate                                                  |
|-------------|-------------------------------------------------------------------|
| `core`      | Pagini statice (despre, contacte, termeni, politica), tablou administrativ și context global. |
| `accounts`  | Modelul utilizatorului, formulare de autentificare și înregistrare. |
| `catalog`   | Categoriile, sculele, paginile de detaliu, favorite și comparator. |
| `rentals`   | Cererile de închiriere, calculul prețului, contractele PDF, mementouri prin email. |
| `dashboard` | Cabinetul personal al clientului.                                 |
| `config`    | Setările proiectului, URL-ul principal și WSGI/ASGI.              |

## Instalare locală

```bash
# 1. Clonează depozitul
git clone https://github.com/Chom333/moldtool.git
cd moldtool

# 2. Creează și activează mediul virtual
python3 -m venv venv
source venv/bin/activate  # pe Windows: venv\Scripts\activate

# 3. Instalează dependențele
pip install -r requirements.txt

# 4. Aplică migrările
python manage.py migrate

# 5. Creează un superutilizator pentru panoul de administrare
python manage.py createsuperuser

# 6. Pornește serverul de dezvoltare
python manage.py runserver
```

Aplicația va fi disponibilă la `http://127.0.0.1:8000/`, iar panoul administrativ la `/admin/`.

## Variabile de mediu

Configurabile direct sau printr-un fișier `.env` (încărcat prin `python-dotenv`):

| Variabilă | Implicit | Descriere |
|-----------|----------|-----------|
| `DJANGO_SECRET_KEY` | cheie de dezvoltare | Cheia secretă Django pentru producție. |
| `DJANGO_DEBUG` | `True` | Activează modul debug. În producție: `False`. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Listă separată prin virgulă cu gazdele permise. |
| `EMAIL_HOST` / `EMAIL_PORT` / `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | — | Setări SMTP pentru trimiterea emailurilor de confirmare și a mementourilor. |

## Comenzi de management

```bash
# Trimite mementouri pentru închirierile care expiră în următoarele 2 ore.
# Este apelată automat de APScheduler la pornirea aplicației și poate fi rulată și manual / din cron.
python manage.py send_rental_reminders

# Populează catalogul cu date de test (categorii și unelte).
python manage.py create_test_data
```

## Internaționalizare

Limbile suportate sunt definite în `config/settings.py`. Fișierele de traducere se află în `locale/<cod>/LC_MESSAGES/django.po`.

```bash
# Generează / actualizează fișierele de traducere
python manage.py makemessages -l ro
python manage.py makemessages -l ru

# Compilează traducerile în .mo
python manage.py compilemessages
```

## Structura proiectului

```
moldtool/
├── accounts/        # autentificare și profil
├── catalog/         # catalog scule și categorii
├── config/          # setări Django, URL-uri, WSGI
├── core/            # pagini statice și context global
├── dashboard/       # cabinetul utilizatorului
├── rentals/         # cereri de închiriere, contracte PDF, mementouri
├── locale/          # traduceri (ro, ru)
├── media/           # imagini încărcate
├── static/          # CSS, JS, imagini ale temei
├── templates/       # șabloane HTML
├── manage.py
└── requirements.txt
```

## Licență

Acest proiect este proprietatea autorilor săi. Toate drepturile rezervate.
