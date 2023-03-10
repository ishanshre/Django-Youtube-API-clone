# Generated by Django 4.1.5 on 2023-01-09 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('core', '0002_content_uploaded_alter_content_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_subscribed', models.BooleanField(default=False)),
                ('subscribed_date', models.DateTimeField(auto_now_add=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe_to', to='core.channel')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_by', to='accounts.profile')),
            ],
            options={
                'ordering': ['-subscribed_date'],
            },
        ),
        migrations.AddField(
            model_name='channel',
            name='subscribering',
            field=models.ManyToManyField(related_name='subscribers', through='core.Subscription', to='core.channel'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['-subscribed_date'], name='core_subscr_subscri_c823b4_idx'),
        ),
    ]
