from django.db.models import Q
from rest_framework import generics, filters, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.http import HttpResponse
from rest_framework.permissions import AllowAny


def homepage(request):
    return HttpResponse("<h1>This is Api for social</h1> <br> /api/signup/ , /api/login/ <br> /api/search/ <br> /api/friend-requests/ <br> /api/friend-requests/pending/")

class SignupView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()

        return Response({
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                },
                'token': token.key  
            })
    

class LoginView(APIView):

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():

            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            accepted_friendships = Friendships.objects.filter(
                (models.Q(user1=user) | models.Q(user2=user)) )

            friends = [
                friendship.user1 if friendship.user2 == user else friendship.user2
                for friendship in accepted_friendships
            ]

            friend_data = UserSerializer(friends, many=True).data
            friends_count = len(friends)

            return Response({"token": token.key, "user": UserSerializer(user).data ,"friends" :friend_data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchView(generics.ListAPIView):

    queryset = CustomUser.objects.all().exclude(is_superuser=True)
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'name']
    pagination_class = StandardResultsSetPagination


class FriendRequestView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    def post(self, request):

        receiver_id = request.data.get('receiver_id')

        if not receiver_id:
            return Response({"detail": "Receiver ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        receiver = CustomUser.objects.filter(id=receiver_id).first()

        if not receiver:
            return Response({"detail": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)

        if not FriendRequests.can_send_request(request.user):
            return Response({"detail": "You have exceeded the limit of friend requests"}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        friend_request, created = FriendRequests.objects.get_or_create(sender=request.user, receiver=receiver)

        if not created:
            return Response({"detail": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(FriendRequestsSerializer(friend_request).data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        if pk is None:
            return Response({"detail": "Request ID (pk) is required"}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequests.objects.get(id=pk, receiver=request.user, is_accepted=False)
        if not friend_request:
            return Response({"detail": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')

        if action == 'accept':
            friend_request.is_accepted = True
            friend_request.save()
            Friendships.objects.create(user1=friend_request.sender, user2=friend_request.receiver)
            return Response({"detail": "Friend request accepted"}, status=status.HTTP_200_OK)

        elif action == 'reject':
            friend_request.delete()
            return Response({"detail": "Friend request rejected"}, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)


class PendingFriendRequestsView(generics.ListAPIView):

    serializer_class = FriendRequestsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        
        sent_requests = FriendRequests.objects.filter(sender=self.request.user, is_accepted=False)
        received_requests = FriendRequests.objects.filter(receiver=self.request.user, is_accepted=False)

        sent = FriendRequestsSerializer(sent_requests, many=True)
        received = FriendRequestsSerializer(received_requests, many=True)

        data = {
            'sent': sent.data,
            'received': received.data
        }

        return Response(data)


