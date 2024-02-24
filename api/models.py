from django.db import models

# Create your models here.

class Address(models.Model):
    address=models.CharField(max_length=50)
    def __str__(self):
        return self.address

class Person(models.Model):
    address=models.ForeignKey(Address,related_name="add",null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,error_messages={'blank':'yah value hal'})
    age=models.IntegerField()
    def __str__(self):
        return self.name
