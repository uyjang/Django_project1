from django.contrib import admin
from .models import Fcuser
# Register your models here.

# 어드민 사이트에 fcuser라는 앱이 등록되고 그 안에 fcuser라는 모델이 나오게 됨.
class FcuserAdmin(admin.ModelAdmin): # 모델클래스 안의 필드들이 리스트업 돼서 보여줌.
    list_display = ('username', 'password')


admin.site.register(Fcuser, FcuserAdmin)
