from django.shortcuts import render, redirect

from notes.noteapp.forms import TagForm


# Create your views here.
def main(request):
    return render(request, 'noteapp/index.html')


def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='noteapp:main')
        else:
            return render(request, 'noteapp/tag.html', {'form': form})

    return render(request, 'noteapp/tag.html', {'form': TagForm()})
