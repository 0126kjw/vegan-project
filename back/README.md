# `django-auth`

Django, DRF(Django REST Framework), dj-rest-auth, django-allauth를 활용하여 로그인과 회원가입을 구현하였습니다. 
User Model의 username 대신 email을 사용하도록 변경하였습니다.

## 실행 방법

```bash
cd back
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python manage.py runserver
```

위와 같이 입력하고 http://localhost:8000/ 으로 접속하면 됩니다.

## API Document
https://documenter.getpostman.com/view/22491165/2s83zgsPrg
