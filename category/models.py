from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True) #The url of the category
    description = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(upload_to='photos/categories', blank=True)# Where to store the category image

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'



    def get_url(self):
        return reverse('products_by_category', args=[self.slug]) #We use the reverse to automatically build the correct url. This comes in handy when we generate urls dynamically

    def __str__(self):  #String representation of the model
        return self.category_name

