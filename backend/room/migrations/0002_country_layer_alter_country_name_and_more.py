# Generated by Django 4.1.6 on 2023-04-24 20:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='layer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='player', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='outcome',
            name='validation',
            field=models.CharField(choices=[('MYBE', 'Order Not Evaluated'), ('MARK', 'Order Marked for future Evaluation'), ('NCVY', 'Move Order has No Convoy'), ('PASS', 'Order Passed'), ('VOID', 'Order Failed'), ('CUT', 'Order Cut'), ('BNCE', 'Order Bounced with another'), ('DLGE', 'Order Unit Dislodged'), ('DRPT', 'Convoy Order Distrupted'), ('DBAN', 'Order Unit needs to Disband')], default='MYBE', max_length=4),
        ),
    ]