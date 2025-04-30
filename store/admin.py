from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry
from .models import CustomUser, Producto
from .models import Banner

# Producto Admin
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'stock', 'oferta')
    search_fields = ('nombre', 'descripcion', 'categoria')
    list_filter = ('categoria', 'oferta')
    list_editable = ('precio', 'stock', 'oferta')
    ordering = ('-fecha_creacion',)

# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email',)
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# LogEntry Admin personalizado
@admin.register(LogEntry)
class CustomLogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
    list_filter = ['action_time', 'content_type', 'action_flag']
    search_fields = ['user__email', 'object_repr']
    date_hierarchy = 'action_time'
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'orden', 'fecha_creacion')
    list_editable = ('activo', 'orden')  # Editar directamente desde la lista
    search_fields = ('titulo', 'url_destino')
    list_filter = ('activo',)

admin.site.register(Banner, BannerAdmin)