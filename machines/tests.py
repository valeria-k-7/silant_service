from datetime import date

from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse

from .forms import MachineForm
from .models import (
    DriveAxleModel,
    EngineModel,
    Machine,
    SteeringAxleModel,
    TechniqueModel,
    TransmissionModel,
)


class MachineAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        client_group = Group.objects.create(name='client')
        service_group = Group.objects.create(name='service')
        manager_group = Group.objects.create(name='manager')

        view_permission = Permission.objects.get(
            content_type__app_label='machines',
            codename='view_machine',
        )
        add_permission = Permission.objects.get(
            content_type__app_label='machines',
            codename='add_machine',
        )
        change_permission = Permission.objects.get(
            content_type__app_label='machines',
            codename='change_machine',
        )

        client_group.permissions.add(view_permission)
        service_group.permissions.add(view_permission)
        manager_group.permissions.add(
            view_permission,
            add_permission,
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

        cls.client_machine = cls.create_machine(
            factory_number='TEST-C',
            shipment_date=date(2026, 1, 20),
            client=cls.double_user,
            service_company=cls.other_service,
        )
        cls.service_machine = cls.create_machine(
            factory_number='TEST-S',
            shipment_date=date(2026, 1, 10),
            client=cls.other_client,
            service_company=cls.double_user,
        )
        cls.foreign_machine = cls.create_machine(
            factory_number='TEST-F',
            shipment_date=date(2026, 1, 30),
            client=cls.other_client,
            service_company=cls.other_service,
        )

    @classmethod
    def create_machine(
        cls,
        factory_number,
        shipment_date,
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
            shipment_date=shipment_date,
            consignee=f'Consignee {factory_number}',
            delivery_address=f'Address {factory_number}',
            equipment='Standard',
            client=client,
            service_company=service_company,
        )

    def test_guest_is_redirected_from_detail(self):
        url = reverse(
            'machines:detail',
            args=[self.client_machine.pk],
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_double_role_reads_client_and_service_scopes(self):
        self.client.force_login(self.double_user)

        client_response = self.client.get(
            reverse(
                'machines:detail',
                args=[self.client_machine.pk],
            )
        )
        service_response = self.client.get(
            reverse(
                'machines:detail',
                args=[self.service_machine.pk],
            )
        )
        foreign_response = self.client.get(
            reverse(
                'machines:detail',
                args=[self.foreign_machine.pk],
            )
        )

        self.assertEqual(client_response.status_code, 200)
        self.assertEqual(service_response.status_code, 200)
        self.assertEqual(foreign_response.status_code, 404)

    def test_non_manager_cannot_update_machine(self):
        self.client.force_login(self.double_user)

        response = self.client.get(
            reverse(
                'machines:update',
                args=[self.client_machine.pk],
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_manager_can_access_foreign_machine(self):
        self.client.force_login(self.manager)

        detail_response = self.client.get(
            reverse(
                'machines:detail',
                args=[self.foreign_machine.pk],
            )
        )
        update_response = self.client.get(
            reverse(
                'machines:update',
                args=[self.foreign_machine.pk],
            )
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(update_response.status_code, 200)

    def test_detail_contains_reference_descriptions(self):
        self.client.force_login(self.manager)

        response = self.client.get(
            reverse(
                'machines:detail',
                args=[self.foreign_machine.pk],
            )
        )

        descriptions = (
            self.technique.description,
            self.engine.description,
            self.transmission.description,
            self.drive_axle.description,
            self.steering_axle.description,
        )

        for description in descriptions:
            self.assertContains(response, description)

    def test_list_is_sorted_by_shipment_date(self):
        self.client.force_login(self.manager)

        response = self.client.get(
            reverse('machines:list')
        )
        content = response.content.decode()

        service_position = content.index(
            self.service_machine.factory_number
        )
        client_position = content.index(
            self.client_machine.factory_number
        )
        foreign_position = content.index(
            self.foreign_machine.factory_number
        )

        self.assertLess(service_position, client_position)
        self.assertLess(client_position, foreign_position)

    def test_invalid_machine_filter_ids_do_not_cause_server_error(self):
        self.client.force_login(self.manager)

        filter_names = (
            'technique_model',
            'engine_model',
            'transmission_model',
            'drive_axle_model',
            'steering_axle_model',
        )

        for filter_name in filter_names:
            with self.subTest(filter_name=filter_name):
                response = self.client.get(
                    reverse('machines:list'),
                    {filter_name: 'abc'},
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context['machines']),
                    [],
                )

    def test_machine_form_limits_user_choices_by_role(self):
        form = MachineForm()

        client_ids = set(
            form.fields['client']
            .queryset
            .values_list('pk', flat=True)
        )
        service_ids = set(
            form.fields['service_company']
            .queryset
            .values_list('pk', flat=True)
        )

        self.assertSetEqual(
            client_ids,
            {
                self.double_user.pk,
                self.other_client.pk,
            },
        )
        self.assertSetEqual(
            service_ids,
            {
                self.double_user.pk,
                self.other_service.pk,
            },
        )

    def test_machine_form_uses_date_widget(self):
        form = MachineForm()

        self.assertEqual(
            form.fields['shipment_date'].widget.input_type,
            'date',
        )
