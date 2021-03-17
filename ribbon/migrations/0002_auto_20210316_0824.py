# Generated by Django 3.1.7 on 2021-03-16 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ribbon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('street', models.CharField(blank=True, max_length=200, null=True)),
                ('building', models.CharField(blank=True, max_length=200, null=True)),
                ('house', models.CharField(blank=True, max_length=200, null=True)),
                ('region', models.CharField(blank=True, max_length=200, null=True)),
                ('zip_code', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='ribbon',
            name='quantity',
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ribbon_name', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('order_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ribbon.orderinfo')),
            ],
        ),
    ]
