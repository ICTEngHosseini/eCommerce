from django.db import models

# Create your models here.
import random
from django.db.models import Q
from django.db import models
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_slug_generator
from django.urls import reverse


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 9999)
    return "products/{new_filename}/".format(new_filename=new_filename)


class ProductQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tag__title__icontains=query))
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def featured(self):
        return self.get_queryset().filter(featured=True)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)  # Product.object == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().search(query)


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True, null=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    featured = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    image = models.FileField(
        upload_to=upload_image_path,
        null=True,
        blank=True
    )

    objects = ProductManager()

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
