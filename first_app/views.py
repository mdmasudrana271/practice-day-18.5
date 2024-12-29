from django.shortcuts import render,redirect
from . import forms
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate,login,update_session_auth_hash,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import RegisterForm  
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login

# Create your views here.
@login_required
def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'user':request.user})
    else:
        return redirect('user_login')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm 
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save() # Save the user
        login(self.request, user)
        messages.success(self.request, 'Account created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with your submission.')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context



class UserLoginView(LoginView):
    template_name = 'register.html'
    # success_url = reverse_lazy('profile')
    def get_success_url(self):
        return reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, 'Logged In Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context


@login_required
def pass_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user,data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile Updated Successefully')
                update_session_auth_hash(request,form.user)
                return redirect('profile')

        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'change_pass.html', {'form':form})
    else:
        return redirect('user_login')    


@login_required
def pass_change_without_old(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SetPasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password changed Successefully')
                update_session_auth_hash(request,form.user)
                return redirect('profile')

        else:
            form = SetPasswordForm(user=request.user)
        return render(request, 'change_pass.html', {'form':form})
    else:
        return redirect('user_login')




@login_required
def user_logout(request):
    messages.success(request, 'Logged Out Successfully')
    logout(request)
    return redirect('user_login')
     
