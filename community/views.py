from django.shortcuts import render, redirect, get_object_or_404
from .models import Community, Comment
from .forms import CommunityForm, CommentForm
# DVDH
from django.views.decorators.http import require_POST
from IPython import embed
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.core.paginator import Paginator

from django.http import JsonResponse

from datetime import datetime

# Create your views here.
def index(request):
    #embed()
    articles = Community.objects.all().order_by('-pk')
    # 1. Paginator(전체 리스트, 한 페이지당 개수)
    paginator = Paginator(articles, 10)
    # 2. 몇 번째 페이지를 보여줄 것인지 GET으로 받
    # 'articles/?page=3'
    page = request.GET.get('page')
    # 해당하는 페이지의 게시글만 가져오기
    articles = paginator.get_page(page)
    

    context = {
        'articles': articles
    }
    return render(request, 'community/index.html', context)

def detail(request, community_pk):
    article = get_object_or_404(Community, pk=community_pk)
    comment_form = CommentForm()
    # 1은 N을 보장할 수 없기 때문에 querySet(comment_set)형태로 조회해야한다.
    comments=article.comment_set.all()
    article.click # 조회수
    context = {
        'article': article,
        'comments':comments,
        'comment_form' : comment_form,
    }
    return render(request, 'community/detail.html', context)

@login_required
def create(request):
    if request.method == "POST":
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            myDate=datetime.now()
            formatedDate=myDate.strftime("%Y.%m.%d")
            
            article.date=formatedDate
            article.save()
            messages.success(request, '게시글 작성 완료')
            return redirect('community:detail', article.pk)
        else:
            messages.error(request,'잘못된 데이터를 넣었어')
    else:
        form = CommunityForm()
    context = {
        'form': form
    }
    return render(request, 'community/form.html', context)

@login_required
def update(request, community_pk):
    article = get_object_or_404(Community, pk=community_pk)
    if article.user.username == request.user.username:
        if request.method == "POST":
            form = CommunityForm(request.POST, instance=article)
            if form.is_valid():
                article = form.save()
                return redirect('community:detail', article.pk)
        else:
            form = CommunityForm(instance=article)
        context = {
            'form': form
        }
        return render(request, 'community/form.html', context)

@require_POST
@login_required
def delete(request, community_pk):
    article = get_object_or_404(Community, pk=community_pk)
    if article.user.username == request.user.username:
        article.delete()
        return redirect('community:index')

@login_required
@require_POST
def comment_create(request,community_pk):
    #article = Community.objects.get(pk=article_pk)
    article=get_object_or_404(Community, pk=community_pk)

    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        #comment.article=article 주석한다
        #comment.article_id(자동으로 만들어줌) = article.pk
        comment.article_id = community_pk
        comment.save()
        return redirect('community:detail', community_pk)
    else:
        context={
            'comment_form' : comment_form,
            'article' : article
        }
    return redirect('community:detail', context)

@login_required
@require_POST
def comment_delete(request, community_pk, comment_pk):
    comment=get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('community:detail',community_pk)

@login_required
def like(request, community_pk):
    # 특정 게시물에 대한 정보
    article = get_object_or_404(Community, pk=community_pk)
    # 좋아요를 누른 유저에 대한 정보
    user = request.user
    # 사용자가 게시글의 좋아요 목록에 있으면 지우고 없으면 추가한다.
    if user in article.like_users.all():
        article.like_users.remove(user)
        liked=False
    else:
        article.like_users.add(user)
        liked=True
    context={
        'liked':liked,
        'count':article.like_users.count(),
    }
    return JsonResponse(context)

@login_required
def recommend(request, community_pk):
    article = get_object_or_404(Community, pk=community_pk)
    user = request.user
    if user in article.recommend_users.all():
        article.recommend_users.remove(user)
    else:
        article.recommend_users.add(user)
    return redirect('community:index')

def border_search(request):
    br = Community.objects.all() # 모든 Border 테이블의 모든 object들을 br에 저장하라

    b = request.GET.get('b','') # GET request의 인자중에 b 값이 있으면 가져오고, 없으면 빈 문자열 넣기

    if b: # b에 값이 들어있으면 true
        br = br.filter(title__icontains=b) # 의 title이 contains br의 title에 포함되어 있으면 br에 저장

    return render(request, 'community/border_search.html', { 'border_search':br , 'b':b})
    # br에는 Border 테이블에 title 이름이 'Singapore'인 데이터들이 들어있고,
    # b에는 내가 처음에 입력했던 'Singapore'가 들어있다.