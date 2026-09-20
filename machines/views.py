from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.access import get_accessible_machines
from .forms import (
    DriveAxleModelForm,
    EngineModelForm,
    MachineForm,
    SteeringAxleModelForm,
    TechniqueModelForm,
    TransmissionModelForm,
)
from .models import (
    DriveAxleModel,
    EngineModel,
    Machine,
    SteeringAxleModel,
    TechniqueModel,
    TransmissionModel,
)


def _filter_by_fk_id(queryset, field_name, value):
    if not value:
        return queryset

    try:
        object_id = int(value)
    except (TypeError, ValueError):
        # Invalid filter values should not cause a server error.
        return queryset.none()

    return queryset.filter(
        **{f'{field_name}_id': object_id}
    )


@login_required
@permission_required('machines.view_machine', raise_exception=True)
def machine_list(request):
    machines = (
        get_accessible_machines(request.user)
        .select_related(
            'technique_model',
            'engine_model',
            'transmission_model',
            'drive_axle_model',
            'steering_axle_model',
            'client',
            'service_company',
        )
        .order_by('shipment_date')
    )

    technique_model = request.GET.get('technique_model')
    engine_model = request.GET.get('engine_model')
    transmission_model = request.GET.get('transmission_model')
    drive_axle_model = request.GET.get('drive_axle_model')
    steering_axle_model = request.GET.get('steering_axle_model')

    machines = _filter_by_fk_id(
        machines,
        'technique_model',
        technique_model,
    )
    machines = _filter_by_fk_id(
        machines,
        'engine_model',
        engine_model,
    )
    machines = _filter_by_fk_id(
        machines,
        'transmission_model',
        transmission_model,
    )
    machines = _filter_by_fk_id(
        machines,
        'drive_axle_model',
        drive_axle_model,
    )
    machines = _filter_by_fk_id(
        machines,
        'steering_axle_model',
        steering_axle_model,
    )

    context = {
        'machines': machines,
        'technique_models': TechniqueModel.objects.all(),
        'engine_models': EngineModel.objects.all(),
        'transmission_models': TransmissionModel.objects.all(),
        'drive_axle_models': DriveAxleModel.objects.all(),
        'steering_axle_models': SteeringAxleModel.objects.all(),
        'selected': {
            'technique_model': technique_model,
            'engine_model': engine_model,
            'transmission_model': transmission_model,
            'drive_axle_model': drive_axle_model,
            'steering_axle_model': steering_axle_model,
        },
        'can_add_machine': request.user.has_perm('machines.add_machine'),
        'can_change_machine': request.user.has_perm('machines.change_machine'),
    }

    return render(request, 'machines/machine_list.html', context)


class MachineCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Machine
    form_class = MachineForm
    template_name = 'machines/machine_form.html'
    success_url = reverse_lazy('machines:list')
    permission_required = 'machines.add_machine'


class MachineUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Machine
    form_class = MachineForm
    template_name = 'machines/machine_form.html'
    success_url = reverse_lazy('machines:list')
    permission_required = 'machines.change_machine'


class MachineDetail(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = Machine
    template_name = 'machines/machine_detail.html'
    context_object_name = 'machine'
    permission_required = 'machines.view_machine'

    def get_queryset(self):
        return (
            get_accessible_machines(self.request.user)
            .select_related(
                'technique_model',
                'engine_model',
                'transmission_model',
                'drive_axle_model',
                'steering_axle_model',
                'client',
                'service_company',
            )
        )


class TechniqueModelList(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = TechniqueModel
    template_name = 'machines/technique_model_list.html'
    context_object_name = 'technique_models'
    permission_required = 'machines.view_techniquemodel'
    ordering = 'name'


class TechniqueModelCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = TechniqueModel
    form_class = TechniqueModelForm
    template_name = 'machines/technique_model_form.html'
    success_url = reverse_lazy('machines:technique_model_list')
    permission_required = 'machines.add_techniquemodel'


class TechniqueModelUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = TechniqueModel
    form_class = TechniqueModelForm
    template_name = 'machines/technique_model_form.html'
    success_url = reverse_lazy('machines:technique_model_list')
    permission_required = 'machines.change_techniquemodel'


class EngineModelList(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = EngineModel
    template_name = 'machines/engine_model_list.html'
    context_object_name = 'engine_models'
    permission_required = 'machines.view_enginemodel'
    ordering = 'name'


class EngineModelCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = EngineModel
    form_class = EngineModelForm
    template_name = 'machines/engine_model_form.html'
    success_url = reverse_lazy('machines:engine_model_list')
    permission_required = 'machines.add_enginemodel'


class EngineModelUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = EngineModel
    form_class = EngineModelForm
    template_name = 'machines/engine_model_form.html'
    success_url = reverse_lazy('machines:engine_model_list')
    permission_required = 'machines.change_enginemodel'


class TransmissionModelList(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = TransmissionModel
    template_name = 'machines/transmission_model_list.html'
    context_object_name = 'transmission_models'
    permission_required = 'machines.view_transmissionmodel'
    ordering = 'name'


class TransmissionModelCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = TransmissionModel
    form_class = TransmissionModelForm
    template_name = 'machines/transmission_model_form.html'
    success_url = reverse_lazy('machines:transmission_model_list')
    permission_required = 'machines.add_transmissionmodel'


class TransmissionModelUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = TransmissionModel
    form_class = TransmissionModelForm
    template_name = 'machines/transmission_model_form.html'
    success_url = reverse_lazy('machines:transmission_model_list')
    permission_required = 'machines.change_transmissionmodel'


class DriveAxleModelList(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = DriveAxleModel
    template_name = 'machines/drive_axle_model_list.html'
    context_object_name = 'drive_axle_models'
    permission_required = 'machines.view_driveaxlemodel'
    ordering = 'name'


class DriveAxleModelCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = DriveAxleModel
    form_class = DriveAxleModelForm
    template_name = 'machines/drive_axle_model_form.html'
    success_url = reverse_lazy('machines:drive_axle_model_list')
    permission_required = 'machines.add_driveaxlemodel'


class DriveAxleModelUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = DriveAxleModel
    form_class = DriveAxleModelForm
    template_name = 'machines/drive_axle_model_form.html'
    success_url = reverse_lazy('machines:drive_axle_model_list')
    permission_required = 'machines.change_driveaxlemodel'


class SteeringAxleModelList(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = SteeringAxleModel
    template_name = 'machines/steering_axle_model_list.html'
    context_object_name = 'steering_axle_models'
    permission_required = 'machines.view_steeringaxlemodel'
    ordering = 'name'


class SteeringAxleModelCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = SteeringAxleModel
    form_class = SteeringAxleModelForm
    template_name = 'machines/steering_axle_model_form.html'
    success_url = reverse_lazy('machines:steering_axle_model_list')
    permission_required = 'machines.add_steeringaxlemodel'


class SteeringAxleModelUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = SteeringAxleModel
    form_class = SteeringAxleModelForm
    template_name = 'machines/steering_axle_model_form.html'
    success_url = reverse_lazy('machines:steering_axle_model_list')
    permission_required = 'machines.change_steeringaxlemodel'
