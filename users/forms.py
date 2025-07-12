"""
Forms for password reset functionality
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import UserProfile

class UserSignupForm(UserCreationForm):
    """Custom user signup form"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': 'your@email.com'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update widget attributes for existing fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm your password'
        })
        
        # Update help texts
        self.fields['username'].help_text = 'Your unique identifier on ReWear'
        self.fields['password1'].help_text = 'Must be at least 8 characters'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user)
        return user

class PasswordResetRequestForm(forms.Form):
    """Form for requesting password reset"""
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        }),
        help_text="We'll send you a password reset link at this email address."
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No account found with this email address.")
        return email

    def get_user(self):
        """Get user associated with the email"""
        email = self.cleaned_data.get('email')
        if email:
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return None
        return None

class PasswordResetConfirmForm(DjangoSetPasswordForm):
    """Form for setting new password"""
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter new password',
            'autocomplete': 'new-password'
        }),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm new password',
            'autocomplete': 'new-password'
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = (
            "Your password must contain at least 8 characters and cannot be too common."
        )

class UserLoginForm(AuthenticationForm):
    """Custom user login form"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update widget attributes
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': 'Enter your username or email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your password'
        })
        
        # Update labels and help text
        self.fields['username'].label = 'Username or Email'
        self.fields['username'].help_text = ''
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Check if username is actually an email
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                    self.cleaned_data['username'] = username
                except User.DoesNotExist:
                    raise ValidationError("Invalid email or password.")
            
            # Authenticate with username and password
            self.user_cache = authenticate(
                self.request, 
                username=username, 
                password=password
            )
            
            if self.user_cache is None:
                raise ValidationError("Invalid username/email or password.")
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data
