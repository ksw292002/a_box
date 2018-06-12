from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Sign Up, Upload를 위한 model form
from .forms import SigninForm

# Create your views here.

# login을 뷰에 따로 구현하는 것에서 뷰이름을 'login'이면 안된다.
# 이미 login이 auth에 있고, 이를 우리는 사용해야 한다.
def signin(request) :
    if(request.method == "POST") :
        #form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if(user != None) :
            login(request, user)
            return redirect('/main/')
        else :
            # user를 찾지 못할 경우 or user 로그인에 실패한 경우
            return HttpResponse("Login Failed")

    else :
        form = SigninForm()
        return render(request, 'signin.html', context={'form':form})

def fileList(request) :
    return HttpResponse("good!")

