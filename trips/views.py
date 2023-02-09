from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView 
from django.db.models import Q


from .serializers import UserSerializer, LogInSerializer, TripSerializer
from .models import Trip

class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer

class TripView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id' 
    lookup_url_kwarg = 'trip_id'
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self): 
        user = self.request.user
        if user.group == 'driver':
            return Trip.objects.filter(
                Q(status=Trip.REQUESTED) | Q(driver=user)  #A Q object (django.db.models.Q) is an object used to encapsulate a collection of keyword arguments
            )
        if user.group == 'rider':
            return Trip.objects.filter(rider=user)
        return Trip.objects.none() #You use none() you know there is going to be no result (or don't want a result) and you still need one, none() will not hit the database.