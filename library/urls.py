from django.urls import path
from .views import (
    CategoryListView, BookListView, BookDetailView,
    BorrowingListCreateView, BorrowingDetailView, ReturnRetrieveUpdateView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('books/', BookListView.as_view(), name='books'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('borrowings/', BorrowingListCreateView.as_view(), name='borrowings'),
    path('borrowings/<int:pk>/', BorrowingDetailView.as_view(), name='borrowing_detail'),
    path('borrowings/<int:pk>/return/', ReturnRetrieveUpdateView.as_view(), name='borrowing_return'),
]