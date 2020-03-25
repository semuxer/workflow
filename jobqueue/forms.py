from django import forms
from .models import Jobs, Tagtype, Colors, User, Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.utils import timezone
from django.contrib.admin import widgets

from .icons2 import stchose
import re

def parse_tags(lss):
    regex = r"(?P<name>.*?)\s*\((?P<ext>.*)\)"
    out = {}
    for ls in lss:
        #print(ls)
        matches = re.search(regex, str(ls))
        if matches:
            name = matches.group('name')
            #ext = matches.group('ext')
            if type(out.get(name)) is not list:
                out[name] = [(ls.id, ls.name)]
            else:
                out[name].append((ls.id, ls.name))
                #print('-name',name)
                #print(' ext',ext)
        else:
            if type(out.get(ls)) is not list:
                out[str(ls)] = [(ls.id, ls.name)]
            else:
                out[str(ls)].append((ls.id, ls.name))
            #print('-name',ls)
    return out


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
        exclude = ('createdatetime','order','tags', 'manager','newtag')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        alltags = Tagtype.objects.filter(techop__exact=True)#.values_list('id', flat=True)
        z = parse_tags(alltags)
        #print("z",z)
        for tkey, tval in z.items():
            #print(tkey, tval, len(tval))
            if len(tval) > 1:
                choices = tval
                state = None
                for cst in tval:
                    if self.instance.checknt(cst[0]):# str(cst[0]) in ctags:
                        state = tval[0]
                choices.insert(0,(None,"---------"))
                field_name = '__tgl__,%s' % (tkey,)
                self.fields[field_name] = forms.CharField(label=tkey, widget=forms.Select(choices=choices), required=False)   #forms.BooleanField(label=tg.name, required=False)
                self.fields[field_name].initial = state
            else:
                field_name = '__tgc__,%s' % (tval[0][0],)
                if self.instance.checknt(tval[0][0]):#if str(tval[0][0]) in ctags:
                    state = True
                else:
                    state = False
                self.fields[field_name] = forms.BooleanField(label=tval[0][1], required=False)
                self.fields[field_name].initial = state
        # for tg in alltags:
        #     field_name = '__tg__,%s' % (tg.id,)
        #     if str(tg.id) in ctags:
        #         state = True
        #     else:
        #         state = False
        #     self.fields[field_name] = forms.BooleanField(label=tg.name, required=False)
        #     self.fields[field_name].initial = state
        #     print(tg.name, state)

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
        data = self.cleaned_data
        alltags = Tagtype.objects.filter(techop__exact=True)
        job.newtag = ""
        #for tg in alltags:
        #    job.tags.remove(str(tg.id))
        for key,value in data.items():
            print("-kv-",key,value)
            tg = key.split(",",1)
            if tg[0]=="__tgc__" and value:
                print("tgc",value,"-1",str(tg[1]))
                job.addnt(tg[1])
                #job.tags.add(str(tg[1]))
            elif tg[0]=="__tgl__" and value:
                try:
                    ctg = Tagtype.objects.get(id=value)
                    job.addnt(value)
                    #job.tags.add(str(value))
                except:
                    pass
                print("ctg",ctg)
                print("tgl",job,"-1",value,"-2",tg)
            else:
                pass
        job.save()


class TagtypeForm(forms.ModelForm):
    form_title = 'Редактирование/добавление тегов'
    icon2 =  forms.ChoiceField(label = "Icon", widget=forms.Select(attrs={'class': 'form-control'}), required=False, choices=stchose)
    class Meta:
        model = Tagtype
        fields = ('name','icon2','seton','techop','color',) #,
    def clean(self):
        cleaned_data = super(TagtypeForm, self).clean()
        name = self.cleaned_data.get('name')
        print('name',name.split())
        # if len(name.split()) > 1:
        #     raise forms.ValidationError("Наименование тега должно состоять из одного слова!")
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
