# Generated by Django 2.2.2 on 2019-07-18 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0004_auto_20190718_1208'),
        ('users', '0005_auto_20190717_2048'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(max_length=10)),
                ('indicator', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_diagnosis', models.TextField(max_length=200)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('remarks', models.TextField(max_length=200)),
                ('booked_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Patient')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.Payment')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookings.SessionStatus')),
            ],
        ),
        migrations.CreateModel(
            name='CancelledSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason_for_cancelling', models.TextField(max_length=100)),
                ('cancelled_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookings.Session')),
            ],
        ),
    ]
