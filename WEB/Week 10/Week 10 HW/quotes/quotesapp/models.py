from django.db import models


# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=150, null=False)
    born_date = models.DateField(null=False)
    born_location = models.CharField(max_length=300, null=False)
    description = models.CharField(max_length=10000, null=False)

    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    quote = models.CharField(max_length=10000, null=False)

    def __str__(self):
        return f"{self.quote}"
