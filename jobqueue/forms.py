from django import forms
from .models import Jobs, Tagtype, Colors, User, Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.utils import timezone
from django.contrib.admin import widgets

from .icons2 import stchose

class UserForm(forms.ModelForm):
    form_title = 'Редактирование/добавление пользователя'
    username = forms.CharField(widget=forms.TextInput(attrs={ 'autocomplete':'off' }))
    class Meta:
        model = User
        labels = {'username':"login"}
        fields = ('username', 'first_name', 'last_name', 'email')

        def clean_email(self):
            email = self.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email already exists")
            return email

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        return cleaned_data

class UserEditForm(forms.ModelForm):
    form_title = 'Редактирование пользователя'
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    form_title = 'Остальные данные пользователя'
    class Meta:
        model = Profile
        fields = ('phone', )

class PasswordForm(forms.ModelForm):
    form_title = 'Создание нового пароля для пользователя'
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password_repeat = forms.CharField(max_length=32, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('password','password_repeat',)

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("password_repeat")

        if password1 != password2:
            raise forms.ValidationError("Пароли должны совпадать")
        elif len(password1) < 8:
            raise forms.ValidationError("Пароль должен быть 8 и более символов")
        else:
            return cleaned_data

class ProfileForm(forms.ModelForm):
    form_title = 'Остальные данные пользователя'
    class Meta:
        model = Profile
        fields = ('phone','status',)

class JobsForm(forms.ModelForm):
    form_title = 'Редактирование/добавление задания'
    class Meta:
        model = Jobs
        exclude = ('createdatetime','order','tags',)

class JobTechOpForm(forms.ModelForm):
    form_title = 'Редактирование/добавление задания'
    class Meta:
        model = Jobs
        fields = '__all__'
        exclude = ('createdatetime','order','tags', 'manager')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            ctags = self.instance.tags.names()
        except:
            ctags = ()
        print("ctags",ctags)
        alltags = Tagtype.objects.filter(techop__exact=True)#.values_list('id', flat=True)
        for tg in alltags:
            field_name = '__tg__,%s' % (tg.id,)
            if str(tg.id) in ctags:
                state = True
            else:
                state = False
            self.fields[field_name] = forms.BooleanField(label=tg.name, required=False)
            self.fields[field_name].initial = state
            print(tg.name, state)

    def clean(self):
        cleaned_data = super(JobTechOpForm, self).clean()
        # name = self.cleaned_data.get('name')
        # print('name',name.split())
        # if len(name.split()) > 1:
        #     raise forms.ValidationError("Наименование тега должно состоять из одного слова!")
        return cleaned_data

    def save(self, profile=None):
        job = self.instance
        job.manager = profile
        job.save()
        data = self.cleaned_data
        alltags = Tagtype.objects.filter(techop__exact=True)
        for tg in alltags:
            job.tags.remove(str(tg.id))
        for key,value in data.items():
            print(key,value)
            tg = key.split(",")
            if tg[0]=="__tg__" and value:
                print(job,value,str(tg[1]))
                job.tags.add(str(tg[1]))
            else:
                pass
                #setatr


class TagtypeForm(forms.ModelForm):
    form_title = 'Редактирование/добавление тегов'
    icon2 =  forms.ChoiceField(label = "Icon", widget=forms.Select(attrs={'class': 'form-control'}), required=False, choices=stchose)
    class Meta:
        model = Tagtype
        fields = ('name','icon2','seton','techop',) #,
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
