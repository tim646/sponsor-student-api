from django.contrib.auth.models import User
from rest_framework import routers, serializers
from rest_framework.exceptions import ValidationError
from .models import Homiy, Talaba, Payment


from django.db.models import Count, Sum

# Yangi Homiy Serializeri
class UnauthHomiySerializer(serializers.ModelSerializer):
    class Meta:
        model = Homiy
        fields = ['id', 'sponsor_type', 'f_i_o', 'tel_no', 'tulov_summa', 'tashkilot_nomi']


# TALABAGA PUL AJRATISH SERIALIZERI
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'talaba', 'homiy', 'ajratilgan_summa', 'sana',)

    def validate(self, data):
        """ Talabaga Pul ajratayotganda inputlar to'g'ri kiritilganini va
         xisob kitob to'gri amalga oshirilganini tekshiradi"""
        data = super().validate(data)
        kontrakt_miqdor = data.get('talaba').kontrakt_miqdor
        talabaga_ajratilgan_summa = data.get('talaba').ajratilgan_summa
        homiy_tulov_sum = data.get("homiy").tulov_summa
        homiy_ajratayotgan_sum = data.get('ajratilgan_summa')
        homiy_sarflangan_sum = data.get("homiy").sarflangan_summa

        if kontrakt_miqdor == talabaga_ajratilgan_summa:
            raise ValidationError({"talaba": "Talaba Kantrakti to'langan!"})
        elif homiy_ajratayotgan_sum + homiy_sarflangan_sum > homiy_tulov_sum:
            raise ValidationError({"homiy": "Homiyda yetarli mablag' mavjud emas!!"})
        elif kontrakt_miqdor - talabaga_ajratilgan_summa < homiy_ajratayotgan_sum:
            raise ValidationError({"ajratilgan_summa": "Ajratilayotgan summa keragidan ortiq!"})
        elif 10000 > homiy_ajratayotgan_sum:
            raise ValidationError({"ajratilgan_summa": "Pul ajratishning eng kam miqdori 10 ming sum"})
        return data


# ADMIN HOMIY MODELI BILAN ISHLASHI UCHUN SERIALIZER
class HomiySerializer(serializers.ModelSerializer):
    class Meta:
        model = Homiy
        fields = '__all__'

# ADMIN TALABA MODELI BILAN ISHLASHI UCHUN SERIALIZER
class TalabaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talaba
        fields = '__all__'


# DASHBOARD HISOBOTLAR
class HisobotSerializer(serializers.ModelSerializer):
    jami_tulov_sum = serializers.IntegerField()
    jami_suralgan_sum = serializers.IntegerField()
    tulanishi_kerak_sum = serializers.IntegerField()
    talabalar_soni = serializers.IntegerField()
    homiylar_soni = serializers.IntegerField()
    class Meta:
        model = Payment
        fields = ('jami_tulov_sum', 'jami_suralgan_sum', 'tulanishi_kerak_sum', 'talabalar_soni', 'homiylar_soni',)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']







