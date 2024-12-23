from datetime import datetime
from django import forms
from . import choices
from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)

        for field in self.visible_fields():
            # CSS for look (bootstrap classes)
            field.field.widget.attrs['class'] = 'form-control shadow'


class CustomUserForm(FormSettings):
    # fields...
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=choices.GENDER)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this if and only if you want to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()

        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "This email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # change in email
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError(
                        "This email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class FacultyForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Faculty
        fields = CustomUserForm.Meta.fields + ['course']


class CourseForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Course
        fields = ['name']


class SubjectForm(FormSettings):
    faculty = forms.ModelMultipleChoiceField(
        queryset=Faculty.objects.none(),
        widget=forms.SelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id', None)
        super(SubjectForm, self).__init__(*args, **kwargs)

        if course_id:
            self.fields['faculty'].queryset = Faculty.objects.filter(course_id=course_id)
        else:
            self.fields['faculty'].queryset = Faculty.objects.none()

    class Meta:
        model = Subject
        fields = ['name', 'course', 'faculty']


class StudentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['batch'].queryset = Batch.objects.all()
        self.fields['batch'].empty_label = "Select Batch"

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + ['course', 'batch']


class BatchForm(FormSettings):
    start_year = forms.ChoiceField(
        choices=choices.YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Start Year",
        required=True
    )
    end_year = forms.ChoiceField(
        choices=choices.YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="End Year",
        required=True
    )

    class Meta:
        model = Batch
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_year = cleaned_data.get('start_year')
        end_year = cleaned_data.get('end_year')

        if start_year and end_year:
            cleaned_data['start_year'] = datetime.strptime(f"{start_year}-01-01", "%Y-%m-%d")
            cleaned_data['end_year'] = datetime.strptime(f"{end_year}-01-01", "%Y-%m-%d")

            if cleaned_data['start_year'] >= cleaned_data['end_year']:
                raise forms.ValidationError("Start year must be earlier than end year.")
        else:
            raise forms.ValidationError(
                "Both start year and end year must be selected.")

        return cleaned_data
    

class FacultyEditForm(FormSettings):
    first_name = forms.CharField(max_length=120)
    last_name = forms.CharField(max_length=120)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super(FacultyEditForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.admin.first_name
            self.fields['last_name'].initial = self.instance.admin.last_name
            self.fields['email'].initial = self.instance.admin.email
            self.fields['password'].widget.attrs['placeholder'] = "Fill this if and only if you want to update password"

    class Meta:
        model = Faculty
        fields = []

    def save(self, commit=True):
        faculty = super().save(commit=False)
        if faculty.admin:
            faculty.admin.first_name = self.cleaned_data['first_name']
            faculty.admin.last_name = self.cleaned_data['last_name']
            faculty.admin.email = self.cleaned_data['email']
            faculty.admin.gender = self.cleaned_data['gender']
            if self.cleaned_data['password']:
                faculty.admin.set_password(self.cleaned_data['password'])
            if commit:
                faculty.admin.save()
                faculty.save()
        return faculty

class LeaveReportFacultyForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportFacultyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportFaculty
        fields = ['date', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
