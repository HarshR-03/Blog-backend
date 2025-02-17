from django.urls import path
from api.views import helloWorldView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("",helloWorldView.as_view(),name="hello-world"),
    path("api-token-auth/", obtain_auth_token, name='api_token_auth')
]