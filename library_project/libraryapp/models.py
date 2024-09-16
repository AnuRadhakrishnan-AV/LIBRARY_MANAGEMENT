# models.py
from django.db import models


class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('user', 'User'),
      ]
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    age = models.IntegerField()
    address = models.TextField()
    contact_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    library_name = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_approved = models.BooleanField(default=False)
    library_location = models.CharField(max_length=100, blank=True, null=True)
    library_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username


class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('novel', 'Novel'),
        ('fantasy', 'Fantasy'),
        ('Autobiography', 'Autobiography'),
        ('biography', 'Biography'),
        ('poetry', 'Poetry'),
        ('thriller','Thriller')
    ]

    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('malayalam', 'Malayalam'),
        
    ]


    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    librarian = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='fiction')
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, default='english')
    is_booked = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title

class Booking(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booked_on = models.DateField()
    return_due_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} booked {self.book.title}'





