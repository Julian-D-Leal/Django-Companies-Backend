from rest_framework import generics, status, viewsets
from django.db import transaction
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from io import BytesIO
from reportlab.pdfgen import canvas
from rest_framework.response import Response
from .models import Company, CustomUser, Product
from .serializers import CompanySerializer, ProductSerializer, UserSerializer, UserLoginSerializer

#productos
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
#compañias
class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    #aplicando atomic transaction en el metodo delete
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        company = self.get_object()
        try:
            if Product.objects.filter(company_id=company.nit).exists():
                return Response({'error': 'the company has associted products, It cannot be deleted'}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Company deleted successfully'})
    
#inventario
class CompanyProductView(generics.ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        company_nit = self.kwargs['company_nit']
        return Product.objects.filter(company_id=company_nit)
    
#inventario en pdf y envio a email
class SendCompanyProductsPDFView(APIView):


    def post(self, request):
        email = request.data.get('email')
        company_name = request.data.get('company_name')
        company_nit = request.data.get('company_nit')

        if not email or not company_nit:
            return Response({'error': 'Email and companys Nit are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(nit=company_nit)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found.'}, status=status.HTTP_404_NOT_FOUND)
        products = Product.objects.filter(company_id=company_nit)

        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Products for {company_name}")

        y = 770

        p.drawString(100, y, f"Nombre del producto - Código - descripción - precio - moneda")
        y -= 20  
        for product in products:
            p.drawString(100, y, f"{product.name} - {product.code} - {product.description} - {product.price} - {product.currency}")
            y -= 20
            if y < 50:
                p.showPage()
                y = 800

        p.showPage()
        p.save()
        buffer.seek(0)

        email_message = EmailMessage(
            f'Product List for {company_name}',
            f'Attached is the product list for {company_name}.',
            'julian-231@hotmail.com',
            [email],
        )
        email_message.attach(f'{company_name}_products.pdf', buffer.read(), 'application/pdf')
        email_message.send()

        return Response({'message': 'PDF sent by email'}, status=status.HTTP_200_OK)

def get_completion(prompt):
    # query = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=1024,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    # )

    # response = query.choices[0].text
    # print(response)
    # return response
    return "This is a mock response from the chatbot."

class ChatBotView(APIView):
    def post(self, request):
        user_message = request.data.get('message')
        if not user_message:
            return Response({'error': 'Message is required.'}, status=status.HTTP_400_BAD_REQUEST)

        bot_response = get_completion(user_message)

        return Response({'response': bot_response}, status=status.HTTP_200_OK)


class RegisterView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            if not user.is_admin:
                if user.password == password:
                    serializer = UserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            if user.check_password(password):
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    