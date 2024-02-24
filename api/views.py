from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from .models import Person
from .serilizers import PeopleSerilizers,RegisterSerilizer,LoginSerilizer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

@api_view(["POST"])
def register(request):
    ser=RegisterSerilizer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    else:
        return Response(ser.errors)

@api_view(["POST"])
def login(request):
    ser=LoginSerilizer(data=request.data)
    if ser.is_valid():
        user=authenticate(username=ser.validated_data.get("username"),password=ser.validated_data.get("password"))
        if not user:
            return Response({"mes":"user Doesnt exists"},status=status.HTTP_404_NOT_FOUND)
        
        try:
            token=Token.objects.get(user=user)
        except:
            token=Token.objects.create(user=user)
            
        
        
        return Response({'user':ser.validated_data.get("username"),'mes':'user_created','token':str(token)},)
    else:
        return Response(ser.errors)
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout(request):
    
    user=Token.objects.get(user=request.user)
    user.delete()
    return Response({"msg":"logout sucessful"})
    



@api_view(["POST","GET"])    
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def people(request):
    if request.method=="GET":
        data=Person.objects.all()
        serilizer=PeopleSerilizers(data,many=True)
        return Response(serilizer.data)
    if request.method=="POST":
        data=request.data
        serilizer=PeopleSerilizers(data=data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        return Response(serilizer.errors)

@api_view(["GET","PUT","PATCH","DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def mehods(request,id):
    try:
        instance=Person.objects.get(id=id)
    except:
        return Response({"msg":'No Data Found'})
    if request.method=="GET":
        ser=PeopleSerilizers(instance)
        return Response(ser.data)
    if request.method=="PUT":
        ser=PeopleSerilizers(instance,data=request.data)
        if(ser.is_valid()):
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)
        

        
    if request.method=="PATCH":
        ser=PeopleSerilizers(instance,data=request.data,partial=True)
        if(ser.is_valid()):
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)
        
    if request.method=="DELETE":
        instance.delete()
        return Response({'msg':'Delete sucessful'})