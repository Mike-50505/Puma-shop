from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import Http404
from .forms import ProductoForm
from .carrito import Carrito
from .models import Producto
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegistroForm, LoginForm
from django.views.generic import TemplateView
from .models import Banner, Producto
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q

def index(request):
    banners_activos = Banner.objects.filter(activo=True).order_by('orden')
    productos = list(Producto.objects.all())
    productos_aleatorios = random.sample(productos, min(3, len(productos)))
    return render(request, 'store/index.html', {
        'banners': banners_activos,
        'productos_aleatorios': productos_aleatorios
    })

def shop_view(request):
    productos = Producto.objects.all()  # ← Elimina select_related
    return render(request, 'store/shop.html', {'productos': productos})

def ofertas_view(request):
    productos_oferta = Producto.objects.filter(oferta=True)
    return render(request, 'store/ofertas.html', {'productos': productos_oferta})

class CustomLoginView(LoginView):
    template_name = 'store/login.html'

@permission_required('store.add_producto')
@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop')
    else:
        form = ProductoForm()
    return render(request, 'store/agregar_producto.html', {'form': form})

def detalle_producto(request, producto_id=None, slug=None):
    if producto_id:
        producto = get_object_or_404(Producto, id=producto_id)
    elif slug:
        producto = get_object_or_404(Producto, slug=slug)
    else:
        raise Http404("Producto no encontrado")
    
    return render(request, 'store/detalle_producto.html', {'producto': producto})

def agregar_al_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.agregar(producto)
    return redirect('ver_carrito')

def remover_del_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.remover(producto)
    return redirect('ver_carrito')

def actualizar_carrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad'))
        carrito = Carrito(request)
        producto = get_object_or_404(Producto, id=producto_id)
        carrito.actualizar(producto, cantidad)
    return redirect('ver_carrito')

def ver_carrito(request):
    return render(request, 'store/carrito.html')

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'store/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def categoria_view(request, categoria):
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'store/categoria.html', {
        'productos': productos,
        'categoria_actual': dict(Producto.CATEGORIAS).get(categoria, categoria)
    })

class ContactoView(TemplateView):
    template_name = 'store/contacto.html'
    
def buscar_productos(request):
    query = request.GET.get('q')
    resultados = Producto.objects.filter(
        Q(nombre__icontains=query) | 
        Q(descripcion__icontains=query)
    )
    return render(request, 'store/busqueda.html', {'resultados': resultados})