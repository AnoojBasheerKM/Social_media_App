from rest_framework import serializers

from socialapp.models import User

class UserSerializer(serializers.ModelSerializer):
    
    password1 = serializers.CharField(write_only = True)
    
    password2 = serializers.CharField(write_only = True)
    
    class Meta:
        
        model = User

        fields = ["id","username","email","phone","password"]

        read_only_fields=["id","password"]
        
    def create(self,validated_data):
        
        password1 = validated_data.pop("password1")
        
        password2 = validated_data.pop("password2")
        
        if password1!= password2:
            
            return serializers.ValidationError("password Missmatch")

        return User.objects.create_user(**validated_data,password=password1)



