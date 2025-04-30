# store/carrito.py
from django.conf import settings
from .models import Producto

class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get(settings.CART_SESSION_ID)
        if not carrito:
            carrito = self.session[settings.CART_SESSION_ID] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad=1):
        producto_id = str(producto.id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                'cantidad': 0,
                'precio': str(producto.precio_actual)
            }
        self.carrito[producto_id]['cantidad'] += cantidad
        self.guardar()

    def remover(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar()

    def actualizar(self, producto, cantidad):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            self.carrito[producto_id]['cantidad'] = cantidad
            self.guardar()

    def guardar(self):
        self.session.modified = True

    def __iter__(self):
        producto_ids = self.carrito.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        carrito = self.carrito.copy()
        
        for producto in productos:
            carrito[str(producto.id)]['producto'] = producto
        
        for item in carrito.values():
            item['precio'] = float(item['precio'])
            item['total'] = item['precio'] * item['cantidad']
            yield item

    def __len__(self):
        return sum(item['cantidad'] for item in self.carrito.values())

    def obtener_total(self):
        return sum(float(item['precio']) * item['cantidad'] for item in self.carrito.values())

    def vaciar(self):
        del self.session[settings.CART_SESSION_ID]
        self.guardar()