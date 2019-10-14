from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import QuestionForm, ChoiceFormSet
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

# class CreateView(generic.CreateView):
#     model = Question
#     template_name = 'polls/create.html'
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)

class CreateView(generic.CreateView):
    model = Question
    template_name = 'polls/create.html'
    form_class = QuestionForm
    success_url = 'polls/index/'

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = QuestionForm(self.request.POST)
            context['formset'] = ChoiceFormSet(self.request.POST)
        else:
            context['form'] = QuestionForm()
            context['formset'] = ChoiceFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['form']
        formset = context['formset']
        if all([form.is_valid(), formset.is_valid()]):
            form.instance.created_by = self.request.user
            question = form.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    choice = inline_form.save(commit=False)
                    choice.question = question
                    choice.save()
            return HttpResponseRedirect(reverse('polls:index',))

# def add_poll(request):
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         formset = ChoiceFormSet(request.POST)
#         if all([form.is_valid(), formset.is_valid()]):
#             form.instance.created_by = request.user
#             question = form.save()
#             for inline_form in formset:
#                 if inline_form.cleaned_data:
#                     choice = inline_form.save(commit=False)
#                     choice.question = question
#                     choice.save()
#             return render(request, 'polls/index.html', {})
#     else:
#         form = QuestionForm()
#         formset = ChoiceFormSet()
#
#     return render(request, 'polls/create.html', {'form': form,
#                                                    'formset': formset})

def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
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
