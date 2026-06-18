from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auditlog_weatherrequestlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='summary',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='news_images/'),
        ),
    ]
