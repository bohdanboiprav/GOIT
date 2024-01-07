from django.forms import ModelForm, CharField, TextInput, DateField, DateInput
from .models import Author, Quote, Tag


# from .models import Profile


class AuthorForm(ModelForm):
    fullname = CharField(max_length=150, required=True, widget=TextInput())
    born_date = DateField(required=True, widget=DateInput(attrs={'placeholder': 'Enter date in YYYY-MM-DD format'}))
    born_location = CharField(max_length=300, required=True, widget=TextInput())
    description = CharField(max_length=10000, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    quote = CharField(max_length=10000, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['author', 'tags']
