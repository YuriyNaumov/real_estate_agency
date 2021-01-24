from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['listing','listing_id','name','email','phone','message','file','contact_date','user_id']


# class ContactForm(forms.Form):
#     name = forms.CharField(max_length=200)
#     email = forms.EmailField()
#     phone = forms.CharField(max_length=100)
#     message = forms.CharField()
#     file = forms.FileField()

