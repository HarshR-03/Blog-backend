from django.urls import path
import api.views as v
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("",v.helloWorldView.as_view(),name="hello-world"),
    path("api-token-auth/", obtain_auth_token, name='api_token_auth'),
    path("signup/",v.signUpView.as_view(),name="signup"),
    path("login/",v.userLoginView.as_view(),name='login'),
    path("blogs/",v.viewAndCreatePosts.as_view()),
    path("blogs/<int:pk>/",v.viewAndCreatePosts.as_view()),
    path("update/<int:pk>/",v.updatePostView.as_view()),
    path("delete/<int:pk>/",v.deletePostView.as_view()),
]