from django.contrib import admin

from .models import Complaint, FailureNode, RecoveryMethod


admin.site.register(FailureNode)
admin.site.register(RecoveryMethod)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    readonly_fields = ('downtime',)
