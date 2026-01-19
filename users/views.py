from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.views.generic import FormView, View
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from .forms import CustomUserCreationForm

User = get_user_model()

class LoginView(BaseLoginView):
    """
    Custom login view that uses auth-kit's cookie-based authentication.
    """
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()
        login(self.request, user)
        
        # For AJAX requests, return JSON response
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'redirect': self.get_success_url(),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)


class LogoutView(View):
    """
    Logout view that clears the session and redirects to the login page.
    """
    def post(self, request, *args, **kwargs):
        logout(request)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'redirect': reverse_lazy('login')
            })
        return redirect('login')


class RegisterView(FormView):
    """
    View for user registration.
    """
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        form.save()
        
        # Auto-login after registration
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'redirect': self.get_success_url(),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)
