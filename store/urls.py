from django.urls import path
from . import views
from .views import ContactoView

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop_view, name='shop'),
    path('ofertas/', views.ofertas_view, name='ofertas'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    
    # Ambas opciones para compatibilidad
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto_id'),
    path('producto/<slug:slug>/', views.detalle_producto, name='detalle_producto_slug'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('remover/<int:producto_id>/', views.remover_del_carrito, name='remover_del_carrito'),
    path('actualizar/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contacto/', ContactoView.as_view(), name='contacto'),
    path('categoria/<str:categoria>/', views.categoria_view, name='categoria'),
]