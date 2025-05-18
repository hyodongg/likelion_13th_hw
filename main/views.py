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
    if request.method=='GET':
        comments=Comment.objects.filter(post=post)
        return render(request,'main/detail.html',{'post':post,'comments':comments})

    elif request.method=='POST':
        new_comment=Comment()
        new_comment.post=post
        new_comment.writer=request.user
        new_comment.content=request.POST['content']
        new_comment.pub_date=timezone.now()
        new_comment.save()
        return redirect('main:detail',id)

def create(request):
    if request.user.is_authenticated:
        new_post = Post()

        new_post.title = request.POST['title']
        new_post.writer = request.user
        new_post.content = request.POST['content']
        new_post.feeling = request.POST['feeling']
        new_post.created_time = timezone.now()
        new_post.updated_time = timezone.now()
        new_post.image=request.FILES.get('image')

        new_post.save()

        words=new_post.content.split()
        tag_list=[]

        for w in words:
            if len(w)>0:
                if w[0]=='#':
                    tag_list.append(w[1:])  
        for t in tag_list:
            tag,boolean=Tag.objects.get_or_create(name=t)
            new_post.tags.add(tag.id)

        return redirect('main:detail',new_post.id)
    else:
        return redirect('accounts:login')

def edit(request,id):
    edit_post=Post.objects.get(pk=id)
    return render(request,'main/edit.html',{"post":edit_post})

def update(request,id):
    update_post=Post.objects.get(pk=id)
    if request.user.is_authenticated and request.user==update_post.writer:
        update_post.title=request.POST['title']
        update_post.content=request.POST['content']
        update_post.feeling=request.POST['feeling']
        update_post.updated_time=timezone.now()
        
        words=update_post.content.split()
        tag_list=[]

        for w in words:
            if len(w)>0:
                if w[0]=='#':
                    tag_list.append(w[1:])
        for t in tag_list:
            tag,boolean=Tag.objects.get_or_create(name=t)
            update_post.tags.add(tag.id)

        if request.FILES.get('image'):
            update_post.image=request.FILES.get('image')
        update_post.save()
        return redirect('main:detail',update_post.id)
    return redirect('accounts:login',update_post.id)

def delete(request,id):
    delete_post=Post.objects.get(pk=id)
    delete_post.delete()
    return redirect('main:secondpage')

def delete_comment(request,id):
    comments = get_object_or_404(Comment,pk=id)
    post_id=comments.post.id
    comments.delete()
    return redirect('main:detail',post_id)

def tag_list(request): #모든 태그 목록을 볼 수 있는 페이지
    tags=Tag.objects.all()
    return render(request,'main/tag-list.html',{'tags':tags})

def tag_posts(request,tag_id): #특정 태그를 가진 게시글의 목록을 볼 수 있는 페이지
    tag=get_object_or_404(Tag,id=tag_id)
    posts=tag.posts.all()
    return render(request,'main/tag-post.html',{'tag':tag,'posts':posts})