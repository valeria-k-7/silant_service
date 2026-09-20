from datetime import date

from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse

from machines.models import (
    DriveAxleModel,
    EngineModel,
    Machine,
    SteeringAxleModel,
    TechniqueModel,
    TransmissionModel,
)

from .forms import MaintenanceForm
from .models import Maintenance, MaintenanceOrganization, MaintenanceType


class MaintenanceAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        client_group = Group.objects.create(name='client')
        service_group = Group.objects.create(name='service')
        manager_group = Group.objects.create(name='manager')

        view_permission = Permission.objects.get(
            content_type__app_label='service',
            codename='view_maintenance',
        )
        change_permission = Permission.objects.get(
            content_type__app_label='service',
            codename='change_maintenance',
        )

        client_group.permissions.add(
            view_permission,
            change_permission,
        )
        service_group.permissions.add(
            view_permission,
            change_permission,
        )
        manager_group.permissions.add(
            view_permission,
            change_permission,
        )

        cls.double_user = User.objects.create_user(
            username='double_user',
        )
        cls.other_client = User.objects.create_user(
            username='other_client',
        )
        cls.other_service = User.objects.create_user(
            username='other_service',
        )
        cls.manager = User.objects.create_user(
            username='manager_test',
        )

        cls.double_user.groups.add(
            client_group,
            service_group,
        )
        cls.other_client.groups.add(client_group)
        cls.other_service.groups.add(service_group)
        cls.manager.groups.add(manager_group)

        cls.technique = TechniqueModel.objects.create(
            name='Test technique',
            description='Test technique description',
        )
        cls.engine = EngineModel.objects.create(
            name='Test engine',
            description='Test engine description',
        )
        cls.transmission = TransmissionModel.objects.create(
            name='Test transmission',
            description='Test transmission description',
        )
        cls.drive_axle = DriveAxleModel.objects.create(
            name='Test drive axle',
            description='Test drive axle description',
        )
        cls.steering_axle = SteeringAxleModel.objects.create(
            name='Test steering axle',
            description='Test steering axle description',
        )

        cls.maintenance_type = MaintenanceType.objects.create(
            name='Test maintenance type',
            description='Test maintenance type description',
        )
        cls.organization = MaintenanceOrganization.objects.create(
            name='Test organization',
            description='Test organization description',
        )

        cls.client_machine = cls.create_machine(
            factory_number='TEST-C',
            client=cls.double_user,
            service_company=cls.other_service,
        )
        cls.service_machine = cls.create_machine(
            factory_number='TEST-S',
            client=cls.other_client,
            service_company=cls.double_user,
        )
        cls.foreign_machine = cls.create_machine(
            factory_number='TEST-F',
            client=cls.other_client,
            service_company=cls.other_service,
        )

        cls.client_maintenance = cls.create_maintenance(
            cls.client_machine,
        )
        cls.service_maintenance = cls.create_maintenance(
            cls.service_machine,
        )
        cls.foreign_maintenance = cls.create_maintenance(
            cls.foreign_machine,
        )

    @classmethod
    def create_machine(
        cls,
        factory_number,
        client,
        service_company,
    ):
        return Machine.objects.create(
            factory_number=factory_number,
            technique_model=cls.technique,
            engine_model=cls.engine,
            engine_factory_number=f'ENG-{factory_number}',
            transmission_model=cls.transmission,
            transmission_factory_number=f'TR-{factory_number}',
            drive_axle_model=cls.drive_axle,
            drive_axle_factory_number=f'DR-{factory_number}',
            steering_axle_model=cls.steering_axle,
            steering_axle_factory_number=f'ST-{factory_number}',
            supply_contract=f'Contract {factory_number}',
            shipment_date=date(2026, 1, 1),
            consignee=f'Consignee {factory_number}',
            delivery_address=f'Address {factory_number}',
            equipment='Standard',
            client=client,
            service_company=service_company,
        )

    @classmethod
    def create_maintenance(cls, machine):
        return Maintenance.objects.create(
            maintenance_type=cls.maintenance_type,
            maintenance_date=date(2026, 1, 10),
            operating_time=100,
            work_order_number=f'WO-{machine.factory_number}',
            work_order_date=date(2026, 1, 9),
            organization=cls.organization,
            machine=machine,
            service_company=machine.service_company,
        )

    def test_guest_is_redirected_from_detail(self):
        url = reverse(
            'service:detail',
            args=[self.service_maintenance.pk],
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_double_role_reads_client_and_service_scopes(self):
        self.client.force_login(self.double_user)

        client_response = self.client.get(
            reverse(
                'service:detail',
                args=[self.client_maintenance.pk],
            )
        )
        service_response = self.client.get(
            reverse(
                'service:detail',
                args=[self.service_maintenance.pk],
            )
        )
        foreign_response = self.client.get(
            reverse(
                'service:detail',
                args=[self.foreign_maintenance.pk],
            )
        )

        self.assertEqual(client_response.status_code, 200)
        self.assertEqual(service_response.status_code, 200)
        self.assertEqual(foreign_response.status_code, 404)

    def test_double_role_can_update_both_accessible_scopes(self):
        self.client.force_login(self.double_user)

        client_response = self.client.get(
            reverse(
                'service:update',
                args=[self.client_maintenance.pk],
            )
        )
        service_response = self.client.get(
            reverse(
                'service:update',
                args=[self.service_maintenance.pk],
            )
        )
        foreign_response = self.client.get(
            reverse(
                'service:update',
                args=[self.foreign_maintenance.pk],
            )
        )

        self.assertEqual(client_response.status_code, 200)
        self.assertEqual(service_response.status_code, 200)
        self.assertEqual(foreign_response.status_code, 404)

    def test_manager_can_access_foreign_maintenance(self):
        self.client.force_login(self.manager)

        detail_response = self.client.get(
            reverse(
                'service:detail',
                args=[self.foreign_maintenance.pk],
            )
        )
        update_response = self.client.get(
            reverse(
                'service:update',
                args=[self.foreign_maintenance.pk],
            )
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(update_response.status_code, 200)

    def test_detail_contains_reference_descriptions(self):
        self.client.force_login(self.manager)

        response = self.client.get(
            reverse(
                'service:detail',
                args=[self.foreign_maintenance.pk],
            )
        )

        self.assertContains(
            response,
            self.maintenance_type.description,
        )
        self.assertContains(
            response,
            self.organization.description,
        )

    def test_maintenance_form_uses_date_widgets(self):
        form = MaintenanceForm()

        self.assertEqual(
            form.fields['maintenance_date'].widget.input_type,
            'date',
        )
        self.assertEqual(
            form.fields['work_order_date'].widget.input_type,
            'date',
        )
