# DAY ONE

## STEP ONE

Create a project folder, move into the project folder, and install Django.

If you're cloning a repo from GitHub, you do not need to create a new directory. Use the one that was created when you ran `git clone <ssh key>`).
```
mkdir <project_name>
cd <project_name>
pipenv install django
```
## STEP TWO

Activate the shell
```
pipenv shell
```

## STEP THREE

Start a new Django project ¡DON'T FORGET THE PERIOD!
```
django-admin startproject <project_name> .
```
Let's take a look at what `startproject` created for you.

These files are:

* The outer **<project_name>/** root directory is just a container for your project. Its name doesn’t matter to Django; you can rename it to anything you like.
* manage.py: A command-line utility that lets you interact with this Django project in various ways. You can read all the details about **manage.py** in [django-admin and manage.py](https://docs.djangoproject.com/en/2.2/ref/django-admin/).
* The inner **<project_name>/** directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. **mysite.urls**).
* **mysite/__init__.py**: An empty file that tells Python that this directory should be considered a Python package. If you’re a Python beginner, read [more about packages](https://docs.python.org/3/tutorial/modules.html#tut-packages) in the official Python docs.
* **mysite/settings.py**: Settings/configuration for this Django project. [Django settings](https://docs.djangoproject.com/en/2.2/topics/settings/) will tell you all about how settings work.
* **mysite/urls.py**: The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in [URL dispatcher](https://docs.djangoproject.com/en/2.2/topics/http/urls/).
* **mysite/wsgi.py**: An entry-point for WSGI-compatible web servers to serve your project. See [How to deploy with WSGI](https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/) for more details.

## STEP FOUR

Verify your Django project works.
```
python manage.py runserver
```

Django created migrations when you setup your project. It's a good idea at this point to go ahead apply those migrations. Run the following command in the terminal:
```
python manage.py migrate
```

The migrate command looks at the **INSTALLED_APPS**  setting and creates any necessary database tables.

## STEP FIVE

Create an application.
```
python manage.py startapp <app_name>
```
Tell Django to use the app you created by adding it to the list of **INSTALLED APPS** in the `<project_name>/settings.py` file:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '<app_name>', // newly create app name goes here
]
```
## STEP SIX

Let’s write the first view. Open the file `polls/views.py` and put the following Python code in it:
```
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```
This is the simplest view possible in Django. To call the view, we need to map it to a URL - and for this we need a URLconf.

## STEP SEVEN

To create a URLconf in the polls directory, create a file called urls.py.

In the polls/urls.py file include the following code:
```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
## STEP EIGHT

Point the root URLconf at the `polls.urls` module. In `mysite/urls.py`, add an import for `django.urls.include` and insert an `include()` in the `urlpatterns` list:
```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```
## STEP NINE

Define your models in the `<app_name>/models.py`:
```
from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    # you can use an optional first positional arg to a Field
    # to designate a human-readable format
    pub_date = models.DateTimeField('date published', default=timezone.now)


    def __str__(self):
          return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
          return self.choice_text
```
Now we need to **makemigrations**.
```
python manage.py makemigrations polls
```
Migrations are how Django stores changes to your models.

Before we migrate, let's see what SQL that migration would run.
```
python manage.py sqlmigrate polls 0001
```
Now, let's run the migration to our database.
```
python manage.py migrate
```
Essentially, this syncs the changes you've made to your models with the schema in the database.

## STEP TEN

Let's check out the Django admin:
```
python manage.py createsuperuser
```
Start the server and navigate to `http://127.0.0.8000/admin`.

Oops. We forgot to register the app. Add the following to `polls/admin.py`
```
from django.contrib import admin

from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)
```

## LET'S WRITE SOME MORE VIEWS

```

def index(request):
    return HttpResponse("Hello, world!")

def detail(request, question_id):
    return HttpResponse("Details for question #%s" % question_id)

def results(request, question_id):
    return HttpResponse("Results for question #%s" % question_id)

def vote(request, question_id):
    return HttpResponse("Voting for question #%s" % question_id)
```

## WIRE THE VIEWS INTO THE PROJECT

```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # variable name url pattern
    # will be sent as a keyword arg to the view
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

]
```

## WRITE VIEWS THAT PULL DATA FROM THE DATABASE
```
def index(request):
    question_list = Question.objects.all()
    # join list into a string
    output = '<br/>'.join([q.question_text for q in question_list])
    return HttpResponse(output)
```
## TIME FOR TEMPLATES

Create a templates/polls directory in your polls app - by convention, DjangoTemplates looks for a templates subdirectory in each of the **INSTALLED_APPS**.
```
{% if question_list %}

  <ul>
    {% for question in question_list %}
    <li><a href="/polls/{{ question.id }}/">{{question.question_text}}</a></li>
    {% endfor %}
  </ul>

{% else %}

  <p>No polls available</p>

{% endif %}
```
## LET'S UPDATE OUR VIEWS
```
from django.shortcuts import render

def index(request):
    question_list = Question.objects.all()
    context = {
        'question_list': question_list
    }
    return render(request, 'polls/index.html', context)
```
## CREATE A DETAIL VIEW
```
from django.shortcuts import render, get_object_or_404

def detail(request, question_id):
    # question = Question.objects.get(pk=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'polls/detail.html', context)
```
```
{{question}}
```
## ADD STYLES

Create a static/polls directory in your polls app and add a `styles.css` file.
```
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static 'polls/styles.css' %}">
```

# DAY TWO

## Removing hardcoded URLs in templates:
```
<ul>
  {% for question in question_list %}
  <li><a href="{% url 'polls:detail' question.id %}">{{question.question_text}}</a></li>
  {% endfor %}
</ul>
```
Make sure to add namespace in the project urls:
```
urlpatterns = [
    path('polls/', include('polls.urls', namespace='polls'),),
    path('admin/', admin.site.urls),
]
```
Update your app urls.py
```
app_name = 'polls'
```
## Write a simple form

<!-- polls/templates/polls/detail.html¶ -->
```
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
{% endfor %}
<input type="submit" value="Vote">
</form>
```
* Form displays a radio button for each question choice
* Using method="post"
* forloop.counter indicates how many times the for tag has gone through its loop
* Cross Site Request Forgeries, Django comes with a very easy-to-use system for protecting against it.

* XSS enables attackers to inject client-side scripts into webpages

## Update the vote view
```
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```
* request.POST is a dictionary-like object that lets you access submitted data by key name
* request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data.

## Add a results url
```
urlpatterns = [
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('', views.index, name='index'),
]
```
## Add a results.html
```
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```
# DAY THREE

Use generic views: Less code is better!

```
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # instead of using object_list
    context_object_name = 'question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.all()

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
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

```
```
  path('', views.IndexView.as_view(), name='index'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
  path('<int:question_id>/vote/', views.vote, name='vote'),
```
```
class CreateView(generic.CreateView):
    model = Question
    fields = '__all__'
    template_name = 'polls/create.html'
```
```
path('new/', views.CreateView.as_view(), name='create'),
```
```
<form method='post'>
  {% csrf_token %}
  {{form.as_p}}
  <button>Submit</button>
</form>
```
```
from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
```
