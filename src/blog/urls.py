from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user-posts'),
    path('search/', views.SearchListView.as_view(), name='search-results'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name="post-detail"),
    path('post/new/', views.PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name="post-delete"),
]
