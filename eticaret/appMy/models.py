from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    title = models.CharField(("Kategori"), max_length=50)
    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name=("Kategori"), on_delete=models.CASCADE, null=True, blank=True)
    marka = models.CharField(("Marka"), max_length=50)
    title = models.CharField(("Ürün Adı"), max_length=50)
    text = models.TextField(("Ürün Hakkında"), max_length=1000)
    image = models.FileField(("Ürün Fotografı"), upload_to='', max_length=100)
    date_now = models.DateTimeField(("Tarih"), auto_now_add=True)
    likes = models.FloatField(("Ürün Beğenisi"), default=0)
    price = models.FloatField(("Ürün Fiyatı"), default=0)
    def __str__(self):
        return self.marka
    
class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=("Ürün"), on_delete=models.CASCADE)
    title = models.CharField(("Yorum Başlığı"), max_length=50)
    text = models.TextField(("Yorum"), max_length=1000)
    date_now = models.DateTimeField(("Girilen Zaman"), auto_now_add=True)
    likes = models.FloatField(("Beğeni"),default=0)
    def __str__(self):
        return self.title


class UserProfil(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı Adı"), on_delete=models.CASCADE)
    job = models.CharField(("Meslek"), max_length=50, default='-')
    address = models.CharField(("Adres"), max_length=50, default='-')
    deneyim = models.IntegerField(("Deneyim"),default=0)
    image = models.ImageField(("Profil Resmi"), upload_to='', max_length=None, default='profilresmi.png')
    phone = models.CharField(("Telefon Numarası"), max_length=50)
    web_site = models.URLField(("Web site"), max_length=200, default='-')
    def __str__(self):
        return self.user.username

