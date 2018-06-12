"""a_box URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views  # 이 줄 추가. auth
from a_box_app.views import signin, fileList, fileUpload

# 밑에 두개 static 파일 설정
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^main/$', fileList, name = 'main'),
    url(r'^upload/$', fileUpload, name = 'upload'),
    
    url(
        r'^logout/$',
        # django.contrib.auth.views를 auth_views로 위에 설정했고,
        # 이것의 logout 뷰함수를 작동시킴
        auth_views.logout,
        name='logout',

        # 추가로 전할달 인자
        kwargs={
            # next_page : 로그아웃 후 이동할 url
            # 이 항목이 없으면 기본 django logout page로 이동
            # LOGIN_URL은 기본적으로는 /accounts/login/ 으로 지정되어있음
            # 'next_page': settings.LOGIN_URL,
            'next_page': '/'
        }
    ),



    url(r'^$', signin, name = 'login'),
]
