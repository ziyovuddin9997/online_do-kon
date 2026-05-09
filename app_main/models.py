from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from phonenumber_field.modelfields import PhoneNumberField

from app_main.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name="Ism", max_length=255)
    last_name = models.CharField(verbose_name="Familiya", max_length=255)
    phone_number = PhoneNumberField(verbose_name="Telefon raqam", null=True, blank=True, unique=True)
    profile_image = models.ImageField(verbose_name="Profil rasmi", upload_to="profiles/", null=True, blank=True)
    address = models.CharField(verbose_name="Yashash manzili", max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(verbose_name="Xodimlik statusi", default=False)
    is_superuser = models.BooleanField(verbose_name="Superadminlik statusi", default=False)
    is_active = models.BooleanField(verbose_name="Profil aktivligi holati", default=True)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class Category(models.Model):
    name = models.CharField(verbose_name="Kategoriya nomi", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Product(models.Model):
    id = models.UUIDField(verbose_name="ID", primary_key=True, unique=True, editable=False, default=uuid4)
    name = models.CharField(verbose_name="Maxsulot nomi", max_length=100)
    price = models.DecimalField(verbose_name="Maxsulot narxi", max_digits=12, decimal_places=2)
    image = models.ImageField(verbose_name="Maxsulot rasmi", upload_to="products/")
    description = models.TextField(verbose_name="Maxsulot ta'rifi", null=True, blank=True)
    in_stock = models.IntegerField(verbose_name="Ombordagi soni", default=1)
    category = models.ForeignKey(verbose_name="Maxsulot kategoriyasi", to=Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Maxsulot'
        verbose_name_plural = 'Maxsulotlar'


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Savatcha maxsuloti"
        verbose_name_plural = "Savatcha maxsulotlari"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.product.name} - {self.count} ta - {self.created.strftime('%d/%m/%Y, %H:%M:%S')}"

    @property
    def total_price(self):
        return self.product.price * self.count


class Transaction(models.Model):
    id = models.UUIDField(verbose_name="ID", primary_key=True, unique=True, editable=False, default=uuid4)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    product_name = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Oldi-berdi"
        verbose_name_plural = "Oldi-berdilar"
        ordering = ['-created', 'amount']
