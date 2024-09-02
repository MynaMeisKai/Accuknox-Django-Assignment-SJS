from django.urls import path
from .views import *


urlpatterns = [
    path('', homepage, name='homepage'),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/search/', SearchView.as_view(), name='user-search'),
    path('api/friend-requests/', FriendRequestView.as_view(), name='friend-requests'),
    path('api/friend-requests/<int:pk>/', FriendRequestView.as_view(), name='friend-requests'),
    path('api/friend-requests/pending/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]