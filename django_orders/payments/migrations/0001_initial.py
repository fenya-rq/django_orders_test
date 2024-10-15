# Generated by Django 5.1.2 on 2024-10-15 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=25, verbose_name='Сумма')),
                ('status', models.CharField(choices=[('pending', 'В процессе'), ('completed', 'Выполнен успешно'), ('failed', 'Платеж не прошел'), ('voided', 'Voided')], default='pending', max_length=10, verbose_name='Статус')),
                ('payment_type', models.CharField(choices=[('Credit Card', 'Credit Card'), ('PayPal', 'PayPal'), ('Bank Transfer', 'Bank Transfer')], max_length=25, verbose_name='Тип оплаты')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payment', to='orders.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
    ]
