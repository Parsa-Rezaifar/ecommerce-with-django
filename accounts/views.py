from . forms import User_RegistrationForm,Verification_CodeForm,User_LoginForm
from django.shortcuts import render,redirect
from django.contrib import messages
from . models import OtpCode,User
from utils import send_opt_code
from django.views import View
import random
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class User_RegistrationView(View) : # This class get user information and send a verification code to user phone number

    template_name = 'accounts/User_Registration_Form.html'
    form_class = User_RegistrationForm

    def get(self,request) :
        form = self.form_class()
        return render(request,self.template_name,context={'form':form})

    def post(self,request) :
        form = self.form_class(request.POST)
        if form.is_valid() :
            random_code = random.randrange(1000,10000)
            send_opt_code(phone_number=form.cleaned_data['phone_number'],code=random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'],code=random_code)
            request.session['user_registration_info'] = {
                'phone_number' : form.cleaned_data['phone_number'],
                'email' : form.cleaned_data['email'],
                'full_name' : form.cleaned_data['full_name'],
                'password' : form.cleaned_data['password'],
            }
            messages.success(request,'We sent you a code',extra_tags='success')
            return redirect('accounts:verification_code')
        else :
            return render(request, self.template_name,context={'form':form})

class User_Registration_Verification_CodeView(View) : # This class check that the code we sent is that one user use and register user

    template_name = 'accounts/Verification_Code_Form.html'
    form_class = Verification_CodeForm

    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,context={'form':form})

    def post(self,request) :
        user_session = request.session['user_registration_info']
        code_instance=OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            if code_instance.code == cd['verification_code'] :
                User.objects.create_user(phone_number=user_session['phone_number'],email=user_session['email'],full_name=user_session['full_name'],password=user_session['password'])
                code_instance.delete()
                messages.success(request,'User Registered successfully',extra_tags='success')
                return redirect('Home:home')
            else :
                messages.error(request,'This code is wrong , try again',extra_tags='danger')
                return redirect('accounts:verification_code')
        else :
            return render(request, self.template_name, context={'form': form})

class User_LoginView(View) :

    template_name = 'accounts/User_Login_Form.html'
    form_class = User_LoginForm

    def get(self,request) :
        form = self.form_class()
        return render(request,self.template_name,context={'form':form})

    def post(self,request) :
        form = self.form_class(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            user = authenticate(request,phone_number=cd['phone_number'],password=cd['password'])
            if user is not None :
                login(request,user)
                messages.success(request,'User logged in successfully',extra_tags='success')
                return redirect('Home:home')
            else :
                messages.error(request,'Either phone number or password is wrong ')
        else :
            return render(request, self.template_name, context={'form':form})


class User_LogoutView(LoginRequiredMixin,View) :

    def get(self,request) :
        logout(request)
        messages.success(request,'User logged out successfully',extra_tags='success')
        return redirect('Home:home')