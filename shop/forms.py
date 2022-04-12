from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginUserForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'login__input', 'maxlength': '32'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'login__input', 'minlength': '8'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    # Валидация всей формы
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'Пользователь с логином {username} не найден')
        if not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'login__input', 'maxlength': '32'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'login__input', 'minlength': '8'}))
    confirm_password = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'login__input'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'login__input', 'maxlength': '255'}))
    # phone = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'login__input'}), required=False)
    # address = forms.CharField(label='Адрес', widget=forms.TextInput(attrs={'class': 'login__input'}), required=False)
    # first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'login__input'}), required=False)
    # last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'login__input'}), required=False)
    

  # Валидация конкретного поля
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный электронный адрес уже зарегистрован')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Логин {username} занято. Попробуйте другое.')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        if len(password) < 8:
            raise forms.ValidationError('Пароль слишком короткий. Он должен быть не менее 8 символов')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email',]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'surname', 'email', 'phone', 'buying_type', 'state', 'city', 'street', 'house', 'flat', 'comment'
        )
