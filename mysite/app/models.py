from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random, string

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.ManyToManyField('Author')
    title = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='images', null=True)
    file = models.FileField(upload_to='books', null=True)
    description = models.CharField(max_length=1000)
    publisher = models.ForeignKey('Publisher')
    price = models.IntegerField(null=True)
    category = models.ForeignKey('Category', null=True)
    year = models.ForeignKey('Year')

    def __str__(self):
    	return self.title

def create_token():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))

class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    token = models.CharField(max_length=40, default=create_token)
    book = models.ManyToManyField('Book')
    archive = models.BooleanField(default=False)
    def number_of_books(self):
        return len(self.book.all())

    def total_price(self):
        return sum([book.price for book in self.book.all()])

    def books_ids_list(self):
        return ','.join([str(book.id) for book in self.book.all()])

    def books_list(self):
        return self.book.all()



class Purchased(models.Model):
    user = models.ForeignKey(User, null=True)
    book = models.ForeignKey('Book', null=True)


class Publisher(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Year(models.Model):
    year = models.IntegerField(null=True)

    def __str__(self):
        return str(self.year)