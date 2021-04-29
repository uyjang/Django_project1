from django.contrib import admin
from .models import Board
# Register your models here.

# 어드민 사이트에서 왼쪽 메뉴에 Board라는 것을 추가
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Board, BoardAdmin)
