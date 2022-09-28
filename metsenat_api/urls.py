from django.urls import path, include

from . import views

urlpatterns = [
    # HOMIY URLS
    path('', views.apiOverview, name='api-overview'),
    # UNAUTH HOMIY
    path('unauth-homiy-create/', views.unauth_homiy_create, name='unauth-homiy-create'),

    path('homiy-list/', views.homiy_list, name='homiy-list'),
    path('homiy-detail/<str:pk>/', views.homiy_detail, name='homiy-detail'),
    path('homiy-create/', views.homiy_create, name='homiy-create'),
    path('homiy-delete/<str:pk>/', views.homiy_delete, name='homiy-delete'),
    path('homiy-update/<str:pk>/', views.homiy_update, name='homiy-update'),

    # TALABA URLS
    path('talaba-list/', views.talaba_list, name='talaba-list'),
    path('talaba-detail/<str:pk>/', views.talaba_detail, name='talaba-detail'),
    path('talaba-create/', views.talaba_create, name='talaba-create'),
    path('talaba-delete/<str:pk>/', views.talaba_delete, name='talaba-delete'),
    path('talaba-update/<str:pk>/', views.talaba_update, name='talaba-update'),


#     Payment URLS
    path('payment-list/', views.payment_list, name='payment-list'),
    path('pul-ajratish/', views.make_payment, name='make-payment'),

#     Dashboard Hisobot URL
    path('dashboard/', views.get_dashboard_hisobot, name='dashboard')

]
