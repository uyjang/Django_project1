from django.db import models

# Create your models here.

# 모델의 변수나 어떠한 변경사항이 있을 시 python manage.py makesmigrations 하고 python manage.py migrate를 진행해준다. 그 다음에 서버 실행 (데이터 베이스에 변경사항을 적용하고 진행하는 듯한 느낌)


class Fcuser(models.Model):
    username = models.CharField(max_length=64, verbose_name='사용자명')
    useremail = models.EmailField(max_length=128, verbose_name='사용자 이메일')# 이미 데이터가 한번 생성된 다음 중간에 데이터베이스의 열을 추가하고 마이그레이션을 진행하면 지금 추가하는 열에는 어떤 데이터를 넣을 거니 하면서 물어봄(1번방법일 경우 내가 직접입력, 2번 방법일 경우 인자로 default값을 지정) 
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    regstered_dttm = models.DateTimeField(
        auto_now_add=True, verbose_name='등록시간')

    def __str__(self): # 새로운 유저를 등록할 때마다 목록에 유저네임으로 나오게 함.
        return self.username

    class Meta: # 데이터베이스 테이블명을 별도로 설정하고 싶어요! # 내가 만든 앱의 이름과 데이터 베이스의 테이블명을 좀 구분하기 위해서 설정.
        db_table = 'fastcampus_fcuser'
        verbose_name = '패스트캠퍼스 사용자' # FCuser앱이 뜬 목록 밑에 패스트캠퍼스 사용자라고 표시하고 그걸 누르면 사용자들이 등록된 리스트가 쭉 나옴.
        verbose_name_plural = '패스트캠퍼스 사용자'

# makemigrations 는 내가 모델클래스에 지정한 변수들을 데이터베이스의 필드명으로 만들어서 데이터베이스를 만든다.
# migrate 세팅파일에 있는 여러 앱들이 사용하는 테이블들을 자동으로 생성해줌.ㄴ
