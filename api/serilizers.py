from rest_framework import serializers
from .models import Person,Address
from django.contrib.auth.models import User


class LoginSerilizer(serializers.Serializer):
    username=serializers.CharField(max_length=50)
    password=serializers.CharField(write_only=True)
    


class RegisterSerilizer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["username","email","password"]
    
    def create(self, validated_data):
        user=User.objects.create(username=validated_data.get("username"),email=validated_data.get("email"))
        user.set_password(validated_data.get("password"))
        user.save()
        return user
    
    def validate_username(self, attrs):
        if User.objects.filter(username=attrs).exists():
            raise serializers.ValidationError("Username already exists")
        return attrs


class AddressSerilizers(serializers.ModelSerializer):
     class Meta:
        model=Address
        fields="__all__"   

class PeopleSerilizers(serializers.ModelSerializer):
    address = AddressSerilizers() 
    class Meta:
        model=Person
        fields=["name","age","address"]
        depth=1
    
    def create(self,validated_data):
        
        
        try:
            address=Address.objects.get(address=validated_data.get("address").get("address"))
        except:
            address=Address.objects.create(address=validated_data.get("address").get("address"))
            
        
        return Person.objects.create(name=validated_data.get("name"),age=validated_data.get("age"),address=address)

       
    #using field and using objects upper one is using field and lower one is using objects
    def validate_age(self,value):
        if(value<18):
            raise serializers.ValidationError("age should be greater than 18")
        return value

    def validate(self,value):
        if(value['age']<18):
            raise serializers.ValidationError("age should be greater than 18")
        return value