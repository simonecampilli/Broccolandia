import random

import pandas as pd
from django.db import transaction
from django.http import JsonResponse
from rest_framework import viewsets

from provaconmapbox import calcola_primi_100_consumo_attuale
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
    # Fetch all data from UserData model
    queryset = UserData.objects.all().values()
    df = pd.DataFrame(list(queryset))
    df_ok = df[df['flag'] != True].sort_values(by='data_lettura')

    # Calculate the top 100 current consumption readings (adapt this part as needed)
    current_route_coords, optimized_route_coords, emissioni_correnti, emissioni_proposta, distanza_corrente, distanza_proposta = calcola_primi_100_consumo_attuale(df_ok)

    # Ensure coordinates are in the correct format
    current_route_coords = [list(coord) for coord in current_route_coords]  # Ensure list format
    optimized_route_coords = [list(coord) for coord in optimized_route_coords]  # Convert NumPy arrays to lists

    # Prepare the points to pass to the template
    points = []
    for entry in UserData.objects.all():
        color = 'green' if entry.flag else 'red'
        points.append({
            "id": entry.id,  # Include ID to make the point clickable
            "lat": entry.latitude,
            "lon": entry.longitude,
            "color": color
        })

    # Pass the data to the template
    context = {
        'points': points,
        'current_route_coords': current_route_coords,
        'optimized_route_coords': optimized_route_coords,
        'emissioni_correnti': emissioni_correnti,
        'emissioni_proposta': emissioni_proposta,
        'distanza_corrente': distanza_corrente,
        'distanza_proposta': distanza_proposta
    }

    return render(request, 'map.html', context)

from django.shortcuts import render, get_object_or_404
def dettaglio(request, id):
    # Recupera l'entry dal modello UserData o restituisce un errore 404 se non esiste
    entry = get_object_or_404(UserData, id=id)

    # Passa l'entry al template
    context = {
        'entry': entry
    }

    return render(request, 'dettaglio.html', context)

# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
from .models import UserData  # Make sure 'UserData' model is correctly imported

def import_user_data(request):
    try:
        # Path to the Excel file
        file_path = 'Report_Complessivo_AqA_blocco35_Apr.mag.24.xlsx'
        df = pd.read_excel(file_path, sheet_name='Letture')

        # Convert columns to appropriate data types
        df['Data Lettura'] = pd.to_datetime(df['Data Lettura'], errors='coerce', dayfirst=True)
        df['Ora Lettura'] = pd.to_datetime(df['Ora Lettura'], format='%H:%M', errors='coerce').dt.time

        specific_date = '2024-05-06'
        df_filtered = df[(df['Data Lettura'] == specific_date) & (df['Codice Letturista'] == 'LO0414')]
        print(df_filtered)
        if df_filtered.empty:
            return HttpResponse("No matching data found for the specified criteria.")

        df_sorted = df_filtered.sort_values(by='Ora Lettura')

        with transaction.atomic():
            for _, row in df_sorted.iterrows():
                try:
                    user_data = UserData(
                        comune=row['Comune'],
                        indirizzo=row['Indirizzo'],
                        civ=row.get('Civ', None),
                        codice_letturista=row['Codice Letturista'],
                        data_lettura=row['Data Lettura'],
                        ora_lettura=row['Ora Lettura'],
                        latitude=row['Latitude'],
                        longitude=row['Longitude'],
                        altitude=row.get('Altitude', None),
                        lettura1=1,
                        lettura2=2,
                        lettura3=3,
                        link_map=row.get('Link Map', None)
                    )
                    user_data.save()
                    if user_data.pk:
                        print(f"Saved entry: {user_data}")
                    else:
                        print("Save failed")

                except Exception as e:
                    print(f"Error saving entry: {e}")
                    return HttpResponse(f"Error saving entry: {e}")

        return HttpResponse("Data import completed successfully!")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
'''
import os
import torch
from django.conf import settings
from ultralytics import YOLO

def sort_tensor_by_x1(data, cls):
    sorted_data, indices = torch.sort(data[:, 0], dim=0)
    sorted_cls = cls[indices]
    return sorted_cls

def detect_numbers(img):
    model = YOLO('best.pt')
    result_obj_det = model(img)

    boxes = None
    for result in result_obj_det:
        boxes = result.boxes

        # Assicurati che la cartella 'yolo' esista all'interno di MEDIA_ROOT
        save_directory = os.path.join(settings.MEDIA_ROOT, 'yolo')
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Crea il percorso di salvataggio nell'ambito MEDIA_ROOT
        save_path = os.path.join(save_directory, os.path.basename(img))
        # Salva l'immagine con annotazioni nel percorso desiderato
        result.save(save_path)

    if boxes is not None:
        # Estrai il percorso relativo per l'uso nel template
        rel_save_path = os.path.join(settings.MEDIA_URL, 'yolo', os.path.basename(img))
        numbers = sort_tensor_by_x1(boxes.data, boxes.cls)
        return numbers, rel_save_path
    else:
        return "ErrorImage", None

def detection_view(request):
    directory = os.path.join(settings.MEDIA_ROOT, 'testProva')
    results = []
    for image in os.listdir(directory):
        numbers, image_path = detect_numbers(os.path.join(directory, image))
        results.append((image, numbers, image_path))
    return render(request, 'results.html', {'results': results})

'''