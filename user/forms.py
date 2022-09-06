from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.db import models


User = get_user_model()



class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        error_messages={"required": "이메일을 입력해주세요."}, max_length=64, label="이메일"
    )
    username = forms.CharField(
        error_messages={"required": "유저이름을 입력해주세요."},
        label="유저명",
    )
    password1 = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput,
        label="비밀번호",
    )
    password2 = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput,
        label="비밀번호 확인",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


# 로그인 폼에 대한 클래스, 로그인/ID/Password에 대한 Validation 처리 포함
# 로그인 폼과 로그인 화면에서 입력된 사용자ID와 비밀번호를 받아 유효성 검증!!
# class LoginForm(forms.Form):


class LoginForm(forms.ModelForm):
    """ 로그인 폼에 대한 클래스 """
    
    # 지정사항
    # TODO: 2. login 할 때 form을 활용해주세요

    class Meta:
        model = User
        fields = {"username", "password"}
        widgets = {
            "username": forms.TextInput(attrs={"style": "width:270px;"}),       # 사용자ID 위젯
            "password": forms.PasswordInput(attrs={"style": "width:270px;"}),   # 비밀번호 위젯
        }



    # 입력된 사용자ID가 기존에 기 등록된 회원인지 확인!!
    # 기존 등록된 회원일 경우 validationError 발생!!
    # 등록된 회원이 아닐 경우 미등록되었다고 메시지 발생!!

    def clean__Username(self):
        username = self.cleaned_data.get("username")
        try:
            User.objects.get(username=username)
            return username
        except models.User.DoesNotExist:
            self.add_error("username", forms.ValidationError("User ID is not registered"))



    # 사용자ID 정상적 입력 시 입력된 비밀번호 확인!!
    # 기존 등록된 ID, Password 일 경우 validationError 발생!!

    def clean(self):
        password = self.cleaned_data.get("password")    # 비밀번호 입력 받기
        username = self.cleaned_data.get("username")    # 사용자ID 입력 받기
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is incorrect!"))
        except User.DoesNotExist:
            self.add_error("username", forms.ValidationError("User ID is not registered!"))

        return super().clean()



# 로그인 입력 폼 완료 처리 (이상 없을 경우 표시
# Django 파일들간(py-html 등)에 연동처리 이상없는지 크로스 체크 할 것!!!

        