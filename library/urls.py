from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home')
     ,path('add/', views.add_book,name='add_book')
      ,path("edit/<int:book_id>/", views.edit_book, name="edit_book")
      ,path('delete/<int:book_id>/', views.delete_book, name='delete_book')
      ,path('book/<int:id>/', views.book_detail, name='book_detail')
      ,path("signup/", views.signup, name="signup")
]