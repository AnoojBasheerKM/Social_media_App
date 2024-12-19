from django.shortcuts import render

from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView

from socialapp.serializers import UserSerializer,PostSerializer

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework import authentication,permissions

from rest_framework.response import Response

from socialapp.models import Post



# Create your views here.

class SignupView(CreateAPIView):
    
    serializer_class = UserSerializer
    
class PostCreateListView(ListAPIView,CreateAPIView):
    
    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = PostSerializer
    
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        
        serializer.save(owner=self.request.user)
    
class PostUpdateRetrieveDestroyView(UpdateAPIView,RetrieveAPIView,DestroyAPIView):
    
    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = PostSerializer
    
    queryset = Post.objects.all()

    

    
  
    
    

