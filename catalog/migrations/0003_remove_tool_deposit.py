from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_faq_favorite_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tool',
            name='deposit',
        ),
    ]
