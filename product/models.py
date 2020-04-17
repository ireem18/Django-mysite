from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
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
    parent =TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE) # models.ForeignKey mtpp den sonra silinir
    """Herbir katagori için ayrı dosya oluşmaz agac mantığı ile oluşur"""
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src = "{}" height ="50"/>'.format(self.image.url))
    image_tag.short_description = 'Images'

class Product(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    detail = RichTextUploadingField()
    slug = models.SlugField(blank=True, max_length=150)
    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src = "{}" height ="50"/>'.format(self.image.url))
    image_tag.short_description = 'Images'

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True) #Blank bos gecmemize izin verir
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title #sayfada hangi ismi döndürmek istiyorsak

    def image_tag(self):
        return mark_safe('<img src = "{}" height ="50"/>'.format(self.image.url))
    image_tag.short_description = 'Images'


class Comment(models.Model):
    STATUS = (
        ('New','Yeni'),
        ('True','Evet'),
        ('False','Hayır'),
    )
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=200,blank=True)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate'] #htmlden hangi alanlar çagrılack ise o yazılır