from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.access import get_accessible_maintenance
from .filters import MaintenanceFilter
from .forms import (
    MaintenanceForm,
    MaintenanceOrganizationForm,
    MaintenanceTypeForm,
)
from .models import (
    Maintenance,
    MaintenanceOrganization,
    MaintenanceType,
)


class MaintenanceList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Maintenance
    template_name = 'service/maintenance_list.html'
    context_object_name = 'maintenance_records'
    permission_required = 'service.view_maintenance'

    def get_queryset(self):
        queryset = (
            get_accessible_maintenance(self.request.user)
            .select_related(
                'maintenance_type',
                'organization',
                'machine',
                'service_company',
            )
            .order_by('maintenance_date')
        )

        self.filterset = MaintenanceFilter(
            self.request.GET,
            queryset=queryset,
        )

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['can_add_maintenance'] = self.request.user.has_perm(
            'service.add_maintenance'
        )
        context['can_change_maintenance'] = self.request.user.has_perm(
            'service.change_maintenance'
        )
        return context


class MaintenanceCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'service/maintenance_form.html'
    success_url = reverse_lazy('service:list')
    permission_required = 'service.add_maintenance'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MaintenanceUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'service/maintenance_form.html'
    success_url = reverse_lazy('service:list')
    permission_required = 'service.change_maintenance'

    def get_queryset(self):
        return get_accessible_maintenance(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MaintenanceDetail(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = Maintenance
    template_name = 'service/maintenance_detail.html'
    context_object_name = 'maintenance'
    permission_required = 'service.view_maintenance'

    def get_queryset(self):
        return (
            get_accessible_maintenance(self.request.user)
            .select_related(
                'maintenance_type',
                'organization',
                'machine',
                'service_company',
            )
        )


class MaintenanceTypeList(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = MaintenanceType
    template_name = 'service/maintenance_type_list.html'
    context_object_name = 'maintenance_types'
    permission_required = 'service.view_maintenancetype'
    ordering = 'name'


class MaintenanceTypeCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = MaintenanceType
    form_class = MaintenanceTypeForm
    template_name = 'service/maintenance_type_form.html'
    success_url = reverse_lazy('service:maintenance_type_list')
    permission_required = 'service.add_maintenancetype'


class MaintenanceTypeUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = MaintenanceType
    form_class = MaintenanceTypeForm
    template_name = 'service/maintenance_type_form.html'
    success_url = reverse_lazy('service:maintenance_type_list')
    permission_required = 'service.change_maintenancetype'


class MaintenanceOrganizationList(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = MaintenanceOrganization
    template_name = 'service/maintenance_organization_list.html'
    context_object_name = 'maintenance_organizations'
    permission_required = 'service.view_maintenanceorganization'
    ordering = 'name'


class MaintenanceOrganizationCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = MaintenanceOrganization
    form_class = MaintenanceOrganizationForm
    template_name = 'service/maintenance_organization_form.html'
    success_url = reverse_lazy('service:maintenance_organization_list')
    permission_required = 'service.add_maintenanceorganization'


class MaintenanceOrganizationUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = MaintenanceOrganization
    form_class = MaintenanceOrganizationForm
    template_name = 'service/maintenance_organization_form.html'
    success_url = reverse_lazy('service:maintenance_organization_list')
    permission_required = 'service.change_maintenanceorganization'
