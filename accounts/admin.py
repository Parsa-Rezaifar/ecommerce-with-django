from django.contrib import admin
from . models import User,OtpCode
from . forms import Create_UserForm,Change_UserForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(OtpCode)
class OtpCode(admin.ModelAdmin):
    list_display = ('phone_number','code','create')
class UserFormAdmin(BaseUserAdmin) :

    form = Change_UserForm
    add_form = Create_UserForm

    list_display = ('email','phone_number','full_name','is_admin')
    readonly_fields = ('last_login',)
    list_filter = ('is_admin',)
    fieldsets = (
        ('Main', {'fields':('email', 'phone_number', 'full_name', 'password')}),
        ('Permissions',{'fields': ('is_active', 'is_admin','is_superuser','last_login','groups','user_permissions')}),
    )
    add_fieldsets = (None,{'fields':('phone_number', 'email', 'full_name', 'first_password', 'second_password')}),
    search_fields = ('email','full_name')
    ordering = ('full_name',)
    filter_horizontal = ('groups','user_permissions')

    def get_form(self, request, obj=None, **kwargs) :
        form = super().get_form(request,obj,**kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser :
            form.base_fields['is_superuser'].disabled = True
        return form

admin.site.register(User,UserFormAdmin)