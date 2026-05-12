from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0005_add_delivery'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentalrequest',
            name='deposit_amount',
        ),
    ]
