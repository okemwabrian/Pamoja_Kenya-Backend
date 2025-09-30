from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role_display', 'get_membership_status_display', 'is_active', 'created_at')
    list_filter = ('role', 'membership_status', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    date_hierarchy = 'created_at'
    
    actions = ['activate_users', 'deactivate_users', 'make_active_members']
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users activated successfully.')
    activate_users.short_description = 'Activate selected users'
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users deactivated successfully.')
    deactivate_users.short_description = 'Deactivate selected users'
    
    def make_active_members(self, request, queryset):
        updated = queryset.update(membership_status='active')
        self.message_user(request, f'{updated} users set to active membership.')
    make_active_members.short_description = 'Set selected users as active members'
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'address', 'city', 'state', 'zip_code', 'membership_status')
        }),
        ('Important Dates', {
            'fields': ('created_at',)
        }),
    )
    
    readonly_fields = BaseUserAdmin.readonly_fields + ('created_at',)
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2'),
        }),
        ('Additional Info', {
            'fields': ('role',)
        }),
    )