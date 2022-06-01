from django.urls import path

from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views
#from .views import ListCategory, DetailCategory, ListChocolate, DetailChoco, SearchResultsListView, ChocoCheckoutView, PaymentComplete,CartAdd,home,services

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('home/',views.home, name='home'),
    path('services/', views.services, name='services'),
    path('categorylist',views.ListCategory.as_view(),name='categorylist'),
    path('categories/<int:pk>/',views.DetailCategory.as_view(),name='singlecategory'),
    path('chocolates',views.ListChocolate.as_view(),name='list'),
    path('details/<int:pk>/',views.DetailChoco.as_view(),name='detail'),
    path('search/<int:pk>/',views.SearchResultsListView.as_view(),name='search_results'),
    path('checkout/<int:pk>/',views.ChocoCheckoutView.as_view(), name='checkout'),
    path('complete/',views.PaymentComplete, name = 'complete'),
    path('cart/(?P<product_id>[0-9]+)$',views.CartAdd.as_view(), name='addtocart'),
    #path('cart/add/<int:id>/', CartAdd.as_view(), name='cart_add'),
    #path('cart/add/<int:id>/', views.cart_add, name='cart_add'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)