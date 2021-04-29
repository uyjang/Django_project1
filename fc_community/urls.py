"""fc_community URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include
from fcuser.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fcuser/', include('fcuser.urls')),
    path('', home), # fcuser앱 밑에 만들면 메인홈페이지가 아니라 fcuser처리에 종속되는 홈페이지임... # 그리고 ''안에 비워 놓는 이유는 주소 다음에 아무것도 안적으면 홈으로 이동하게 할거기 때문이다.
    path('board/', include('board.urls')),
]
