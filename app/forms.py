from django import forms


# Form for user registration
class UserRegister(forms.Form):
    email = forms.EmailField(max_length=30, label='Введите email')
    first_name = forms.CharField(min_length=3, max_length=20, label='Введите имя')
    last_name = forms.CharField(min_length=3, max_length=20, label='Введите фамилию')
    password = forms.CharField(min_length=8, label='Введите пароль')
    password_repeat = forms.CharField(min_length=8, label='Повторите пароль')


# Form for login
class UserLogin(forms.Form):
    email = forms.EmailField(max_length=30, label='Введите email')
    password = forms.CharField(min_length=8, label='Введите пароль')


# Form for user information update
class UserUpdate(forms.ModelForm):
    email = forms.EmailField(max_length=30, label='Введите email')
    first_name = forms.CharField(min_length=3, max_length=20, label='Введите имя')
    last_name = forms.CharField(min_length=3, max_length=20, label='Введите фамилию')


# Search field
class Search(forms.Form):
    search = forms.CharField(max_length=30, label='Поиск')
