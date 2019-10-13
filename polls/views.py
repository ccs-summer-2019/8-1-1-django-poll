from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice
from .forms import QuestionForm

# def index(request):
#     question_list = Question.objects.all()
#     context = {
#         'question_list': question_list
#     }
#     return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # instead of using object_list
    context_object_name = 'question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.all()

# def detail(request, question_id):
#     # question = Question.objects.get(pk=question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     context = {'question': question}
#     return render(request, 'polls/detail.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

# def results(request, question_id):
#     # return HttpResponse("Results for question #%s" % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     # print(question.choice_set.all())
#     return render(request, 'polls/results.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def create_view(request):
#     form = QuestionForm()
#     return render(request, 'polls/create.html', {'form': form})

class CreateView(generic.CreateView):
    model = Question
    fields = '__all__'
    template_name = 'polls/create.html'

# class DeleteView(generic.DeleteView):
#     model = Question
#     success_url = reverse_lazy('polls:index')

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
