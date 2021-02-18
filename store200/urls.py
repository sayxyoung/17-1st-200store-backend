from django.urls import path, include

urlpatterns = [
        path('main', include('product.urls')),
        path('product', include('product.urls')),
]
