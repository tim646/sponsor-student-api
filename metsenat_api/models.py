from django.db import models
from django.core.exceptions import ValidationError

# from django.utils.translation import gettext_lazy as _
# Create your models here.


# Integer Validators
def validate_integer(value):
    if len(str(value)) < 6:
        raise ValidationError(message='Kiritilgan raqam minimal miqdordan kam!', params={'value':value},)

class Talaba(models.Model):
    TALABALIK_TURI = [
        ('Bakalavr', 'Bakalavr'),
        ('Magister', 'Magistr'),
    ]
    OTM_LAR = [('WIUT', 'Westminister'),
               ('IUT', 'Inha'),
               ('TDYU', 'Toshkent Davlat Yuridik Universiteti'),
               ]

    f_i_o = models.CharField(max_length=150, blank=False, null=False)
    student_type = models.CharField(max_length=15, choices=TALABALIK_TURI, default='Bakalavr')
    kontrakt_miqdor = models.PositiveIntegerField(validators=[validate_integer])
    otm = models.CharField(choices=OTM_LAR, max_length=30)
    ajratilgan_summa = models.PositiveIntegerField(default=0, blank=True)
    tel_no = models.PositiveIntegerField(validators=[validate_integer])

    def __str__(self):
        return self.f_i_o



class Homiy(models.Model):
    SPONSOR_CHOICES = [
        ('Jismoniy', 'Jismoniy Shaxs'),
        ('Yuridik', 'Yuridik Shaxs'),
    ]

    HOLATI = [
        ('Yangi', 'Yangi'),
        ('Moderatsiyada', 'Moderatsiyada'),
        ('Tasdiqlangan', 'Tasdiqlangan'),
        ('Bekor', 'Bekor Qilingan'),
    ]
    f_i_o = models.CharField(max_length=170)
    sponsor_type = models.CharField(choices=SPONSOR_CHOICES, default='Jismoniy', max_length=15)
    tel_no = models.PositiveIntegerField(validators=[validate_integer])
    tulov_summa = models.PositiveIntegerField(validators=[validate_integer])
    tashkilot_nomi = models.CharField(max_length=300, blank=True, null=True)
    sana = models.DateTimeField(auto_now=True)
    sarflangan_summa = models.PositiveIntegerField(default=0, blank=True)
    holati = models.CharField(choices=HOLATI, default='Yangi', max_length=15)

    def __str__(self):
        return self.f_i_o


class Payment(models.Model):
    talaba = models.ForeignKey(Talaba, on_delete=models.CASCADE, related_name='talaba')
    homiy = models.ForeignKey(Homiy, on_delete=models.CASCADE, related_name='homiy')
    ajratilgan_summa = models.PositiveIntegerField()
    sana = models.DateField(auto_now=True)

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        """Databasega kiritilayotgan xar bir amallni tekshiradi Xato Yuzaga kelgan bo'lsa bu xaqida ogoxlantiradi!"""

        if self.homiy.tulov_summa - self.homiy.sarflangan_summa < self.ajratilgan_summa:
            raise ValidationError("Homiyda Ajratish uchun Yetarli mablag' mavjud emas!!!!!!")
        elif self.talaba.kontrakt_miqdor == self.talaba.ajratilgan_summa:
            raise ValidationError('Talaba kantrakti Allaqachon Tulangan!!!!!!')
        elif self.talaba.kontrakt_miqdor - self.talaba.ajratilgan_summa < self.ajratilgan_summa:
            raise ValidationError('Ajratilayotgan summa Keragidan ortiq!!!!!!')
        elif self.ajratilgan_summa < 10000:
            raise ValidationError("Pul ajratishning eng kam miqdori 10 ming sum")


    def save(self, *args, **kwargs):
        """Funksiya malumotni saqlashdan oldin validate qiladi va  kiritilgan inputlarni databasega saqlaydi!"""

        self.full_clean()
        homiy_sarf_sum = Homiy.objects.get(pk=self.homiy.id)
        homiy_sarf_sum.sarflangan_summa += self.ajratilgan_summa
        talaba_ajrat_sum = Talaba.objects.get(pk=self.talaba.id)
        talaba_ajrat_sum.ajratilgan_summa += self.ajratilgan_summa
        homiy_sarf_sum.save()
        talaba_ajrat_sum.save()
        return super(Payment, self).save(*args, **kwargs)



    def __str__(self):
        return self.talaba.f_i_o





