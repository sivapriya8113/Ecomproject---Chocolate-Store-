from django.shortcuts import render, redirect
from knox.models import AuthToken
from django.contrib.auth import login
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.db.models import Q # for search method
from django.http import JsonResponse
import json

from .models import Category, Chocolates, Order,CartItem
from .serializers import ChocoSerializer,CategorySerializer

from cart.cart import Cart


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'
    serializer_class = RegisterSerializer

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


# Register API
class RegisterAPI(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Register.html'
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


def home(request):
    return render(request,'home.html')


def services(request):
    return render(request,'services.html')


class ListChocolate(generics.ListCreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'list.html'
    serializer_class = ChocoSerializer

    def get(self, request):
        queryset = Chocolates.objects.filter(is_deleted=False).all()
        return Response({'object_list': queryset})


class ListCategory(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'listcategory.html'
    #permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CategorySerializer

    def get(self,request,pk=None):
        queryset = Category.objects.get(id=pk)
        return Response({'object': queryset})


class DetailCategory(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'listcategory.html'
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request):
        queryset = Category.objects.all()
        return Response({'object': queryset})


class DetailChoco(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'detail.html'
    serializer_class = ChocoSerializer

    def get(self, request,pk=None):
        queryset = Chocolates.objects.get(id=pk)
        return Response({'object': queryset})


class SearchResultsListView(generics.ListAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'search_results.html'
    serializer_class = ChocoSerializer

    def get(self, request,pk=None):
        queryset = Chocolates.objects.get(id=pk)
        return Response({'object_list': queryset})


class ChocoCheckoutView(generics.ListAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'checkout.html'
    serializer_class = ChocoSerializer

    def get(self, request, pk=None):
        queryset = Chocolates.objects.get(id=pk)
        return Response({'object': queryset})


def PaymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    product = Chocolates.objects.get(id=body['productId'])
    Order.objects.create(
    product=product
    )
    return JsonResponse('Payment completed!', safe=False)


class ChocoCheckoutView(generics.ListAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'checkout.html'
    serializer_class = ChocoSerializer

    def get(self, request, pk=None):
        queryset = Chocolates.objects.get(id=pk)
        return Response({'object': queryset})

'''
class CartAdd(generics.RetrieveUpdateDestroyAPIView ):
    #permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'checkout.html'
    serializer_class = ChocoSerializer

    def get(self,request,id):
        cart = Cart(request)
        queryset = Chocolates.objects.get(id=id)
        cart.add(product=queryset)
        return redirect("list")
'''


class CartAdd(generics.CreateAPIView ):
    #permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'checkout.html'
    serializer_class = ChocoSerializer

    def post(self, request, *args, **kwargs):
        ins_obj,created=CartItem.objects.get_or_create(user=request.user,product_id=kwargs['product_id'])
        if created:
            ins_obj.quantity=ins_obj.quantity+1
            ins_obj.save()
        return Response('ok')

