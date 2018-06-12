from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Sign Up, Upload를 위한 model form
from .forms import SigninForm

# access control을 위한 decorator 참조용
from django.contrib.auth.decorators import login_required

# Sign Up을 위한 User Model 참조와 Sign In function
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

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


@login_required
def fileList(request) :
    # 현재 로그인중인 유저 객체를 받아옴.
    user = request.user

    storedfiles = user.storedfiles_set.order_by('-created_at', '-pk')

    ctx = {
        # template로 넘길 context 요소들
        'user': user,
        # 정렬된 데이터를 템플릿에 변수로서 넘김
        'storedfiles': storedfiles,

    }
    return render(request, 'filelist.html', ctx)

@login_required
def fileUpload(request) :
    return HttpResponse("Good!")