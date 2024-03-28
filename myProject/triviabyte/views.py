from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import random
from .models import QuizCategory
from .models import Question


# Create your views here.
def triviabyte_view(request):
    context = {'categories' : QuizCategory.objects.all()}

    if request.GET.get('category'):
        return redirect(f"/questions/?category={request.GET.get('category')}")
    return render(request, 'index.html' , context)

def questions(request):
    context = {'category': request.GET.get('category')}
    return render(request, 'questions.html', context)

def get_questions(request):
    try:
        questions_items = Question.objects.all()
        if request.GET.get('category'):
            questions_items = questions_items.filter(category__name__icontains=request.GET.get('category'))
        data = []
        for question_obj in questions_items:
            data.append({
                "question_text" : question_obj.question_text,
                "category" : question_obj.category.name,
                "marks" : question_obj.marks,
                "answers" : question_obj.fetch_answers()
            })

        return JsonResponse({'status': True, 'data': data})

    except Exception as error:
        print(error)
        return HttpResponse("Invalid Entry")


def calculate_questions_score(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            # Retrieve the answers from the request
            answers = request.POST.getlist('answers[]')

            # Calculate the score based on the answers
            score = calculate_individual_score(answers)

            # Return the score as JSON response
            return JsonResponse({'score': score})

        except Exception as e:
            # Handle any exceptions that might occur during score calculation
            return JsonResponse({'error': str(e)}, status=500)

    else:
        # Return an error response if the request method is not POST or not AJAX
        return JsonResponse({'error': 'Invalid request'}, status=400)

def calculate_individual_score(answers):
    # Implement your score calculation logic here
    # This is just a placeholder, replace it with your actual logic
    score = len(answers) * 10  # Assuming each correct answer gives 10 points
    return score

def calculate_score(request):
    if request.method == 'POST':
        received_answers = request.POST.getlist('answers[]')  # Assuming answers are sent as a list
        # Calculate score based on received answers
        score = calculate_score_logic(received_answers)
        return JsonResponse({'score': score})
    else:
        return JsonResponse({'error': 'Invalid request method'})
