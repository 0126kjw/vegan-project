from django.contrib import admin
from django.urls import path, include, re_path
from dj_rest_auth.registration.views import VerifyEmailView
from accounts.views import ConfirmEmailView
from django.urls import include


urlpatterns = [
    # 관리자
    path('admin/', admin.site.urls),
    # 로그인, 회원가입 등
    path('', include('accounts.urls')),
    # 소셜 로그인
    path('accounts/', include('allauth.urls')),
    # 인증 이메일
    re_path(r'^registration/email/$', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),
    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^registration/email/(?P<key>[-:\w]+)/$',
            ConfirmEmailView.as_view(), name='account_confirm_email'),
    # 게시물, 댓글 등
    path('board/', include('posts.urls'))
]
