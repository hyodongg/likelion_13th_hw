from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *

# Create your views here.


def mainpage(request):
    context = {
        "generation": 13,
        "info": {"weather": "좋음", "feeling": "배고픔(?)", "note": "아기사자 화이팅!"},
        "shortKeys": [
            "들여쓰기: Tab",
            "내어쓰기: Shift + Tab",
            "주석처리: 윈도우-Ctrl + /, 맥-command + /",
            "자동정렬: Shift + Alt + F or Ctrl + K + F",
            "한줄이동: Alt + 방향키(위/아래)",
            "한줄삭제: Ctrl + Shift + k or Ctrl + x",
            "같은단어전체선택: Ctrl + Shift + L",
        ]
    }
    return render(request, "main/mainpage.html", context)


def secondpage(request):
    posts=Post.objects.all()
    return render(request, "main/secondpage.html",{'posts':posts})

def new_post(request):
    return render(request,'main/hdpost.html')

def detail(request,id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'main/detail.html',{'post': post})

def create(request):
    new_post = Post()

    new_post.title = request.POST['title']
    new_post.writer = request.POST['writer']
    new_post.content = request.POST['content']
    new_post.feeling = request.POST['feeling']
    new_post.created_time = timezone.now()
    new_post.updated_time = timezone.now()
    new_post.image=request.FILES.get('image')

    new_post.save()

    return redirect('main:detail',new_post.id)

def edit(request,id):
    edit_post=Post.objects.get(pk=id)
    return render(request,'main/edit.html',{"post":edit_post})

def update(request,id):
    update_post=Post.objects.get(pk=id)
    update_post.title=request.POST['title']
    update_post.writer=request.POST['writer']
    update_post.content=request.POST['content']
    update_post.feeling=request.POST['feeling']
    update_post.updated_time=timezone.now()
    update_post.image=request.FILES.get('image')
    update_post.save()
    return redirect('main:detail',update_post.id)

def delete(request,id):
    delete_post=Post.objects.get(pk=id)
    delete_post.delete()
    return redirect('main:secondpage')