
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
