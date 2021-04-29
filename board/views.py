from django.shortcuts import render, redirect
from .models import Board
from .forms import BoardForm
from fcuser.models import Fcuser
from django.http import Http404
from django.core.paginator import Paginator
from tag.models import Tag
# Create your views here.


# 몇번째 글을 불러왔는 지 구분해주는 기능으로 pk인데 주소로부터 /1. /2 이렇게 받으려면 함수의 인자에 써줘야 한다.
def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk) # 인자로 입력받은 pk를 보드모델에 자동으로 생성된 pk에 넣어서 그 정보들을 갖게됨
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')

    return render(request, 'board_detail.html', {'board': board})


def board_write(request):
    # 로그인 자체를 안해서 user가 없을 때 로그인페이지로 보내는 기능
    if not request.session.get('user'):
        return redirect('/fcuser/login/')
    if request.method == 'POST': # 글쓰기를 통해 제목정보와 내용정보를 보냈을 때 
        form = BoardForm(request.POST) # 포스트 일 때는 데이터를 넣어줘야됨
        if form.is_valid():
            user_id = request.session.get('user') # 로그인을 했으면 아이디는 세션에 저장된다. 그래서 세션에서 유저아이디를 가져옴
            fcuser = Fcuser.objects.get(pk=user_id)

            board = Board() # 모델 변수를 만듦. 그럼 이 변수를 통해 데이터베이스에 접근 할 수 있게 됨
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = fcuser
            board.save()
            # 보드가 생성이 된 후 저장을 해야 id값(pk)이 생성이 된다. 그 다음에 추가해서 사용이 가능하다.

            # 태그가 forms.py의 파일을 통해 입력이 될 때 그 태그를 데이터 베이스에 저장하기 위해서 뷰에서 관리한다
            tags = form.cleaned_data['tags'].split(',')
            for tag in tags:
                if not tag:
                    continue
           # 태그를 전부 다 가져와서 Tag모델 안에 있던 name을 for문에서 입력한 tag와 비교해서 있으면 가져오고 없으면 생성해서 가져온다는 뜻.
                _tag, _ = Tag.objects.get_or_create(name=tag) # 태그 모델안에 있는 name과 클라이언트가 입력한 tag가 맞는 것만해서 보고 있으면 get가져오고 없으면 create 만든다
                                                                # 그리고 _tag 뒤에 있는 _는 파이썬에서는 사용을 하지 않는 변수입니다라는 뜻이지만 _이러한 모양이 아니라면 새로 생성된건지 원래 있던건지를 판별해줌(True, False값만 가짐)
                board.tags.add(_tag)  # board라는 인스턴스 객체가 생성돼서 저장까지 돼야 사용가능한 코드
            return redirect('/board/list/')
    else:
        form = BoardForm()
    return render(request, 'board_write.html',{'form':form})


def board_list(request):
    all_boards = Board.objects.all().order_by('-id') # Board의 모든 것들을 가지고 와서 boards라는 변수에 넣겠다는 뜻이며 -id라는 뜻은 id의 역순, 즉 최근에 만들어진 글을 가져오겠다 라는 뜻
    page = int(request.GET.get('p', 1)) # GET은 겟 형태로 받겠다는 말이고 get는 그냥 get이라는 함수 / p라는 값으로 받을 것이고 만약에 없으면 1번 값으로
    paginator = Paginator(all_boards, 2)  # 전체 오브젝트(all_boards)를 넣어주고 한페이지에 몇개씩 나오게 할 것인지 정함
    boards = paginator.get_page(page)
    return render(request, 'board_list.html',{'boards':boards}) # 최신글만 가져와서 담은 변수를 템플릿에 전달하겠다
                                                                # 페이지네이터를 사용하기 전에는 쿼리셋을 이용해 가져왔지만 페이지네이터를 사용해서 페이지 형식으로 가져온다.
                                                                # 그래서 boards안에 해당 페이지에 대한 정보들을 다 담아 두게 되는 기능 = 페이지네이터