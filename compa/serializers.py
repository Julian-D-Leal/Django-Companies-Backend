from rest_framework import serializers
from .models import CustomUser, Company, Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'is_admin', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['nit', 'name', 'address', 'phone']
        extra_kwargs = {
            'nit': {'required': True},
            'name': {'required': True},
            'address': {'required': True},
            'phone': {'required': True}
        }
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'price', 'currency', 'company']
        extra_kwargs = {
            'code': {'required': True},
            'name': {'required': True},
            'description': {'required': True},
            'price': {'required': True},
            'currency': {'required': True},
            'company': {'required': True}
        }