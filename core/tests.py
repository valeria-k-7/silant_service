from datetime import date

from django.contrib.auth import get_user_model
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


User = get_user_model()


class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_user = User.objects.create_user(
            username='test_client',
            password='testpass123',
        )

        cls.service_user = User.objects.create_user(
            username='test_service',
            password='testpass123',
        )

        technique_model = TechniqueModel.objects.create(
            name='Тестовая техника',
            description='Описание тестовой техники.',
        )

        engine_model = EngineModel.objects.create(
            name='Тестовый двигатель',
            description='Описание тестового двигателя.',
        )

        transmission_model = TransmissionModel.objects.create(
            name='Тестовая трансмиссия',
            description='Описание тестовой трансмиссии.',
        )

        drive_axle_model = DriveAxleModel.objects.create(
            name='Тестовый ведущий мост',
            description='Описание тестового ведущего моста.',
        )

        steering_axle_model = SteeringAxleModel.objects.create(
            name='Тестовый управляемый мост',
            description='Описание тестового управляемого моста.',
        )

        cls.machine = Machine.objects.create(
            factory_number='TEST-001',
            technique_model=technique_model,
            engine_model=engine_model,
            engine_factory_number='ENGINE-001',
            transmission_model=transmission_model,
            transmission_factory_number='TRANSMISSION-001',
            drive_axle_model=drive_axle_model,
            drive_axle_factory_number='DRIVE-001',
            steering_axle_model=steering_axle_model,
            steering_axle_factory_number='STEERING-001',
            supply_contract='Тестовый договор',
            shipment_date=date(2022, 1, 1),
            consignee='Тестовый грузополучатель',
            delivery_address='Тестовый адрес',
            equipment='Тестовая комплектация',
            client=cls.client_user,
            service_company=cls.service_user,
        )

    def test_guest_sees_public_home(self):
        response = self.client.get(reverse('core:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertFalse(response.context['search_performed'])
        self.assertIsNone(response.context['machine'])

    def test_guest_can_find_machine_by_factory_number(self):
        response = self.client.get(
            reverse('core:home'),
            {'factory_number': 'TEST-001'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['search_performed'])

        machine_data = response.context['machine']

        self.assertIsNotNone(machine_data)
        self.assertEqual(
            machine_data['factory_number'],
            'TEST-001',
        )

        self.assertEqual(
            set(machine_data.keys()),
            {
                'factory_number',
                'technique_model',
                'engine_model',
                'engine_factory_number',
                'transmission_model',
                'transmission_factory_number',
                'drive_axle_model',
                'drive_axle_factory_number',
                'steering_axle_model',
                'steering_axle_factory_number',
            },
        )

    def test_guest_gets_empty_result_for_unknown_factory_number(self):
        response = self.client.get(
            reverse('core:home'),
            {'factory_number': 'UNKNOWN'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['search_performed'])
        self.assertIsNone(response.context['machine'])

    def test_authenticated_user_is_redirected_to_machine_list(self):
        self.client.force_login(self.client_user)

        response = self.client.get(reverse('core:home'))

        self.assertRedirects(
            response,
            reverse('machines:list'),
            fetch_redirect_response=False,
        )
