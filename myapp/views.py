from rest_framework import viewsets
from .models import UserData
from .serializers import UserDataSerializer

from rest_framework import viewsets, permissions
from .models import UserData
from .serializers import UserDataSerializer

class UserDataViewSet(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    # Permette l'accesso non autenticato
    permission_classes = [permissions.AllowAny]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserData
from .serializers import UserDataSerializer

class UserDataCreate(APIView):
    def post(self, request, format=None):
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics, permissions
from .models import UserData
from .serializers import UserDataSerializer

class UserOwnDataView(generics.ListAPIView):
    serializer_class = UserDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Restituisce solo i dati dell'utente corrente."""
        return UserData.objects.filter(user=self.request.user)


from .serializers import UserSerializer  # Assicurati di avere questo serializer

class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        """
        Restituisce l'utente autenticato.
        """
        return self.request.user



from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserData

class UserDetailView(LoginRequiredMixin, View):
    template_name = 'user_detail.html'

    def get(self, request):
        # Ottiene i dati dell'utente autenticato
        user_data = UserData.objects.get(user=request.user)
        context = {
            'user_data': user_data
        }
        return render(request, self.template_name, context)
