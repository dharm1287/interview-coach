from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import InterviewSession, Question, Answer
from .forms import StartSessionForm, AnswerForm
from . import ai_utils, audio_utils
from django.conf import settings
import tempfile


def home(request):
    if request.method == 'POST':
        form = StartSessionForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            level = form.cleaned_data['level']
            session = InterviewSession.objects.create(user=request.user if request.user.is_authenticated else None, role=role, level=level)
            return redirect('interview', session_id=session.id)
    else:
        form = StartSessionForm()
    return render(request, 'core/home.html', {'form': form})


def interview(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    question = Question.objects.filter(session=session).last()
    if not question:
        q_text = ai_utils.generate_question(session.role, session.level)
        question = Question.objects.create(session=session, text=q_text)

    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer_text = form.cleaned_data.get('answer') or ''
            audio_file = form.cleaned_data.get('audio')
            ans = Answer(question=question, transcript=answer_text)
            if audio_file:
                ans.audio.save(audio_file.name, audio_file)
                # transcribe
                temp_path = ans.audio.path
                transcript = audio_utils.transcribe_file(temp_path)
                ans.transcript = transcript
            # evaluate
            feedback = ai_utils.evaluate_answer(question.text, ans.transcript or answer_text, session.role)
            ans.feedback = feedback
            ans.save()
            return render(request, 'core/feedback.html', {'feedback': feedback, 'question': question, 'answer': ans})
    else:
        form = AnswerForm()

    return render(request, 'core/interview.html', {'session': session, 'question': question, 'form': form})


def history(request):
    sessions = InterviewSession.objects.all().order_by('-created_at')
    return render(request, 'core/history.html', {'sessions': sessions})
