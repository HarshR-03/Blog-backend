from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class helloWorldView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        return JsonResponse({"message":"hello world"})
