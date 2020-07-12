from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserRegisterForm, ImageForm
from .models import UserProfile, User
from django.views.generic import View


def register(request):
    if request.user.is_authenticated:
        return redirect('user_dash')
    else:
        form = UserRegisterForm()
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                messages.success(request, f'Account created for {username}')
                return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'html/register.html', {'form' : form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('user_dash')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if username == "admin" or username == "Admin":
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}")
                    return redirect('admin_panel')
                else:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}")
                    return redirect('user_dash')
            else:
                messages.error(request, "Invalid username. Try Again!!")
                context = {}
                return render(request, 'html/login.html', context)
        context = {}
        return render(request, 'html/login.html', context)


@login_required(login_url='login')
def user_dash(request):
    user_= UserProfile.objects.values()
    log_user = request.user.userprofile
    form = ImageForm(instance=log_user)
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=log_user)
        if form.is_valid():
            form.save()

    return render(request, 'html/user_dash.html', context={'user_': user_, 'form': form})


@login_required(login_url='login')
@staff_member_required
def admin_page(request):
    users = User.objects.exclude(username__startswith="admin").select_related('userprofile')
    return render(request, 'html/admin.html', context={'users':users})


def user_logout(request):
    logout(request)
    return redirect('login')


class DeleteUser(View):
    def get(self, request):
        d_id = request.GET.get('id', None)
        User.objects.get(id=d_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class DeletePic(View):
    def get(self, request):
        user_id = request.GET.get('id', None)
        img = UserProfile.objects.filter(id=user_id).update(profile_pic="Download.png")
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class DisapproveUser(View):
    def get(self, request):
        d_id = request.GET.get('id', None)
        get_user = User.objects.get(id=d_id)
        get_user.is_active = False
        get_user.save()
        user = User.objects.values()
        data = {
            'disapproved': True
        }
        return JsonResponse(data)


class ApproveUser(View):
    def get(self, request):
        d_id = request.GET.get('id', None)
        get_user = User.objects.get(id=d_id)
        get_user.is_active = True
        get_user.save()
        user = User.objects.values()
        data = {
            'approved': True
        }
        return JsonResponse(data)