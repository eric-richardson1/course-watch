from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Course, UserWatchedCourse

# Create your views here.


@login_required
def dashboard(request):
    watched_courses = UserWatchedCourse.objects.filter(user=request.user)
    if request.method == 'POST':
        if 'search_query' in request.POST:
            search_query = request.POST['search_query']
            results = Course.objects.filter(subject__contains=search_query)
            return redirect(request=request, template_name="main/search_results.html", context={'query': search_query, 'results': results})


    return render(request, template_name="main/index.html", context={'watched_courses': watched_courses})


def register_request(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:dashboard")
        messages.error(request, "Registration unsuccessful.")
    form = CustomUserForm()
    return render(request, template_name="main/register.html", context={"register_form": form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}")
                return redirect("main:dashboard")
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Invalid email or password")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})

def search_results(request):
    if request.method == "POST":
        if 'course_watch' in request.POST:

            course_watch = request.POST['course_watch']
            course = Course.objects.get(pk=course_watch)
            UserWatchedCourse.objects.get_or_create(user=request.user, course=course,
                                                    defaults={
                                                        'user': request.user,
                                                        'course': course
        
                                                    })

    return render(request=request, template_name="main/search_results.html")
