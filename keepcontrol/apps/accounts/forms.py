from django import forms
from django.contrib.auth import get_user_model #Para usar o model do nosso usuário
from apps.series.models import Serie, SeasonSerie, EpisodeSerie
User = get_user_model()

class RegisterForm(forms.ModelForm):

    x = {
        "password_mismatch": ("As senhas não conferem!"),
    }
    
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Cosnfirmação de senha', widget=forms.PasswordInput)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.x["password_mismatch"],
                #code="password_mismatch",
            )
        return password2
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control' #Adicionando uma class para os fields
 
    
class EditAccountForm(forms.ModelForm):
     
    class Meta:
        model = User
        fields = ['username', 'email', 'name']

    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control' #Adicionando uma class para os fields
 

class AdicionarSerieForm(forms.ModelForm):
     
    class Meta:
        model = Serie
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(AdicionarSerieForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control' #Adicionando uma class para os fields
 

class AdicionarSeasonSerieForm(forms.ModelForm):
     
    class Meta:
        model = SeasonSerie
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(AdicionarSeasonSerieForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control' #Adicionando uma class para os fields
            if self.fields['serie']:
                self.fields['serie'].widget.attrs['class'] = 'select2'

class AdicionarEpisodeSerieForm(forms.ModelForm):
     
    class Meta:
        model = EpisodeSerie
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(AdicionarEpisodeSerieForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control' #Adicionando uma class para os fields
            if self.fields['season']:
                self.fields['season'].widget.attrs['class'] = 'select2'


    