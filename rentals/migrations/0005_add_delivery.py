# Generated manually for delivery feature

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0004_add_reminder_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalrequest',
            name='delivery_method',
            field=models.CharField(
                choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')],
                default='pickup',
                max_length=20,
                verbose_name='способ получения',
            ),
        ),
        migrations.AddField(
            model_name='rentalrequest',
            name='delivery_address',
            field=models.CharField(
                blank=True,
                max_length=500,
                verbose_name='адрес доставки',
            ),
        ),
        migrations.AddField(
            model_name='rentalrequest',
            name='delivery_price',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name='стоимость доставки',
            ),
        ),
    ]
