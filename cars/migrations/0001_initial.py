# Generated by Django 4.1 on 2022-09-20 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_remove_account_dob_remove_account_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('code_registration', models.CharField(blank=True, max_length=20, null=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('brand', models.CharField(max_length=150)),
                ('model', models.CharField(max_length=150)),
                ('price', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('creator', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos')),
                ('speed', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField()),
                ('date_of_entry', models.DateTimeField(auto_now_add=True)),
                ('on_the_way', models.BooleanField(default=False)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('to_the_location', models.CharField(blank=True, max_length=255, null=True)),
                ('come_back', models.BooleanField(default=False)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Cars_ARC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_car', models.CharField(max_length=5)),
                ('id_location', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=100)),
                ('code_registration', models.CharField(max_length=20)),
                ('creator_ARC', models.CharField(max_length=255)),
                ('change_date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=255)),
                ('on_the_way', models.BooleanField(default=False)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('to_the_location', models.CharField(blank=True, max_length=255, null=True)),
                ('come_back', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=100)),
                ('GST_number', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=150, null=True, unique=True)),
                ('mobile', models.CharField(max_length=10, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='vendors')),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to='accounts.account')),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Cars_Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=255)),
                ('client_document_type', models.CharField(blank=True, max_length=50, null=True)),
                ('client_document_identification', models.CharField(blank=True, max_length=50, null=True)),
                ('client_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('client_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('date_from', models.DateTimeField(blank=True, null=True)),
                ('date_to', models.DateTimeField(blank=True, null=True)),
                ('note', models.CharField(blank=True, max_length=1024, null=True)),
                ('date_of_entry', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('creator', models.CharField(max_length=255)),
                ('date_of_change', models.DateTimeField(blank=True, null=True)),
                ('creator_change', models.CharField(blank=True, max_length=64, null=True)),
                ('type_change', models.CharField(blank=True, max_length=64, null=True)),
                ('id_arc', models.CharField(blank=True, max_length=64, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
                ('id_cars', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carReservations', to='cars.car')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locationReservations', to='cars.location')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.dealer')),
            ],
        ),
        migrations.CreateModel(
            name='Cars_Rents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=255)),
                ('client_document_type', models.CharField(blank=True, max_length=50, null=True)),
                ('client_document_identification', models.CharField(blank=True, max_length=50, null=True)),
                ('client_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('client_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('date_from', models.DateTimeField(auto_now_add=True)),
                ('date_to', models.DateTimeField(blank=True, null=True)),
                ('deposit', models.CharField(max_length=255)),
                ('deposit_currency', models.CharField(max_length=255)),
                ('deposit_is_active', models.BooleanField(default=False)),
                ('total_price', models.CharField(max_length=255)),
                ('total_price_currency', models.CharField(max_length=255)),
                ('total_price_is_paid', models.BooleanField(default=False)),
                ('creator', models.CharField(max_length=255)),
                ('date_of_entry', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('note', models.CharField(blank=True, max_length=1024, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
                ('id_cars', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carRents', to='cars.car')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locationRents', to='cars.location')),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='main_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tracks', to='cars.location'),
        ),
        migrations.AddField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='cars.dealer'),
        ),
    ]
