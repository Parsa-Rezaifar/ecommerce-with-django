from django import forms
from . models import User,OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class Create_UserForm(forms.ModelForm) :

    first_password = forms.CharField(min_length=1,max_length=20,label='Password ',widget=forms.PasswordInput)
    second_password = forms.CharField(min_length=1,max_length=20,label='Confirm password ',widget=forms.PasswordInput)

    class Meta :

        model = User
        fields = ('email','phone_number','full_name')

    def clean_second_password(self) :

        cd = self.cleaned_data
        password1 = cd.get('first_password')
        password2 = cd.get('second_password')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match , check them again')
        return password2 #OR password1

    def save(self, commit=True) :
        cd = self.cleaned_data
        password = cd.get('first_password') #OR second_password
        user = super().save(commit=False)
        user.set_password(password)
        if commit is True :
            user.save()
        else :
            return user

class Change_UserForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(help_text='You can change your password using <a href=\"../password/\">this form</a>.')

    class Meta :

        model = User
        fields = ('email','phone_number','full_name','password','last_login')

class User_RegistrationForm(forms.Form) :

    phone_number = forms.CharField(max_length=11,label='Phone number ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your phone number'}))
    email = forms.EmailField(max_length=255,label='Email ',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Your email'}))
    full_name = forms.CharField(max_length=100,label='Full name ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your full name'}))
    password = forms.CharField(min_length=1,max_length=100,label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Your password'}))

    def clean_email(self) :
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user :
            raise ValidationError('This email has already taken')
        return email

    def clean_phone_number(self) :
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user :
            raise ValidationError('This phone number has already taken')
        else :
            OtpCode.objects.filter(phone_number=phone_number).delete()
        return phone_number

class Verification_CodeForm(forms.Form) :
    verification_code = forms.IntegerField(min_value=4,label='Received code ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your code'}))

class User_LoginForm(forms.Form) :
    phone_number = forms.CharField(max_length=11,label='Phone number ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your phone number'}))
    password = forms.CharField(min_length=1,max_length=100,label='Password ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Your password'}))