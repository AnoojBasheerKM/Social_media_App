from django.shortcuts import render

from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView

from socialapp.serializers import UserSerializer,PostSerializer,CommentSerializer,ProfileSerializers

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework import authentication,permissions

from rest_framework.response import Response

from socialapp.permissions import OwnerOnly,OwnerOrReadOnly

from socialapp.models import Post,Profile

from rest_framework.views import APIView



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
        
    def get_serializer_context(self):
        
        context= super().get_serializer_context()
    
        context["request"] = self.request
        
        return context
    
class PostUpdateRetrieveDestroyView(UpdateAPIView,RetrieveAPIView,DestroyAPIView):
    
    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [OwnerOrReadOnly]

    serializer_class = PostSerializer
    
    queryset = Post.objects.all()
    
class PostLikeView(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def post (self,request,*args,**kwargs):
        
        id = kwargs.get("pk")

        post_object = Post.objects.get(id=id)
        
        if request.user in post_object.liked_by.all():
            
            post_object.liked_by.remove(request.user)

        else:
            
            post_object.liked_by.add(request.user)

            liked = True

        post_object.liked_by.add(request.user)

        return Response(data={"message":"ok","liked":liked})
    
class PostCommentView(CreateAPIView):
    
    serializer_class = CommentSerializer
    
    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        
        serializer_instance = self.serializer_class(data=request.data)

        id = kwargs.get("pk")

        post_object = Post.objects.get(id=id)

        if serializer_instance.is_valid():
            
            serializer_instance.save(post=post_object,owner=request.user)

            return Response(data=serializer_instance.data)

        return Response(data=serializer_instance.errors)
    
class UserProfileView(UpdateAPIView):
    
    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = ProfileSerializers

    def get_object(self):
        
        return Profile.objects.get(owner__username=self.request.user)
    

    

    
  
    
    

