from django.http import HttpResponse,JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from .serializers import UserSerializer, PostListSerializer, PostDetailSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Post
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser 
from .permissions import IsOwnerOrReadOnly
# from corsheaders.decorators import cors_exempt, cors_decorator

# Create your views here.
class helloWorldView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        return JsonResponse({"message":"hello world"})

class signUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

# @cors_exempt
class userLoginView(APIView):
    def post(self,req):
        print(req.data['username'])
        print(req.data['password'])
        user = authenticate(username=req.data['username'],password=req.data['password'])
        if user:
            token,created = Token.objects.get_or_create(user=user)
            return JsonResponse({"token":token.key})
        else:
            return JsonResponse({"error":"invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)

class viewAndCreatePosts(generics.ListAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            if self.kwargs.get('pk') != None:
                return PostDetailSerializer
            return PostListSerializer
        return PostDetailSerializer

    def get(self,request,pk=None):
        if pk is not None:
            instance = get_object_or_404(self.get_queryset(),pk=pk)
            serializer = self.get_serializer(instance)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            list = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(list, many=True)
            return JsonResponse(serializer.data,safe=False, status=status.HTTP_200_OK)
        
    def post(self,request):
        print(request.data)
        data = request.data
        data['author'] = request.user.pk
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class deletePostView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        super().perform_destroy(instance)

class updatePostView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'
