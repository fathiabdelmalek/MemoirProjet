import os.path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.core.mail import send_mail

from MemoirProjet import settings
from .models import Conference, Submission
from .forms import ConferenceCreationForm, ConferenceUpdateForm, SubmissionCreationForm, SubmissionUpdateForm
from .filters import ConferenceFilter


class IndexView(generic.ListView):
    model = Conference

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        conferences = Conference.objects.all()
        filter = ConferenceFilter(self.request.GET, queryset=conferences)
        conferences = filter.qs
        paginator = Paginator(conferences, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = conferences
        context['submission_list'] = Submission.objects.all()
        context['filter'] = filter
        context['page_obj'] = page_obj
        self.request.session['page'] = self.request.path
        return context


class ConferenceView(generic.DetailView):
    model = Conference
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submission_list'] = Submission.objects.filter(conference=self.kwargs['pk'])
        self.request.session['page'] = self.request.path
        return context


@method_decorator(login_required, name='dispatch')
class ConferenceCreationView(generic.CreateView):
    model = Conference
    form_class = ConferenceCreationForm

    def form_valid(self, form):
        conference = form.save(commit=False)
        conference.organizer = self.request.user
        conference.save()
        messages.success(self.request, "Conference created successfully")
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class ConferenceUpdateView(generic.UpdateView):
    model = Conference
    form_class = ConferenceUpdateForm
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Conference updated successfully")
        return redirect(self.request.session['page'])


@login_required()
def delete_conference(request, pk):
    Conference.objects.filter(id=pk).delete()
    messages.success(request, "Conference deleted successfully")
    return redirect(request.session['page'])


@method_decorator(login_required, name='dispatch')
class SubmissionCreationView(generic.CreateView):
    model = Submission
    form_class = SubmissionCreationForm
    pk_url_kwarg = 'conf_pk'

    def form_valid(self, form):
        submission = form.save(commit=False)
        submission.user = self.request.user
        submission.conference = Conference.objects.get(id=self.kwargs['conf_pk'])
        submission.save()
        messages.success(self.request, 'Your submission to subscribe has been created successfully')
        message = " I'm "
        message += str(submission.user)
        message += " have submitted to join in your conference "
        message += str(submission.conference)
        send_mail(
            'Submission for your Conference',
            message,
            [submission.user.email],
            [submission.conference.organizer.email]
        )
        return redirect(self.request.session['page'])


@method_decorator(login_required, name='dispatch')
class SubmissionUpdateView(generic.UpdateView):
    model = Submission
    form_class = SubmissionUpdateForm
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Submission updated successfully")
        return redirect(self.request.session['page'])


@login_required()
def delete_submission(request, pk):
    Submission.objects.filter(id=pk).delete()
    messages.success(request, "Submission deleted successfully")
    return redirect(request.session['page'])


@login_required()
def accept_submission(request, pk):
    submission = Submission.objects.get(id=pk)
    submission.status = 1
    submission.save()
    message = " We have seen and reviewed your submission in our conference "
    message += str(submission.conference)
    message += ", and we accepted it "
    send_mail(
        'Submission Accepted',
        message,
        submission.conference.organizer.email,
        [submission.user.email]
    )
    messages.success(request, 'The submission has ben accepted successfully')
    return redirect(request.session['page'])


@login_required()
def refuse_submission(request, pk):
    submission = Submission.objects.get(id=pk)
    submission.status = 2
    submission.save()
    message = " We have seen and reviewed your submission in our conference "
    message += str(submission.conference)
    message += ", and we refused it "
    send_mail(
        'Submission Accepted',
        message,
        submission.conference.organizer.email,
        [submission.user.email]
    )
    messages.success(request, 'The submission has ben refused successfully')
    return redirect(request.session['page'])


@login_required()
def confirm_submission(request, pk):
    submission = Submission.objects.get(id=pk)
    submission.status = 3
    submission.save()
    message = " Congrats, we have confirmed your submission in our conference "
    message += str(submission.conference)
    send_mail(
        'Submission Confirmed',
        message,
        submission.conference.organizer.email,
        [submission.user.email]
    )
    messages.success(request, 'The submission has ben confirmed successfully')
    return redirect(request.session['page'])


def download(request, path):
    path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/article")
            response['Content-Disposition'] = 'inline;filename='+os.path.basename(path)
            return response
        raise Http404


def error_404_handler(request, exception):
    return render('404.html')
