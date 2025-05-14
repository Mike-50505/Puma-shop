from .carrito import Carrito
from .models import Producto

def carrito(request):
    return {'carrito': Carrito(request)}

def categorias(request):
    return {
        'categorias': dict(Producto.CATEGORIAS)
    }
