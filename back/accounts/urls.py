from django.urls import path, include, re_path
from .views import KakaoLogin, Checkemail


urlpatterns = [
    # 로그인, 정보 조회 등
    path('', include('dj_rest_auth.urls')),
    # 이메일 중복 확인
    path('email/<str:email>', Checkemail.as_view()),
    # 회원가입
    path('registration/', include('dj_rest_auth.registration.urls')),
    # 카카오 로그인
    re_path(r'^kakao/login/$', KakaoLogin.as_view(), name='kakao_login'),
]
