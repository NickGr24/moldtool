from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0002_add_id_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentalrequest',
            name='id_photo',
        ),
    ]
