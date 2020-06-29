from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('community:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    else: 
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            # AuthenticationForm은 ModelForm이 아닌 Form을 상속하기 때문에 생긴게 달라진다.
            # 별도로 정의된 Model이 없다는 뜻 => 고로 넘겨주는 인자가 달라진다.
            if form.is_valid():
                # 로그인은 DB에 뭔가 작성하는 것은 동일하지만 연결된 모듈이 있는 것은 아니다.
                # 그럼 확인해야 하는것은?
                #   => 세션과 유저정보를 확인해야 하기때문에
                #   => 세션(request)와 유저정보(form.get_user())를 확인해야 한다.
                auth_login(request, form.get_user())
                return redirect(request.GET.get('next') or 'community:index')
        else:
            form = AuthenticationForm
        context = {
            'form' : form
        }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('community:index')

@require_POST
def delete(request):
    request.user.delete()
    return redirect('community:index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('community:index')
    else:
        form = CustomUserChangeForm(instance = request.user)
    context={
        'form' : form
    }
    return render(request, 'accounts/update.html', context)

@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('community:index')
    else :
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/password.html', context)

def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context={
        'person' : person
    }
    return render(request, 'accounts/profile.html', context)

def follow(request, user_pk):
    # person에 담긴 user_pk값을 가진 유저는
    # 프로필의 주인이다.
    # request.user는 나. 요청을 보내온 사용자이다
    person = get_object_or_404(get_user_model(), pk=user_pk)
    if request.user in person.followers.all():
        person.followers.remove(request.user)
    else :
        person.followers.add(request.user)
    return redirect('accounts:profile',person.username)