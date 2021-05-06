from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..forms import AnswerForm
from ..models import Question, Answer


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}  # <------ so 추가
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    #page_b = request.GET.get('page', '1')  # 페이지
    so_answer = request.GET.get('so_answer', 'recent')  # 정렬기준
    question = get_object_or_404(Question, pk=question_id)
    
    # 정렬
    if so_answer == 'recommend':
        answer_list = Answer.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so_answer == 'popular':
        answer_list = Answer.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        answer_list = Answer.objects.filter(question=question).order_by('-create_date')
    
    #paginator_b=Paginator(answer_list, 10)
    #page_obj_b=paginator_b.get_page(page_b)


    context = {'question': answer_list, 'so_answer' : so_answer}
    #context={'answer_list': page_obj_b, 'page': page_b,'so_answer' : so_answer}
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question, 'so' : so}
    """
    return render(request, 'pybo/question_detail.html', context)
