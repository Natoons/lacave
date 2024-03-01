"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from inventory import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dash/', views.index, name='dash'),
    path('products/', views.products, name='products'),
    path('last_products/', views.last_products, name='last_products'),
    path('user_product_quantities/', views.user_product_quantities, name='user_product_quantities'),
    path('user_graph_quantities/', views.user_graph_quantities, name='user_graph_quantities'),
    path('user_category_graphs/', views.user_category_graphs, name='user_category_graphs'),
    path('users/', views.users, name='users'),
    path('user/', views.user, name='user'),
    path('register/', views.register, name='register'),
    path('', auth.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='inventory/logout.html'), name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
