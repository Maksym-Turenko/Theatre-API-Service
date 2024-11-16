# Generated by Django 5.1.2 on 2024-10-13 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("theatre", "0005_alter_ticket_reservation"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="ticket",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ticket_reservation",
                to="theatre.ticket",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="reservation",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="ticket_reservation",
                to="theatre.reservation",
            ),
        ),
    ]
