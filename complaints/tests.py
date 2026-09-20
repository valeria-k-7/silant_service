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

from .forms import ComplaintForm
from .models import Complaint, FailureNode, RecoveryMethod


class ComplaintAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        client_group = Group.objects.create(name='client')
        service_group = Group.objects.create(name='service')
        manager_group = Group.objects.create(name='manager')

        view_permission = Permission.objects.get(
            content_type__app_label='complaints',
            codename='view_complaint',
        )
        change_permission = Permission.objects.get(
            content_type__app_label='complaints',
            codename='change_complaint',
        )

        client_group.permissions.add(view_permission)
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

        cls.failure_node = FailureNode.objects.create(
            name='Test failure node',
            description='Test failure node description',
        )
        cls.recovery_method = RecoveryMethod.objects.create(
            name='Test recovery method',
            description='Test recovery method description',
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

        cls.readonly_complaint = cls.create_complaint(
            cls.client_machine,
        )
        cls.editable_complaint = cls.create_complaint(
            cls.service_machine,
        )
        cls.foreign_complaint = cls.create_complaint(
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
    def create_complaint(cls, machine):
        return Complaint.objects.create(
            failure_date=date(2026, 1, 1),
            operating_time=100,
            failure_node=cls.failure_node,
            failure_description='Test failure',
            recovery_method=cls.recovery_method,
            spare_parts='Test part',
            recovery_date=date(2026, 1, 6),
            machine=machine,
            service_company=machine.service_company,
        )

    def test_guest_is_redirected_from_detail(self):
        url = reverse(
            'complaints:detail',
            args=[self.editable_complaint.pk],
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_double_role_reads_both_scopes(self):
        self.client.force_login(self.double_user)

        editable_response = self.client.get(
            reverse(
                'complaints:detail',
                args=[self.editable_complaint.pk],
            )
        )
        readonly_response = self.client.get(
            reverse(
                'complaints:detail',
                args=[self.readonly_complaint.pk],
            )
        )
        foreign_response = self.client.get(
            reverse(
                'complaints:detail',
                args=[self.foreign_complaint.pk],
            )
        )

        self.assertEqual(editable_response.status_code, 200)
        self.assertEqual(readonly_response.status_code, 200)
        self.assertEqual(foreign_response.status_code, 404)

    def test_double_role_edit_link_uses_service_scope(self):
        self.client.force_login(self.double_user)

        editable_response = self.client.get(
            reverse(
                'complaints:detail',
                args=[self.editable_complaint.pk],
            )
        )
        readonly_response = self.client.get(
            reverse(
                'complaints:detail',
                args=[self.readonly_complaint.pk],
            )
        )

        editable_url = reverse(
            'complaints:update',
            args=[self.editable_complaint.pk],
        )
        readonly_url = reverse(
            'complaints:update',
            args=[self.readonly_complaint.pk],
        )

        self.assertContains(editable_response, editable_url)
        self.assertNotContains(readonly_response, readonly_url)

    def test_double_role_update_scope(self):
        self.client.force_login(self.double_user)

        editable_response = self.client.get(
            reverse(
                'complaints:update',
                args=[self.editable_complaint.pk],
            )
        )
        readonly_response = self.client.get(
            reverse(
                'complaints:update',
                args=[self.readonly_complaint.pk],
            )
        )

        self.assertEqual(editable_response.status_code, 200)
        self.assertEqual(readonly_response.status_code, 404)

    def test_manager_can_access_foreign_complaint(self):
        self.client.force_login(self.manager)

        detail_response = self.client.get(
            reverse(
                'complaints:detail',
                args=[self.foreign_complaint.pk],
            )
        )
        update_response = self.client.get(
            reverse(
                'complaints:update',
                args=[self.foreign_complaint.pk],
            )
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(update_response.status_code, 200)

    def test_downtime_is_calculated(self):
        self.editable_complaint.refresh_from_db()

        self.assertEqual(
            self.editable_complaint.downtime,
            5,
        )

    def test_complaint_form_uses_date_widgets(self):
        form = ComplaintForm()

        self.assertEqual(
            form.fields['failure_date'].widget.input_type,
            'date',
        )
        self.assertEqual(
            form.fields['recovery_date'].widget.input_type,
            'date',
        )
