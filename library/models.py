from django.db import models

# Create your models here.

from core.models import BaseModel
from accounts.models import User

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(BaseModel):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Borrowing(BaseModel):
    CONDITION_CHOICES = (
        ('good', 'Good'),
        ('damaged', 'Damaged'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowings')
    librarian = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lending')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    returned = models.BooleanField(default=False)
    returned_at = models.DateTimeField(auto_now_add=True)
    book_condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    comments = models.TextField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"{self.user} borrowed {self.book}"
