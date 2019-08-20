# Generated by Django 2.2.4 on 2019-08-14 17:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('like', models.IntegerField(blank=True, default=0, null=True)),
                ('unlike', models.IntegerField(blank=True, default=0, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': "Post's",
            },
        ),
    ]