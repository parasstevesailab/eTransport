from django.db import migrations

def migrate_vehicle_owner_data(apps, schema_editor):
    VehicleOwner = apps.get_model('accounts', 'VehicleOwner')
    for vehicle in VehicleOwner.objects.all():
        vehicle.user_id = vehicle.user.id
        vehicle.save()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0005_alter_vehicleowner_user'),
    ]
    operations = [
        migrations.RunPython(migrate_vehicle_owner_data),
    ]