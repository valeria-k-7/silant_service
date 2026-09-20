from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render

from machines.models import Machine


def home(request):
    if request.user.is_authenticated:
        return redirect('machines:list')

    factory_number = request.GET.get('factory_number', '').strip()

    machine_data = None
    search_performed = bool(factory_number)

    if search_performed:
        machine = (
            Machine.objects.select_related(
                'technique_model',
                'engine_model',
                'transmission_model',
                'drive_axle_model',
                'steering_axle_model',
            )
            .filter(factory_number=factory_number)
            .first()
        )

        if machine:
            # Guest search is limited to the first 10 machine fields.
            machine_data = {
                'factory_number': machine.factory_number,
                'technique_model': machine.technique_model,
                'engine_model': machine.engine_model,
                'engine_factory_number': machine.engine_factory_number,
                'transmission_model': machine.transmission_model,
                'transmission_factory_number': (
                    machine.transmission_factory_number
                ),
                'drive_axle_model': machine.drive_axle_model,
                'drive_axle_factory_number': (
                    machine.drive_axle_factory_number
                ),
                'steering_axle_model': machine.steering_axle_model,
                'steering_axle_factory_number': (
                    machine.steering_axle_factory_number
                ),
            }

    context = {
        'factory_number': factory_number,
        'machine': machine_data,
        'search_performed': search_performed,
    }

    return render(request, 'core/home.html', context)


@login_required
@permission_required(
    'machines.view_techniquemodel',
    raise_exception=True,
)
def reference_index(request):
    return render(request, 'core/reference_index.html')
