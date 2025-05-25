from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, ProductViewSet, RegisterView, LoginView, CompanyProductView, SendCompanyProductsPDFView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register users'),
    path('login/', LoginView.as_view(), name='login users'),
     path('send-inventary/', SendCompanyProductsPDFView.as_view(), name='send_company_products_pdf'),
    path('company/<int:company_nit>/products/', CompanyProductView.as_view(), name='company products'),
]

urlpatterns += router.urls