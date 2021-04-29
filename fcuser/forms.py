from django import forms  # 장고안에 있는 폼
from .models import Fcuser
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):
    username = forms.CharField( # 폼 안에 에러메시지들을 담은 곳들에는 key로 required라는 것이 있고 빈값이 입력했을 때 required라는 키가 가지고 있는 값을 보여주게 됨 
        error_messages={'required': '아이디를 입력해주세요.'}, max_length=32, label="사용자 이름") # 여기서 사용한 라벨이 템플릿에 사용된 라벨하고 연동됨.
    password = forms.CharField(
        error_messages={'required': '비밀번호를 입력해주세요.'}, widget=forms.PasswordInput, label="비밀번호") # 여기의 위젯은 템플릿에 지정된 위젯과 연동됨.

    def clean(self): # 값이 일치하는 지 않하는 지 확인하는 단계
        cleaned_data = super().clean() # 기존의 폼안에 만들어져있었던 것이기 때문에 기존의 폼안에 들어있던 클린함수를 먼저 호출해준다. 만약에 값이 안들어있으면 여기에서 실패처리가 돼어서 나가진다
                                       # 왜냐면 위에 로그인폼이라는 클래스에서 폼을 만들었고 거기에 username과 password라는 데이터를 저장해놨기 때문
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                fcuser = Fcuser.objects.get(username=username)
            except Fcuser.DoesNotExist: # 에러처리를 해놓으면 이상한 홈페이지로 이동하는 것이아니라 에러메시지를 템플릿에있는 error메시지가 뜨는 곳에 나오게 해줌
                self.add_error('username', '아이디가 없습니다.')
                return
    #         # 앞에는 내가 방금 입력한 부분, 뒤에는 모델안에 들어있던 번호
            if not check_password(password, fcuser.password):
    #             # 비밀번호 부분에 대한 에러이기때문에
                self.add_error('password', '비밀번호를 틀렸습니다.') # 이미 폼안에는 기본적으로 에러들이 있고 그 중에 하나인 에드에러인데 특정필드에다가 에러를 넣는 함수
            else: # 아이디도 있고 그 아이디는 fcuser데이터베이스에서 가져온 것이고 그 데이터베이스에서 가져온 아이디에 저장된 비밀번호랑 내가 지금 입력한 비밀번호가 맞다면
                self.user_id = fcuser.id # 데이터베이스에서 가져온 id를 내가 변수로 지정한 user_id에 넣음
