# Generated by Django 5.2.3 on 2025-07-15 15:50

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twccapp', '0008_companyprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='galleryimage',
            old_name='description',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='galleryimage',
            name='uploaded_at',
        ),
        migrations.RemoveField(
            model_name='galleryimage',
            name='uploaded_by',
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='summary',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='gallery/'),
        ),
    ]
