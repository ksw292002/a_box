from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Sign Up, Upload를 위한 model form
from .forms import SigninForm, SignUpForm

# access control을 위한 decorator 참조용
from django.contrib.auth.decorators import login_required

# Sign Up을 위한 User Model 참조와 Sign In function
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# S3의 연결(Bucket 생성, 파일 업로드)과 관련된 기능
from .s3_manager import createUserBucket, uploadFile, getFileUrl

# Create your views here.


def signUp(request) :
    if(request.method == "POST") :
        form = SignUpForm(request.POST)
        
        # form 자체에서 유효성 검사
        if(form.is_valid()) :
            # **form.cleaned_data : 유효성 및 파이썬 반환을 고려해
            # request.POST로 접근하는 것 보다 이 방법을 권장한다.
            new_user = User.objects.create_user(**form.cleaned_data)

            # DynamoDB 안쓰는걸로
            # 그리고 그 이름으로 s3에 bucket을 생성
            createUserBucket(request.POST['username'])

            login(request, new_user)
            return redirect('main')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', context={'form': form})




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



