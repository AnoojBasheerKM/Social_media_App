from rest_framework import serializers

from socialapp.models import User,Post,Comment

class UserSerializer(serializers.ModelSerializer):
    
    password1 = serializers.CharField(write_only = True)
    
    password2 = serializers.CharField(write_only = True)
    
    class Meta:
        
        model = User

        fields = ["id","username","email","phone","password1","password2"]

        read_only_fields=["id","password"]
        
    def create(self,validated_data):
        
        password1 = validated_data.pop("password1")
        
        password2 = validated_data.pop("password2")
        
        if password1!= password2:
            
            return serializers.ValidationError("password Missmatch")

        return User.objects.create_user(**validated_data,password=password1)
    
class PostSerializer(serializers.ModelSerializer):
    
    owner = serializers.StringRelatedField(read_only=True)
    
    liked_by = serializers.StringRelatedField(read_only = True,many=True)
    
    like_count = serializers.SerializerMethodField()
    
    comment = serializers.SerializerMethodField()
    
    comment_count = serializers.SerializerMethodField()
    
    

    class Meta:
        
        model = Post
        
        fields = "__all__"

        read_only_fields = ["id","owner","created_at","updated_at","liked_by"]

    def get_like_count(self,obj):
        
        return obj.liked_by.all().count()
    
    def get_comment_count(self,obj):
        
        return Comment.objects.filter(Post=obj).count()
    
    def get_comment(self,obj):
        
        qs = Comment.objects.filter(Post=obj)
        
        serializer_instance = CommentSerializer(qs)

        return serializer_instance.data
    
class CommentSerializer(serializers.ModelSerializer):
    
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        
        model = Comment

        fields = "__all__"

        read_only_fields = ["id","post","owner","created_at"]
        
class ProfileSerializers(serializers.ModelSerializer):
    
    class Meta:
        
        model = User

        fields = "__all__"

        read_only_fields = ["id","owner"]

        
        



