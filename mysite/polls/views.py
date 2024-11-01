from http.client import responses

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound, \
    HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from .models import Question, Choice
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def register (request, name, age):
    return HttpResponse(f"""
        <h2>О пользователе</h2>
        <p>Имя: {name}</p>
        <p>Возраст: {age}</p>
    """)

def home (request):
    return HttpResponse('А я домашняя страница')

def index(request):
    bob = Person("bob", 41)
    return JsonResponse(bob, safe=False, encoder=PersonEncoder)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class PersonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if(isinstance(obj, Person)):
            return {"name": obj.name, "age": obj.age}
        return super().default(obj)

def access(request, age):
    if age not in range(1, 111):
        return HttpResponseBadRequest('Некорректные данные')
    if age > 17:
        return HttpResponse('Доступ разрешен')
    else:
        return HttpResponseForbidden("Доступ заблокирован: Недостаточно лет")

def set(request):
    username = request.GET.get("username", "Undefined")
    response = HttpResponse(f"Hello, {username}")
    response.set_cookie("username", username)
    return response

def about(request):
    return render(request, "polls/about.html")