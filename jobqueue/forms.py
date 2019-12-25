from django import forms
from .models import Jobs, Tagtype, Colors
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.utils import timezone
from django.contrib.admin import widgets

from .icons2 import stchose

class JobsForm(forms.ModelForm):
    form_title = 'Редактирование/добавление задания'
    class Meta:
        model = Jobs
        exclude = ('createdatetime','order','tags',)

class TagtypeForm(forms.ModelForm):
    form_title = 'Редактирование/добавление тегов'
    icon2 =  forms.ChoiceField(label = "Icon", widget=forms.Select(attrs={'class': 'form-control'}), required=False, choices=stchose) 
    class Meta:
        model = Tagtype
        fields = ('name','icon2','seton',) #,
    def clean(self):
        cleaned_data = super(TagtypeForm, self).clean()
        name = self.cleaned_data.get('name')
        print('name',name.split())
        if len(name.split()) > 1:
            raise forms.ValidationError("Наименование тега должно состоять из одного слова!")
        return cleaned_data

class ColorsForm(forms.ModelForm):
    form_title = "Редактирование/добавление цветов"
    class Meta:
        model = Colors
        exclude = ('order',)
        widgets = {
            'text': forms.TextInput(attrs={'type': 'color', 'class':'p-0'}),
            'bg': forms.TextInput(attrs={'type': 'color', 'class':'p-0'}),
        }