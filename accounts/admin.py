from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .forms import CustomerUserChangeForm,CustomerUserCreationForm
from .models import CustomerUser

class CustomerUserAdmin(UserAdmin):
    form = CustomerUserChangeForm
    add_form = CustomerUserCreationForm
    ordering = ['email']
    list_display = ['email', 'full_name','is_active','is_staff','created_at','updated_at']
    search_fields = ['email']
    readonly_fields = ['last_login']
    filter_horizontal = ['groups','user_permissions']

    def full_name(self,obj):
        return f'{obj.first_name} {obj.last_name}'

    fieldsets = (
        ('Main', {'fields':('first_name','last_name', 'email','password')}),
        ('permissions',{'fields':('is_active','is_staff','is_superuser','groups','last_login','user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields':('first_name','last_name','email','password1','password2')}),
    )



    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


admin.site.register(CustomerUser,CustomerUserAdmin)