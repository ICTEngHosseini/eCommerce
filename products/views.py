from django.shortcuts import render, Http404, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin


# Classbase Views (New)
class ProductFeaturedListView(ListView):
    template_name = "products/products.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    # queryset = Product.objects.all()
    template_name = "products/featured-detail.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/products.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Product, slug=slug)
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExit:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Uhhhmmm... :/")

        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return instance


class ProductDetailView(ObjectViewedMixin, DetailView):
    template_name = "products/detail.html"

    # def get_context_data(self, *args, **kwargs):
    #    return super(ProductListView, self).get_context_data(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Ops..Products not founds!")
        return instance