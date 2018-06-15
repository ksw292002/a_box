from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Sign Up, Upload를 위한 model form
from .forms import SigninForm, SignUpForm, FileUpForm

# access control을 위한 decorator 참조용
from django.contrib.auth.decorators import login_required

# Sign Up을 위한 User Model 참조와 Sign In function
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# S3의 연결(Bucket 생성, 파일 업로드)과 관련된 기능
from .s3_manager import createUserBucket, uploadFile, getFileUrl, getFileList, deleteFile

# Create your views here.


def signUp(request) :
    #서원석
    #강상위
    #김재홍
    user = request.user
    if(request.method == "POST") :
        form = SignUpForm(request.POST)
        username = request.POST['username']


        # username 중복체크
        if(not(User.objects.filter(username=username).exists())) :
            # form 자체에서 유효성 검사
            if(form.is_valid()) :
                # **form.cleaned_data : 유효성 및 파이썬 반환을 고려해
                # request.POST로 접근하는 것 보다 이 방법을 권장한다.
                new_user = User.objects.create_user(**form.cleaned_data)

                # DynamoDB 안쓰는걸로
                # 그리고 그 이름으로 s3에 bucket을 생성
                createUserBucket(username)

                login(request, new_user)
                return redirect('main')
        # 중복이면
        else :
            form = SignUpForm()
            return render(request, 'a_box_app/signup.html', context={'form': form, 'user': user, 'chk':1,})
            
    else:
        form = SignUpForm()
        return render(request, 'a_box_app/signup.html', context={'form': form, 'user': user, 'chk':0})

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
            return redirect('/')

    else :
        user = request.user
        form = SigninForm()
        return render(request, 'a_box_app/signin.html', context={'form':form, 'user': user})


@login_required
def fileList(request) :

    # 현재 로그인중인 유저 객체를 받아옴.
    user = request.user

    # storedfiles = user.storedfiles_set.order_by('-created_at', '-pk')
    file_list = getFileList(user.username)

    # file name, key 리스트 만들기
    file_dict = {}
    for key in file_list :
        file_dict[key] = str(getFileUrl(user.username,key))

    ctx = {
        # template로 넘길 context 요소들
        'user': user,
        # 정렬된 데이터를 템플릿에 변수로서 넘김
        # 'storedfiles': storedfiles,
        'file_dict': file_dict,

    }
    return render(request, 'a_box_app/filelist.html', ctx)

@login_required
def fileUpload(request) :
    user = request.user
    # login 한 유저인지에 대한 여부
    # request.user의 is_authenticated() 메서드 사용 => X
    # user.is_authenticated => O
    # 메서드가 아니라 property로 바뀜.
    # bool값으로 반환함 => X => 그냥 자체로 property임.
    # if( not request.user.is_authenticated ) :
    #     return redirect(settings.LOGIN_URL)

    if(request.method == "GET") :
        form = FileUpForm()

    # 게시물 내용과 파일을 제출받는(??) 부분
    elif(request.method == "POST") :

        #  request.POST : form에서 다룰 데이터.
        #                 dict or similar to dict 여야 한다.
        #                 파일을 제외한 HTML에서 POST 방식으로 전송한
        #                 모든 form 데이터가 여기에 있다.
        # request.FILES : 파일은 여기에 있다.
        #
        # 그래서 두개로 나누어서 인자로 전달한 것이다.
        form = FileUpForm(request.POST, request.FILES)

        if(form.is_valid()) : # form 검증

            # form = FileUpForm이고
            # FileUpForm은 model과 연결되어 있으므로
            # 데이터를 저장하게 되는 것
            #
            # form이 ModelForm을 상속한 경우 save() 메서드를 가지고 있음.
            # 이 save() 메서드는 model의 save()와 같은 역할임.
            # data가 저장된 것을 반영한 model의 인스턴스를 반환

            # obj = form.save()
            # 즉, obj는 form에 연결되어 있는 model로 생성한 인스턴스이다.
            # commit=False 속성은 DB에 바로는 반영하지 말아달라고 하는 것.
            obj = form.save(commit=False)

            # 이유는 user에 대한 정보를 넘기기 위해서
            # 여러가지 보안상의 문제가 있지만, 여기서는 편하게
            # 잠시 commit=False로 하고 아래와 같인 직접 할당.
            obj.user = request.user

            # 그리고 최종 save()를 통해 유저정보까지 DB에 반영.
            obj.save()

            # Dynamo는 안쓰는걸로
            # username, file path 설정.
            # prefixing으로 파일이름만 추출
            username = request.user.username
            fpath = obj.content.path

            # file name 설정
            prefixing = 'content/'
            fname = obj.content.name.replace(prefixing,'')

            # 위의 변수들을 토대로 upload
            uploadFile(username, fname, fpath)

            # upload 후 delete
            obj.delete()

            # redirect는 지정한 URL로 이동(?)시킨다.
            # 만약 인자가 model의 인스턴스라면
            # 그 객체의 get_absolute_url() 실행
            return redirect('/main/')


    ctx = {
        # key : tempalte파일 안에서 쓰여지는 변수의 이름
        'form': form, 'user': user,
    }

    return render(request, 'a_box_app/upload.html', ctx)

# file deleting
@login_required
def fileDelete(request, fname) :
    # url에서 fname이 넘어오고
    # 이것을 토대로 s3에서 deleting을 불러온다.
    # 현재는 한글제외 숫자, 문자, -, . 문자로 이루어진 파일만 대응한다.
    deleteFile(request.user.username, fname)
    
    # 삭제 후 main으로 redirect
    return redirect('/main/')