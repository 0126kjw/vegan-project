# `django-auth`

Django, DRF(Django REST Framework), dj-rest-auth, django-allauth를 활용하여 로그인과 회원가입을 구현하였다.  
User Model의 username 대신 email을 사용하도록 변경하였다.

## 실행 방법

```bash
git clone https://github.com/minuchi/django-auth.git
cd django-auth
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

위와 같이 입력하고 http://localhost:8000/ 으로 접속하면 된다.
