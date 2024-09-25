import random

import pandas as pd
from django.http import JsonResponse
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


from rest_framework import generics
from .models import UserData
from .serializers import UserDataSerializer
'''
class UserDataCreateAPIView(generics.CreateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
'''


from rest_framework import generics
from rest_framework.response import Response
from .models import UserData
from .serializers import UserDataSerializer

def my_script(data):
    # Logica dello script che ritorna True se ha esito positivo, False altrimenti
    success = "some_processing_function(data)"
    print("okj")
    return success

'''class UserDataCreateAPIView(generics.CreateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer

    def perform_create(self, serializer):
        instance = serializer.save()  # Salva i dati del modello
        script_success = my_script(instance)  # Esegue lo script e controlla l'esito

        # Salva il risultato dello script nel modello, se necessario
        instance.script_success = script_success
        instance.save()

        # Aggiunge l'esito dello script al contesto della risposta
        self.script_success = script_success

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)  # Esegue la logica di creazione standard

        # Modifica la risposta in base all'esito dello script
        if self.script_success:
            response.data['message'] = 'Script executed successfully!'
        else:
            response.data['message'] = 'Script failed to execute properly.'

        return response
'''
from rest_framework import generics, status
from rest_framework.response import Response
from .models import UserData
from .serializers import UserDataSerializer
'''
class UserDataCreateAPIView(generics.CreateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message': 'Dati ricevuti e script eseguito con successo!'}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
from rest_framework import generics, status
from rest_framework.response import Response
from .models import UserData
from .serializers import UserDataSerializer

class UserDataCreateAPIView(generics.CreateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer

    def perform_create(self, serializer):
        instance = serializer.save()  # Salva i dati del modello
        script_success = self.execute_script(instance)  # Esegue lo script e controlla l'esito

        # Salva il risultato dello script nel modello, se necessario
        # instance.script_success = script_success
        # instance.save()

        # Aggiunge l'esito dello script al contesto della risposta
        self.script_success = script_success

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)  # Esegue la logica di creazione standard
        # Aggiungi il messaggio personalizzato al corpo della risposta
        if self.script_success:
            response.data['message'] = 'Script andato a buon fine!'
        else:
            response.data['message'] = 'Script fallito.'
        return response

    def execute_script(self, instance):
        # Qui inserisci la logica del tuo script
        # Ritorna True se lo script è un successo, False altrimenti
        return True  # O la logica reale del tuo script


def map(request):
        lat_min, lat_max = 45.1376, 45.1776  # Limiti per la latitudine
        lon_min, lon_max = 10.7714, 10.8114  # Limiti per la longitudine

        points = []
        df = pd.read_excel('/Users/michelemenabeni/PycharmProjects/AQA/Report_Complessivo_AqA_blocco35_Apr.mag.24.xlsx')
        print(df.columns)
        df=df.head(1000)
        df = df.dropna(subset=['Latitude', 'Longitude'])
        for index,row in df.iterrows():
            #lat = random.uniform(lat_min, lat_max)
            #lon = random.uniform(lon_min, lon_max)
            color = random.choice(["red", "green"])  # Colore casuale tra rosso e verde
            points.append({"lat": row['Latitude'], "lon": row['Longitude'], "color": color})
        return render(request,'map.html',{'points':points})

