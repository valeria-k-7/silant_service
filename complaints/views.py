from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.access import get_accessible_complaints, get_editable_complaints
from .filters import ComplaintFilter
from .forms import (
    ComplaintForm,
    FailureNodeForm,
    RecoveryMethodForm,
)
from .models import (
    Complaint,
    FailureNode,
    RecoveryMethod,
)


class ComplaintList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Complaint
    template_name = 'complaints/complaint_list.html'
    context_object_name = 'complaints'
    permission_required = 'complaints.view_complaint'

    def get_queryset(self):
        queryset = (
            get_accessible_complaints(self.request.user)
            .select_related(
                'failure_node',
                'recovery_method',
                'machine',
                'service_company',
            )
            .order_by('failure_date')
        )

        self.filterset = ComplaintFilter(
            self.request.GET,
            queryset=queryset,
        )

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        context['can_add_complaint'] = self.request.user.has_perm(
            'complaints.add_complaint'
        )

        context['editable_complaint_ids'] = set(
            get_editable_complaints(self.request.user)
            .values_list('pk', flat=True)
        )

        return context


class ComplaintCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaints/complaint_form.html'
    success_url = reverse_lazy('complaints:list')
    permission_required = 'complaints.add_complaint'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ComplaintUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaints/complaint_form.html'
    success_url = reverse_lazy('complaints:list')
    permission_required = 'complaints.change_complaint'

    def get_queryset(self):
        return get_editable_complaints(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ComplaintDetail(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = Complaint
    template_name = 'complaints/complaint_detail.html'
    context_object_name = 'complaint'
    permission_required = 'complaints.view_complaint'

    def get_queryset(self):
        return (
            get_accessible_complaints(self.request.user)
            .select_related(
                'failure_node',
                'recovery_method',
                'machine',
                'service_company',
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['can_change_complaint'] = (
            self.request.user.has_perm('complaints.change_complaint')
            and get_editable_complaints(self.request.user).filter(
                pk=self.object.pk
            ).exists()
        )

        return context


class FailureNodeList(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = FailureNode
    template_name = 'complaints/failure_node_list.html'
    context_object_name = 'failure_nodes'
    permission_required = 'complaints.view_failurenode'
    ordering = 'name'


class FailureNodeCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = FailureNode
    form_class = FailureNodeForm
    template_name = 'complaints/failure_node_form.html'
    success_url = reverse_lazy('complaints:failure_node_list')
    permission_required = 'complaints.add_failurenode'


class FailureNodeUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = FailureNode
    form_class = FailureNodeForm
    template_name = 'complaints/failure_node_form.html'
    success_url = reverse_lazy('complaints:failure_node_list')
    permission_required = 'complaints.change_failurenode'


class RecoveryMethodList(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = RecoveryMethod
    template_name = 'complaints/recovery_method_list.html'
    context_object_name = 'recovery_methods'
    permission_required = 'complaints.view_recoverymethod'
    ordering = 'name'


class RecoveryMethodCreate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = RecoveryMethod
    form_class = RecoveryMethodForm
    template_name = 'complaints/recovery_method_form.html'
    success_url = reverse_lazy('complaints:recovery_method_list')
    permission_required = 'complaints.add_recoverymethod'


class RecoveryMethodUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = RecoveryMethod
    form_class = RecoveryMethodForm
    template_name = 'complaints/recovery_method_form.html'
    success_url = reverse_lazy('complaints:recovery_method_list')
    permission_required = 'complaints.change_recoverymethod'
