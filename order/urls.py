from django.urls  import path

from order.models import MypageMainView

urlpatterns = [
    path('/mypage', MypageMainView.as_view())
]