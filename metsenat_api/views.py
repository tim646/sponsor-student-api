from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models.signals import post_save
from django.db.models import Count, Sum
import calendar

# Create your views here.
from .models import Homiy, Talaba, Payment


from .serializers import HomiySerializer, TalabaSerializer, PaymentSerializer, UnauthHomiySerializer, HisobotSerializer

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser

from rest_framework.exceptions import NotFound

from rest_framework.exceptions import ValidationError


# UNAUTH homiy uchun


# HOMIY Yaratish
@api_view(['POST'])
def unauth_homiy_create(request):
    serializer = UnauthHomiySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        raise ValidationError(serializer.errors)

    return Response(serializer.data)




# Hamma API Url larni ko'rish uchun
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Autarizatsiya qilinmagan Homiy Uchun URL': '',
        'Homiy Yaratish': '/unauth-homiy-create/',
        'Admin  Uchun URLlar': 'login: testuser | password: metsenatapi',
        'Homiy List': '/homiy-list/',
        'Homiy Detail': '/homiy-detail/<str:pk>/',
        'Homiy Create': '/homiy-create/',
        'Homiy Update': '/homiy-update/<str:pk>/',
        'Homiy Delete': '/homiy-delete/<str:pk/',
        'Talabaga Pul Ajratish': '/pul-ajratish/',
        'Barcha Pul Utkazmalar': '/payment-list/',
        'Hisobot Dashboard': '/dashboard/',
        'Talaba List': '/talaba-list/',
        'Talaba Detail': '/talaba-detail/<str:pk>/',
        'Talaba Create': '/talaba-create/',
        'Talaba Update': '/talaba-update/<str:pk>/',
        'Talaba Delete': '/talaba-delete/<str:pk/',
    }
    return Response(api_urls)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
def homiy_list(request):
    queryset = Homiy.objects.all()
    serializer = HomiySerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
def homiy_detail(request, pk):
    homiy = Homiy.objects.get(id=pk)
    serializer = HomiySerializer(homiy, many=False)
    return Response(serializer.data)


@api_view(['POST'])
# @permission_classes([IsAdminUser])
def homiy_create(request):
    serializer = HomiySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
# @permission_classes([IsAdminUser])
def homiy_delete(request, pk):
    queryset = Homiy.objects.get(pk=pk)
    homiy = get_object_or_404(queryset, pk=pk)
    homiy.delete()
    return Response("Homiy O'chirildi!")


@api_view(['POST'])
# @permission_classes([IsAdminUser])
def homiy_update(request, pk):
    homiy = Homiy.objects.get(id=pk)
    serializer = HomiySerializer(instance=homiy, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# MAKING PAYMENT FUNCTIONS - Talabaga PUL ajratish
@api_view(['GET'])
# @permission_classes([IsAdminUser])
def payment_list(request):
    queryset = Payment.objects.all()
    serializer = PaymentSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
# @permission_classes([IsAdminUser])
def make_payment(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        raise ValidationError(serializer.errors)
    return Response(serializer.data)



@api_view(['GET'])
# @permission_classes([IsAdminUser])
def get_dashboard_hisobot(request):
    jami_tulov_sum = Payment.objects.all().aggregate(jami_tulov_sum=Sum('ajratilgan_summa'))['jami_tulov_sum']
    jami_suralgan_sum = Talaba.objects.all().aggregate(jami_suralgan_sum=Sum('kontrakt_miqdor'))['jami_suralgan_sum']
    tulanishi_kerak_sum = jami_suralgan_sum - jami_tulov_sum
    talabalar_soni = Talaba.objects.all().aggregate(talabalar_soni=Count('id'))['talabalar_soni']
    homiylar_soni = Homiy.objects.all().aggregate(homiylar_soni=Count('id'))['homiylar_soni']
    serializer = {'jami_tulov_sum': jami_tulov_sum, 'jami_suralgan_sum':jami_suralgan_sum,'tulanishi_kerak_sum': tulanishi_kerak_sum,
     'talabalar_soni':talabalar_soni, 'homiylar_soni':homiylar_soni,}
    return Response(serializer)


@api_view(['GET'])
def homiy_talaba_kupayishi_oylarda(request, oy, yil):
    if oy < 1 or oy > 12:
        raise ValidationError('Invalid month number')
    homiylar_soni = Homiy.objects.filter(sana__year=yil, sana__month=oy).aggregate(homiylar_soni=Count('id'))[
        'homiylar_soni']
    talabalar_soni = Talaba.objects.filter(sana__year=yil, sana__month=oy).aggregate(talabalar_soni=Count('id'))[
        'talabalar_soni']
    oy = calendar.month_name[oy]
    serializer = {'oy': oy, 'yil': yil, 'homiylar_soni': homiylar_soni, 'talabalar_soni': talabalar_soni}
    return Response(serializer)


@api_view(['GET'])
def homiy_talaba_kupayishi_yillarda(request, yil):
    homiylar_soni = Homiy.objects.filter(sana__year=yil).aggregate(homiylar_soni=Count('id'))[
        'homiylar_soni']
    talabalar_soni = Talaba.objects.filter(sana__year=yil).aggregate(talabalar_soni=Count('id'))[
        'talabalar_soni']
    serializer = {'yil': yil, 'homiylar_soni': homiylar_soni, 'talabalar_soni': talabalar_soni}
    return Response(serializer)


# Talaba ViewSet CRUD Functions
@api_view(['GET'])
# @permission_classes([IsAdminUser])
def talaba_list(request):
    queryset = Talaba.objects.all()
    serializer = TalabaSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
def talaba_detail(request, pk):
    talaba = Talaba.objects.get(id=pk)
    serializer = TalabaSerializer(talaba, many=False)
    return Response(serializer.data)


@api_view(['POST'])
# @permission_classes([IsAdminUser])
def talaba_create(request):
    serializer = TalabaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
# @permission_classes([IsAdminUser])
def talaba_delete(request, pk):
    queryset = Talaba.objects.get(pk=pk)
    talaba = get_object_or_404(queryset, pk=pk)
    talaba.delete()
    return Response("Talaba O'chirildi!")


@api_view(['POST'])
# @permission_classes([IsAdminUser])
def talaba_update(request, pk):
    talaba = Talaba.objects.get(id=pk)
    serializer = TalabaSerializer(instance=talaba, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)







