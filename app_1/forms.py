from django import forms
from .models import Predmeti, Korisnik, UpisniList
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory

class PredmetForm(forms.ModelForm):
    class Meta:
        model= Predmeti
        fields='__all__'

class StudentForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Korisnik
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'status', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['readonly'] = False
        self.fields['status'].widget.attrs['disabled'] = False
        self.fields['status'].required = False

    def save(self, commit=True):
        korisnik = super().save(commit=False)
        korisnik.role = 'stu'
        if commit:
            korisnik.save()
        return korisnik
    
class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Korisnik
        fields = ['first_name', 'last_name', 'email', 'status', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].disabled = False
        self.fields['role'].disabled = True
        self.fields['role'].widget = forms.HiddenInput()

class ProfessorForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Korisnik
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        professor = super().save(commit=False)
        professor.role = 'prof'
        if commit:
            professor.save()
        return professor


class ProfessorEditForm(forms.ModelForm):
    class Meta:
        model = Korisnik
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AssignPredmetForm(forms.Form):
    predmeti = forms.ModelMultipleChoiceField(queryset=Predmeti.objects.all(), widget=forms.CheckboxSelectMultiple)


class UpisniListForm(forms.ModelForm):
    semestar = forms.IntegerField(label='Semestar')

    class Meta:
        model = UpisniList
        fields = ['predmet', 'korisnik', 'status', 'semestar']

class UpisniListEditForm(forms.ModelForm):
    class Meta:
        model = UpisniList
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = False


UpisniListFormSet = modelformset_factory(
    UpisniList,
    form=UpisniListEditForm,
    extra=0,
)

class UpisniListEditFormStudent(forms.ModelForm):
    class Meta:
        model = UpisniList
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = False
        self.fields['status'].widget.choices = [('enr', 'Enrolled')]

        if self.instance.status != 'enr':
            self.fields['status'].widget.attrs['disabled'] = True


UpisniListFormSetStudent = modelformset_factory(
    UpisniList,
    form=UpisniListEditFormStudent,
    extra=0,
)

class SemesterChoiceForm(forms.Form):
    semestar_choices = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 9)])