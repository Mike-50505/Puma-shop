from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.text import slugify
from django.urls import reverse

class Producto(models.Model):
    CATEGORIAS = [
        ('CAMISETAS', 'Camisetas'),
        ('SUDADERAS', 'Sudaderas'),
        ('ACCESORIOS', 'Accesorios'),
    ]
    
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre del producto",
        help_text="Ingrese el nombre del producto (máx. 100 caracteres)"
    )
    
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del producto",
        blank=True,
        null=True
    )
    
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIAS,
        verbose_name="Categoría",
        help_text="Ej: Camisetas, Sudaderas, Accesorios"
    )
    
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio normal"
    )
    
    imagen = models.ImageField(
        upload_to='productos/%Y/%m/%d/',
        verbose_name="Imagen del producto",
        blank=True, 
        null=True,
        help_text="Suba una imagen atractiva del producto"
    )
    
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Cantidad en inventario"
    )
    
    oferta = models.BooleanField(
        default=False,
        verbose_name="¿Está en oferta?"
    )
    
    precio_oferta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Precio promocional"
    )
    
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="URL amigable",
        help_text="Se genera automáticamente"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    
    ultima_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['nombre', 'categoria']),
            models.Index(fields=['slug'], name='slug_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            self.slug = base_slug
            counter = 1
            while Producto.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('detalle_producto', kwargs={'slug': self.slug})
    
    def __str__(self):
        return f"{self.nombre} (ID: {self.id})"

    @property
    def en_oferta(self):
        """Devuelve True si el producto tiene oferta válida"""
        return self.oferta and self.precio_oferta is not None and self.precio_oferta < self.precio
    
    @property
    def precio_actual(self):
        return self.precio_oferta if self.oferta else self.precio

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('correo electrónico', unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
class Banner(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título del Banner")
    imagen = models.ImageField(
        upload_to='banners/',
        verbose_name="Imagen (1920x1080 px)",
        help_text="Usa imágenes en formato HD (16:9)"
    )
    url_destino = models.URLField(
        verbose_name="URL al hacer clic",
        blank=True,
        help_text="Ej: /ofertas/ o https://tudominio.com/promocion"
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden de visualización"
    )
    activo = models.BooleanField(default=True, verbose_name="¿Activo?")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['orden']

    def __str__(self):
        return self.titulo