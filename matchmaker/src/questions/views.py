from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UserResponseForm
from .models import Question, Answer, UserAnswer

# Create your views here.

def single(request, id):

	if request.user.is_authenticated():

		queryset = Question.objects.all().order_by('-timestamp')
		instance = get_object_or_404(Question, id = id)

		try:
			user_answer = UserAnswer.objects.get(user = request.user, question = instance)
		except UserAnswer.DoesNotExist:
			user_answer = UserAnswer()
		except UserAnswer.MultipleObjectsReturned:
			user_answer = UserAnswer.objects.filter(user = request.user, question = instance)[0]
		except:
			user_answer = UserAnswer()

		form = UserResponseForm(request.POST or None)
		if form.is_valid():
			print form.cleaned_data
			#print request.POST
			
			questions_id = form.cleaned_data.get('question_id')

			answer_id = form.cleaned_data.get('answer_id')
			importance_level = form.cleaned_data.get('importance_level')
			their_importance_level = form.cleaned_data.get('their_importance_level')
			their_answer_id = form.cleaned_data.get('their_answer_id')

			question_instance = Question.objects.get(id = questions_id)
			answer_instance = Answer.objects.get(id = answer_id)
			


			# print question_instance.text, answer_instance.text
			
			user_answer = UserAnswer()
			user_answer.user = request.user

			user_answer.question = question_instance

			user_answer.my_answer = answer_instance
			user_answer.my_answer_importance = importance_level

			if their_answer_id != -1:
				their_answer_instance = Answer.objects.get(id = their_answer_id)
				user_answer.their_answer = their_answer_instance
				user_answer.their_answer_importance = their_importance_level
			else:
				user_answer.their_answer_importance = "Not Important"

			user_answer.save()


			next_q = Question.objects.all().order_by("?").first()
			return redirect("question_single", id = next_q.id)



		context = {
			"form": form,
		    "instance": instance, 
		    "user_answer": user_answer,
		    #"queryset": queryset,
		}
		return render(request, "questions/single.html", context)
	else:
		raise Http404
		



def home(request):
	if request.user.is_authenticated():	
		form = UserResponseForm(request.POST or None)
		if form.is_valid():
			print form.cleaned_data
			questions_id = form.cleaned_data.get('question_id')
			answer_id = form.cleaned_data.get('answer_id')
			question_instance = Question.objects.get(id = questions_id)
			answer_instance = Answer.objects.get(id = answer_id)
			print question_instance.text, answer_instance.text

		queryset = Question.objects.all().order_by('-timestamp')
		instance = queryset[0]
		context = {
			"form": form,
		    "instance": instance, 
		    #"queryset": queryset,
		}
		return render(request, "questions/home.html", context)
	else:
		raise Http404









