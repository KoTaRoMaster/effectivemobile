from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Staff, Office

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'second_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'username': 'Введите логин',
            'email': 'Введите почту',
            'first_name': 'Введите имя',
            'last_name': 'Введите фамилию',
            'second_name': 'Введите отчество',
            'password1': 'Введите пароль',
            'password2': 'Повторите пароль',
        }

        labels = {
            'username': 'Логин',
            'email': 'Почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'second_name': 'Отчество',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-input',
                'placeholder': placeholders.get(field_name, ''),
            })
            if field_name in labels:
                field.label = labels[field_name]
            field.help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'second_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'first_name': 'Введите имя',
            'last_name': 'Введите фамилию',
            'second_name': 'Введите отчество',
            'email': 'Введите почту',
        }

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'second_name': 'Отчество',
            'email': 'Почта',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-input',
                'placeholder': placeholders.get(field_name, ''),
            })
            if field_name in labels:
                field.label = labels[field_name]


class AdminUserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input'
            })

    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'second_name',
            'is_staff',
            'is_superuser',
            'password1',
            'password2',
        )

    is_staff = forms.BooleanField(
        required=False,
        label='Персонал'
    )

    is_superuser = forms.BooleanField(
        required=False,
        label='Администратор'
    )


class AdminUserEditForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'second_name',
            'is_staff',
            'is_superuser',
            'is_active',
        ]


class AdminStaffCreateForm(forms.ModelForm):

    class Meta:
        model = Staff

        fields = [
            'user',
            'offices'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input'
            })

class AdminStaffEditForm(forms.ModelForm):

    class Meta:
        model = Staff

        fields = [
            'user',
            'offices'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input'
            })

class AdminOfficeCreateForm(forms.ModelForm):

    class Meta:
        model = Office

        fields = [
            'name',
            'address',
            'time_work_from',
            'time_work_to',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input'
            })

class AdminOfficeEditForm(forms.ModelForm):

    class Meta:
        model = Office

        fields = [
            'name',
            'address',
            'time_work_from',
            'time_work_to'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input'
            })

