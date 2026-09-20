from django.contrib import admin
from django.urls import include, path, re_path

from users.views import account_management_disabled


urlpatterns = [
    path('admin/', admin.site.urls),

    # Block account management routes before allauth handles them.
    # Users should not change their own account data or password.
    path(
        'accounts/email/',
        account_management_disabled,
    ),

    re_path(
        r'^accounts/password/',
        account_management_disabled,
    ),

    path('accounts/', include('allauth.urls')),
    path('machines/', include('machines.urls')),
    path('maintenance/', include('service.urls')),
    path('complaints/', include('complaints.urls')),
    path('', include('core.urls')),
]
