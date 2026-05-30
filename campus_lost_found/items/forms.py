# items/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Item

# Keep your existing ItemForm here...
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'status', 'category', 'location', 'image', 'contact_email']

# --- ADD THIS NEW FORM ---
class UniversityRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Must use a valid university email address.')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # CHANGE THIS to your actual university domain (e.g., '@nyu.edu', '@ucla.edu')
        allowed_domain = '@gmail.com' 
        
        if not email.endswith(allowed_domain):
            raise forms.ValidationError(f"Registration is restricted. Please use your {allowed_domain} email address.")
        
        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
            
        return email