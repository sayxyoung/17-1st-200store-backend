from django.urls  import path
#from product.view import ProductView

from .views import MainView

urlpatterns = [
    path('', MainView.as_view())
#        path('product', ProductView.as_view()),
]