from django import forms
from django.utils import timezone


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


