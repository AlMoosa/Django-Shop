from django import forms
from django.utils import timezone
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def __clean__(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': 'Користувач з таким логіном не зараєстрований в системі. Будьласка зареєстркйтесь'},
                                        code='user mot exists')

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError({'password': 'Не правильний пароль'},
                                        code='invalid password', )


class RegistrationForm(forms.ModelForm):

    password_check = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_check',
            'first_name',
            'last_name',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Придумайте пароль'
        self.fields['password_check'].label = 'Повторіть пароль'
        self.fields['first_name'].label = 'Імя'
        self.fields['last_name'].label = 'Прізвище'
        self.fields['email'].label = 'Ваша пошта'
        self.fields['email'].help_text = 'Будьласка вкажіть реальну адресу електронної скриньки'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        password_check = self.cleaned_data['password_check']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': 'Користувач з таким логіном вже використовується. Будьласка виберіть інший логін'},
                                        code='user exists')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError({'email': 'Користувач з такию адресною скринькою вже інсунує. Будьласка вкажіть іншу поштову скриньку'},
                                        code='email exists')
        if password != password_check:
            raise forms.ValidationError({'password': '',
                                         'password_check': 'Ви помилились при вводі паролів, вони не співпадають, введіть повторно'},
                                        code='passwords do not match', )


class OrderForm(forms.Form):

    name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=(('self', 'Самовивіз'), ('delivery', 'Доставка')))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Імя'
        self.fields['last_name'].label = 'Прізвище'
        self.fields['phone'].label = 'Контактний телефон'
        self.fields['phone'].help_text = 'Будьласка вказуйте реальний номер телефлну, за яким можна з Вами звязатись'
        self.fields['buying_type'].label = 'Спосіб отримання'
        self.fields['address'].label = 'Адреса'
        self.fields['address'].help_text = 'Обовязково вказуйте місто!'
        self.fields['comments'].label = 'Коментар до замовлення'
        self.fields['date'].label = 'Дата доставки'
        self.fields['date'].help_text = 'Доставка проводиться в день оформлення замовлення. Менеджер з вами попередньо звяжеться'




