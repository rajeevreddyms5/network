# Generated by Django 4.2.3 on 2023-08-22 15:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0008_rename_user_userprofile_user_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userprofile",
            old_name="followers",
            new_name="follows",
        ),
    ]
