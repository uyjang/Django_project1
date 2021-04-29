from django.shortcuts import render, redirect
from .models import Fcuser
from django.views.decorators.csrf import csrf_exempt  # 교차사이트로 접속돼서 정보같은거 훔치는 것을 방지
from django.http import HttpResponse  # 에러같은 것이 생겼을 때 대응
# 글자로 안보이고 암호화 되게 해서 보이게 해주는 것
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm
# Create your views here.


def home(request): # urls에 연결을 해놨기 때문에 클라이언트가 웹을통해 요청을 한 것이 request로 저장되어서 들어옴.
    user_id = request.session.get('user') # 세션에 있는 유저키는 fcuser모델의 id값을 가지고 있음. 즉 user는 fcuser모델의 id값임.
    if user_id: # 세션이 있다라는 것이고 그건 로그인을 했다는 말.
        fcuser = Fcuser.objects.get(pk=user_id) # fcuser모델의 id값에 해당하는 정보들을 가지고 있는 변수임.
    #     return HttpResponse(fcuser.username)
    # return HttpResponse('Home!') # 일단 텍스트만 출력
    return render(request, 'home.html',) # 이미 템플릿 폴더를 바라보고 있음.


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/') # 루트라는 표시임! 아무것도 없는 최상위의 상태


def login(request):
    # if request.method == 'GET':
    #     return render(request, 'login.html',  )
    # elif request.method == 'POST':
    #     username = request.POST.get('username', None) # 전송한 데이터들은 일단 POST안에 담겨있음. # 그리고 .get이 아닌 POST[]형태(딕셔너리)로 가져오면 키가 없을때 에러가 나옴.
    #     password = request.POST.get('password', None)
        
    #     res_data = {}

    #     if not (username and password):
    #         res_data['error'] = '모든 값을 입력해야합니다.'
    #     else: 
    #         fcuser = Fcuser.objects.get(username=username) # fcuser모델을 먼저 가지고오고 앞에 있는 username은 데이터베이스에 있는 것 뒤에 있는 유저네임은 클라이언트가 입력해서 리퀘스트를 통해서 받아온 것
    #         if check_password(password, fcuser.password): # 체크 패스워드를 통해 클라이언트가 입력한 비밀번호랑 데이터베이스의 비밀번호가 같은 지 확인
    #             request.session['user'] = fcuser.id # 같으면 리퀘스트안에 있는 세션이라는 변수(딕셔너리 형태)의 user키에 장고에서 자동으로 만들어주는 fcuser모델의 id값을 저장해놓음.
    #             return redirect('/') # 그다음에 메인홈페이지 화면으로 옮김.
    #         else:
    #             res_data['error'] = '비밀번호가 틀렸습니다.'
    if request.method == 'POST':
        form = LoginForm(request.POST) # forms.py파일안에있는 로그인폼에 POST가 가지고 있는 데이터를 인자로 넣어서 넘겨준다
        if form.is_valid(): # 폼에는 기본적으로 is_valid()라는 함수가 있음 # 로그인폼에 들어간 데이터(POST에 담긴)가 정상인지 확인 # 그리고 폼 안에는 기본적으로 에러정보들이 들어있어서 에러정보를 출력하는 것도 가능함
                            # 만약 유효하지 않다고 판단을 하면 폼안에 들어있는 에러정보들이 render함수 안에있는 폼으로 전달이 되고 템플릿으로 전송된다
            request.session['user'] = form.user_id # 검증이 다 완료가되면 세션에 있는 user라는 키에 value로 id를 줄건데 id는 fcuser에 있으므로 불러와야됨. 불러오는 건 forms.py 파일안에서 할거임
            return redirect('/')
    else:
        form = LoginForm() # forms.py 안에 만들어 놓은 폼을 이용할 거니까 지정만 해준다
    return render(request, 'login.html', {'form':form})


@csrf_exempt
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        # register.html에서 name필드에 있는 값을 키로해서 정보들을 받음. 
        username = request.POST.get('username', None) # 전송한 데이터들은 일단 POST안에 담겨있음. # 그리고 .get이 아닌 POST[]형태(딕셔너리)로 가져오면 키가 없을때 에러가 나옴.
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)# 여기까지랑
        
        # 여기 res_data 이하부터 elif까지는 요청을 처리해주는 로직들을 만든 것.
        res_data = {}

        if not (username and useremail and password and re_password):
            res_data['error'] = '모든 값을 입력해야합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'

        else: # 여기는 html 즉 클라이언트가 입력한 데이터를 받아서 데이터베이스에 저장하는 과정
            fcuser = Fcuser(
                username=username,
                useremail=useremail,
                password=make_password(password)
            )
            fcuser.save()

        return render(request, 'register.html', res_data) # res데이터가 html로 보내지고 html에서는 res데이터를 받을 수 있는 자리를 마련해줘야됨.
