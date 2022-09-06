from django.contrib import admin
from django.urls import path

from user.views import index, login_view, logout_view, register_view, user_list_view, create_dummy_users_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("users/", user_list_view, name="user_list"),
    
    path("dummy/", create_dummy_users_view,)          # 이 라인은 20개 User 등록을 위한 페이징 확인용 더미 사용자 생성에 필요!!!

]



# User 등록 잘 되는지 재확인하여 연동 세팅 할 것 (URL과 비교하여 지정)
# View-HTML-CSS 등과 크로스 체크 필요!!!!


