from django.contrib import admin
from django.urls import path, include, re_path
from dj_rest_auth.registration.views import VerifyEmailView
from accounts.views import ConfirmEmailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    re_path(r'^ragistration/email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    
    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^ragistration/email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
]
