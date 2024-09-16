from django import forms
from .models import Profile
from .models import Report
from .models import ReportFile
from .models import Practice


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'user', 'profile_picture', 'contact_number', 'address']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['subject', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReportForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        report = super(ReportForm, self).save(commit=False)
        # if self.user and not report.whistleblower:
        #     report.whistleblower = self.user
        if commit:
            report.save()
        return report


class ReportFileForm(forms.ModelForm):
    class Meta:
        model = ReportFile
        fields = ['file']


class ResolveForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['notes']

    def __init__(self, *args, **kwargs):
        super(ResolveForm, self).__init__(*args, **kwargs)
        self.fields['notes'].required = False

    def save(self, commit=True):
        report = super(ResolveForm, self).save(commit=False)
        if commit:
            report.status = 'Resolved'
            report.save()
        return report


class PracticeForm(forms.ModelForm):
    existing_practices = forms.ModelChoiceField(
        queryset=Practice.objects.all(),
        required=False,
        label="Select a Practice",
        empty_label="My practice is not listed"
    )
    new_practice = forms.CharField(
        max_length=100,
        required=False,
        label="Name of Practice"
    )

    class Meta:
        model = Practice
        fields = ['existing_practices', 'new_practice', 'state', 'city', 'address', 'zipcode', 'phone', 'website']
        labels = {
            'new_practice': "Name of practice, hospital, group, etc.",
            'phone': "Phone number for practice (if applicable)",
            'website': "Website for practice (if applicable)"
        }

    def clean(self):
        cleaned_data = super().clean()
        existing_practice = cleaned_data.get('existing_practices')
        new_practice = cleaned_data.get('new_practice')

        if not existing_practice and not new_practice:
            raise forms.ValidationError("Please select an existing practice or enter a new practice name.")

        if existing_practice and new_practice:
            raise forms.ValidationError(
                "Please select either an existing practice or enter a new practice name, not both.")

        if new_practice:
            if Practice.objects.filter(name__iexact=new_practice).exists():
                raise forms.ValidationError("This practice already exists. Please select it from the dropdown.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(PracticeForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['website'].required = False
        self.fields['state'].required = False
        self.fields['city'].required = False
        self.fields['address'].required = False
        self.fields['zipcode'].required = False


        if 'instance' in kwargs and kwargs['instance']:
            existing_practice = kwargs['instance']
            self.fields['state'].initial = existing_practice.state
            self.fields['city'].initial = existing_practice.city
            self.fields['address'].initial = existing_practice.address
            self.fields['zipcode'].initial = existing_practice.zipcode


    def save(self, commit=True):
        if self.cleaned_data['existing_practices']:
            return self.cleaned_data['existing_practices']

        practice = Practice(
            name=self.cleaned_data['new_practice'],
            state=self.cleaned_data['state'],
            city=self.cleaned_data['city'],
            address=self.cleaned_data['address'],
            zipcode=self.cleaned_data['zipcode'],
            phone=self.cleaned_data['phone'],
            website=self.cleaned_data['website']
        )
        if commit:
            practice.save()
        return practice
