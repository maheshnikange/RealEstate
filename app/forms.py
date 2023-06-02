from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Project,Image,User,Profile
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    lastname = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))

c1=(('Not Started','Not Started'),('In Progress','In Progress'),('Completed','Completed'))
class add_project_form(forms.ModelForm):
    class Meta:
        model=Project
        fields='__all__'
        exclude = ('user',)
    project_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'project_name'}))
    proposer = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'proposer'}))
    project_manager = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'project_manager'}))
    brief_desc = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'brief_desc'}))
    location = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'location'}))
    locality = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'locality'}))
    Projected_ROI = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'Projected_ROI'}))
    start_date = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'start_date'}))
    location_link = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'location_link'}))
    expected_duration = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'expected_duration'}))
    min_investment = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'min_investment'}))
    Investment_till_date = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'Investment_till_date'}))
    total_investment = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control",'placeholder': 'total_investment'}))
    land_purchased = forms.ChoiceField(choices=c1,label='select')
    detail_desc = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control",'placeholder': 'detail_desc'}))
class ImageForm(ModelForm):
    image=forms.ImageField(
        label='image',
    )
    class Meta:
        model=Image
        fields=('image',)


class userUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields='__all__'
        exclude = ('user',)
    phone_no = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),
    address_line1 = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),
    address_line2 = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),
    pincode = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),
    country = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"})),

    

