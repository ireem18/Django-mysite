from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe


class Category(models.Model):
    """Tablo oluşturmak ve adminde gösterim olsun diye"""
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
    )
    title = models.CharField(max_length=30)
    """ CharField = Alantürü"""
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    """resim türünden dosya eklenecek ise"""
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    """metinsel bir şey ile çağırmak istiyorsak slug"""
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    """Herbir katagori için ayrı dosya oluşmaz agac mantığı ile oluşur"""
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Product(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    #
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    detail = models.TextField ()
    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src = "{}" height ="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True) #Blank bos gecmemize izin verir
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title #sayfada hangi ismi döndürmek istiyorsak

    def image_tag(self):
        return mark_safe('<img src = "{}" height ="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'