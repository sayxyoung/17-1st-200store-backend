import json

from django.http  import JsonResponse
from django.views import Views

from 

class OrderListView(View):
    def get(self, request):
        pass
    
    def post(self, request):
        data = json.loads(request.body)