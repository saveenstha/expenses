from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages, auth
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth


# Create your views here.
class UserNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric values'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username in use, choose another one'}, status=409)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'},status=400)
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error': 'Sorry email in use, choose another one'},status=409)
        return JsonResponse({'email_valid': True})

# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self,request):
        # GET USER DATA
        # Validate
        #create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context ={
            'fieldValues': request.POST
        }

        if not User.objects.filter(username = username).exists():
            if not User.objects.filter(email = email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()

                # path_to_view
                # - getting domain we are on
                # - relative url to verification
                # - encode uid
                # - token

                uidb64 = force_bytes(urlsafe_base64_encode(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64':uidb64, 'token': token_generator.make_token(user)})
                activate_url = 'http://'+domain+link

                email_body = 'Hi' + user.username+" PLease use this link to verify your account\n"+ activate_url

                email_subject = 'Account Activation'

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@saveensth.com',
                    [email],

                )

                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')
        return render(request,'authentication/register.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, '+user.username+' You are now logged in')
                    return redirect('expenses')
                messages.error(request, 'Account is not active, Please check your email.')
                return render(request, 'authentication/login.html')

            messages.error(request, 'Invalid Credentials. Try Again')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Please Fill all fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'you have been logged out')
        return redirect('login')

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST['email']
        if not validate_email(email):
            messages.error(request, "Please enter valid email.")
        return render(request, 'authentication/reset-password.html')
