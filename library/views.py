from rest_framework import generics, permissions
from rest_framework.response import Response
from django.conf import settings
from .models import Category, Book, Borrowing
from .serializers import CategorySerializer, BookSerializer, BorrowingSerializer, BorrowingReturnSerializer
from accounts.models import User

class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        # return request.user.is_authenticated and request.user.role == 'librarian'
        return True

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class CategoryListView(generics.ListAPIView): 
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly] 

class BookListView(generics.ListAPIView): 
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [ReadOnly]  

class BookDetailView(generics.RetrieveAPIView): 
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [ReadOnly]  

class BorrowingListCreateView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        from library.tasks import send_admin_borrowing_mail
        borrowing = serializer.save(librarian=self.request.user)
        if self.request.user.role == 'librarian':
            book = borrowing.book
            book.available = False
            book.save()
            # sending mail to admin through celery task
            send_admin_borrowing_mail.delay(borrowing.id)
            

    def get_queryset(self):
        if self.request.user.role == 'librarian':
            return Borrowing.objects.all()
        return Borrowing.objects.filter(user=self.request.user)
    

class ReturnRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReturnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        borrowing = serializer.save(librarian=self.request.user)
        if self.request.user.role == 'librarian':
            book = borrowing.book
            book.available = True
            book.save()
    

class BorrowingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated, IsLibrarian]  