from django import forms
from .models import Patient, DEFAULT_EMAIL, Gender, Doctor
from bookings.fields import ListTextWidget
from bookings.models import Location, Service, SessionStatus
from payments.models import PaymentType

# crispy-forms import
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.utils import timezone
from dal import autocomplete

PATIENT_SORT_BY = (
    ('registration_date_desc', 'Registration Date(DESC)'),
    ('registration_date_asc', 'Registration Date(ASC)'),
    ('name_asc', 'Name(ASC)'),
    ('name_desc', 'Name (DESC)')
)

BOOKING_SORT_BY = (
    ('start_date_desc', 'Admission Date(DESC)'),
    ('start_date_asc', 'Admission Date(ASC)'),
    ('end_date_desc', 'Discharge Date(DESC)'),
    ('end_date_asc', 'Discharge Date(ASC)'),
    ('name_asc', 'Name(ASC)'),
    ('name_desc', 'Name (DESC)')
)
PAYMENT_SORT_BY = (
    ('date_desc', 'Date(DESC)'),
    ('date_asc', 'Date(ASC)'),
    ('amount_desc', 'Paid Date(DESC)'),
    ('amount_asc', 'Paid Date(ASC)'),
    ('name_asc', 'Name(ASC)'),
    ('name_desc', 'Name (DESC)')
)

BOOKING_TIMELINE_CHOICE = (
    ('', '-----select----'),
    ('PAST', 'Past Bookings'),
    ('ACTIVE', 'Active Bookings'),
    ('FUTURE', 'Future Bookings'),
    ('INCONSISTENT', 'Inconsistent Bookings')
)


class PatientRegistrationForm(forms.ModelForm):

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', None)
        if phone_number.isdigit():
            return phone_number
        else:
            raise forms.ValidationError("Invalid Phone number. Please Try again!")

    """def clean_email(self):
        email = self.cleaned_data.get('email', None)
        qs = Patient.objects.filter(email=email)
        if len(qs) == 0:
            return email
        else:
            raise forms.ValidationError("A Patient with similar email already exists.\n"
                                        "This could be a duplicate.\n"
                                        "Kindly confirm before proceeding")"""

    def clean_date_of_birth(self):
        if self.cleaned_data['date_of_birth'] > timezone.now().date():
            raise forms.ValidationError("FUTURE date of birth values are not allowed!")
        else:
            return self.cleaned_data['date_of_birth']

    class Meta:
        model = Patient
        fields = "__all__"
        widgets = {
            'gender': forms.RadioSelect(),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date'
            })
        }


class PatientReportFilterForm(forms.Form):
    registered_from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label='Registered From')
    to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=timezone.now)
    gender = forms.ModelChoiceField(Gender.objects.all(), required=False)
    sort_by = forms.ChoiceField(choices=PATIENT_SORT_BY)

    def __init__(self, *args, **kwargs):
        super(PatientReportFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('registered_from_date', css_class='form-group col-md-3 mb-0'),
                Column('to', css_class='form-group col-md-3 mb-0'),
                Column('gender', css_class='form-group col-md-3 mb-0'),
                Column('sort_by', css_class='form-group col-md-3 mb-0'),
                css_class='form-row',
            ),
            Submit('submit', 'Filter')
        )

    def clean(self):
        if self.cleaned_data['registered_from_date'] is not None:
            if self.cleaned_data['registered_from_date'] > self.cleaned_data['to']:
                raise forms.ValidationError("Invalid date range!")
            pass
        pass


class BookingReportFilter(forms.Form):
    gender = forms.ModelChoiceField(Gender.objects.all(), required=False)
    service = forms.ModelChoiceField(Service.objects.all(), required=False)
    location = forms.ModelChoiceField(Location.objects.all(), required=False)
    doctor = forms.ModelChoiceField(Doctor.objects.all(), required=False)
    from_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}),
        required=False,
        label='Admission Dates From'
    )
    to_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now,
        label="Admission Dates To"
    )
    status = forms.ModelChoiceField(SessionStatus.objects.all(), required=False)
    sort_by = forms.ChoiceField(choices=BOOKING_SORT_BY)
    patient = forms.ModelChoiceField(
        Patient.objects.all(),
        widget=autocomplete.ModelSelect2(url='users:patient_autocomplete'),
        help_text="Tel no. or name",
        required=False
    )
    timeline = forms.ChoiceField(choices=BOOKING_TIMELINE_CHOICE, required=False)

    def clean(self):
        if self.cleaned_data['from_date'] is not None:
            if self.cleaned_data['from_date'] > self.cleaned_data['to_date']:
                raise forms.ValidationError("Invalid date range!")
            pass
        pass

    def __init__(self, *args, **kwargs):
        super(BookingReportFilter, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('gender', css_class='form-group col-md-3 mb-0'),
                Column('service', css_class='form-group col-md-3 mb-0'),
                Column('location', css_class='form-group col-md-3 mb-0'),
                Column('doctor', css_class='form-group col-md-3 mb-0'),
                css_class='form-row',
            ),
            Row(
                Column('from_date', css_class='form-group col-md-3 mb-0'),
                Column('to_date', css_class='form-group col-md-3 mb-0'),
                Column('sort_by', css_class='form-group col-md-3 mb-0'),
                Column('status', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Row(
                    Column('patient', css_class='form-group col-md-3 mb-0'),
                ),
                Column('timeline', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Filter')
        )


class PaymentReportFilter(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False,
                                           label='Paid From date')
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=timezone.now)
    type = forms.ModelChoiceField(PaymentType.objects.all(), required=False)
    sort_by = forms.ChoiceField(choices=PAYMENT_SORT_BY)
    patient = forms.ModelChoiceField(
        Patient.objects.all(),
        widget=autocomplete.ModelSelect2(url='users:patient_autocomplete'),
        help_text="Tel no. or name",
        required=False
    )
    from_amount = forms.DecimalField(
        decimal_places=2,
        min_value=0,
        initial=0
    )
    to_amount = forms.DecimalField(
        decimal_places=2,
        min_value=0,
        required=False
    )
    extra_tags = forms.Field(
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g AAR or 451JKH'
        }),
        label="Extra tag contains",
        help_text="this field is case insensitive",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(PaymentReportFilter, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('from_date', css_class='form-group col-md-3 mb-0'),
                Column('to_date', css_class='form-group col-md-3 mb-0'),
                Column('type', css_class='form-group col-md-3 mb-0'),
                Column('sort_by', css_class='form-group col-md-3 mb-0'),
                css_class='form-row',
            ),
            Row(
                Row(
                    Column('patient', css_class='form-group col-md-3 mb-0'),
                ),
                Column('from_amount', css_class='form-group col-md-2 mb-0'),
                Column('to_amount', css_class='form-group col-md-2 mb-0'),
                Column('extra_tags', css_class='form-group col-md-3 mb-0'),
                css_class='form-row',
            ),
            Submit('submit', 'Filter')
        )

    def clean(self):
        if self.cleaned_data['to_amount'] is not None:
            if self.cleaned_data['from_amount'] > self.cleaned_data['to_amount']:
                raise forms.ValidationError("Invalid amount range!")
            pass
        pass

        if self.cleaned_data['from_date'] is not None:
            if self.cleaned_data['from_date'] > self.cleaned_data['to_date']:
                raise forms.ValidationError("Invalid date range!")
            pass
        pass
