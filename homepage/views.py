from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import ProfileUser
from .models import Comment
from . import forms
from django.db.models import Q
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def find_master(request):
    search_query = request.GET.get('search', '')
    filter_price = forms.ProfileFilterForm(request.GET)
    if search_query:
        people = ProfileUser.objects.filter(
            Q(type_service__icontains=search_query) | Q(
                address__icontains=search_query))
    else:
        people = ProfileUser.objects.all()

    if filter_price.is_valid():
        if filter_price.cleaned_data["min_price"]:
            people = ProfileUser.objects.filter(
                price__gte=filter_price.cleaned_data["min_price"])
        if filter_price.cleaned_data["max_price"]:
            people = ProfileUser.objects.filter(
                price__lte=filter_price.cleaned_data["max_price"])
    else:
        people = ProfileUser.objects.all()
    return render(request,
                  'people/find_master.html',
                  {"people": people,
                   "filter_price": filter_price,
                   }
                  )


def people_details(request, id_):
    profile = get_object_or_404(ProfileUser,
                                id=id_,
                                )
    reviews = Comment.objects.filter(profile=id_)
    average = reviews.aggregate(Avg('rating'))['rating__avg']
    if average is None:
        average = 0
    average = round(average, 2)

    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.profile = profile
            new_comment.save()
            return redirect(profile)
    else:
        comment_form = forms.CommentForm()
    return render(request,
                  'people/detail.html',
                  {'profile': profile,
                   'comment_form': comment_form,
                   'average': average,
                   })


def start_page(request):
    return render(request,
                  'people/start_page.html',
                  )


def registration_confirmation(request):
    return render(request,
                  'registration/registration_confirmation.html')


def register(request):
    if request.method == 'POST':
        user_form = forms.UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            ProfileUser.objects.create(user=new_user)
            return render(request, 'register_done.html',
                          {'new_user': new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


@login_required
def view_profile(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def create_profile(request):
    return render(request, 'create_profile.html')


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = forms.UserEditForm(request.POST,
                                       instance=request.user,
                                       )
        profile_form = forms.ProfileEditForm(request.POST,
                                             instance=request.user.profileuser,
                                             files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'profile.html', {'user': request.user})

    user_form = forms.UserEditForm(instance=request.user)
    profile_form = forms.ProfileEditForm(instance=request.user.profileuser)
    return render(request,
                  'edit.html',
                  {'profile_form': profile_form,
                   'user_form': user_form})
