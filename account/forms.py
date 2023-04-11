from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    class Meta:
        model = User
        fields = ("email","password")

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = authenticate(email=email,password=password)
        print(user)
        
        if not user:
            raise forms.ValidationError("Email duzgun deyil!")
        
        if not user.is_active:
            raise forms.ValidationError("Hesab aktiv deyil!")
        
        return self.cleaned_data


    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"form-control"})
            
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("email","fullname","password","password_confirm")

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"form-control"})

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu istifaəçi adı artıq mövcuddur!")
        
        if len(password) < 6:
            raise forms.ValidationError("Uzunluq 6 dan kiçikdir!")
        
        if password != password_confirm:
            raise forms.ValidationError("Şifrələr uyğun deyil!")
        
        return self.cleaned_data
