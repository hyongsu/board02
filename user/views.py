from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse

from .forms import LoginForm, RegisterForm



# User 리스트 초기화

User = []


# User로 입력받기 위함 함수 호출

User = get_user_model()



# 우선, 메인 페이지(index.html)에 대한 함수 지정

def index(request):
    return render(request, "index.html")



# 다음으로, 사용자 등록(register_view)하고 로그인 페이지(RegisterForm)로 이동 처리하는 함수 지정

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})



# 그 다음, 로그인 페이지(login_view()) 함수 지정

def login_view(request):
    if request.method == "POST":
        # 지정사항
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요

        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")     # 사용자ID를 POST로 받기
            password = request.POST.get("password")     # 비밀번호를 PIST로 받기
            user = authenticate(request, username=username, password=password)
            if user is None:
                return redirect(reverse("login"))       # user가 없을 경우 다시 login으로 redirect 처리
            login(request, user)
            return redirect(reverse("index"))           # user가 없을 경우 다시 index로 redirect 처리
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})   # LoginForm으로 받아 내용을 login.html로 뿌리기



# 다음으로, 로그아웃(logout_view()) 처리 함수

def logout_view(request):
    # 지정사항
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요.

    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse("index"))      # 지정된 user일 경우 index로 redirect 처리!!
    else:
        return redirect(reverse("login"))      # 지정된 user가 아닐 경우 login으로 redirect 처리!!



# 다음으로, 사용자 리스트에 대한 함수
# 지정사항
# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요.
# 특히 프로젝트 환경설정(settings.py)에 LOGIN_URL 설정이 반드시 필요!!!


@login_required
def user_list_view(request):
    users = User.objects.all()

    # 지정사항
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요

    paginator = Paginator(users, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "users.html", {"users": page_obj})



# 마지막으로 페이징을 확인하기 위해 더미 사용자 20개 생성
# 지정위치 (사용유의) : localhost:8000/dummy/dummy/
# 등록된 유저는 @kt.com 도메인으로 임의 사용자 20개 생성

def create_dummy_users_view(request):
    users = []              # users 리스트 초기화 처리!!!
    for j in range(20):
        user = User(first_name='User%dFirstName' % j,
                    last_name='User%dLastName' % j,
                    username='user%d' % j,
                    email='user%d@kt.com' % j,
                    password='hashedPasswordStringPastedHereFromStep1!',
                    is_active=True,
                    )
        users.append(user)

    User.objects.bulk_create(users)

    return  render(request)




# 최종적으로 동작이 연동되어 잘 되는지 꼭 체크할 것!!!
# 다른 페이지에서 연동 페이지로 이동 시 오류여부 더블체크 할 것!!!





