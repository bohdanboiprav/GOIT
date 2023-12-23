from django.shortcuts import render, redirect
from django.views import View
from .models import Quote, Tag, Author

from .forms import QuoteForm, AuthorForm


# Create your views here.
def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quotesapp/index.html', {"quotes": quotes})


def author(request, auth_id):
    # new_auth_name = auth_name.replace("-", " ")
    author_data = Author.objects.filter(pk=auth_id).first()
    return render(request, 'quotesapp/author.html', {"author": author_data})


class NewAuthor(View):
    template_name = 'quotesapp/add_author.html'
    form_class = AuthorForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to="authapp:signin")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotesapp:home")
        return render(request, self.template_name, {"form": form})


class NewQuote(View):
    template_name = 'quotesapp/add_quote.html'
    form_class = QuoteForm
    authors = Author.objects.all()
    tags = Tag.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to="authapp:signin")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name,
                      {"authors": self.authors, "tags": self.tags, "form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.author = Author.objects.filter(fullname=request.POST.get('author')).first()
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to="quotesapp:home")
        return render(request, self.template_name, {"authors": self.authors, "tags": self.tags, "form": form})
