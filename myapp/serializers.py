from rest_framework import serializers
from .models import UserData

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'


from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']  # Aggiungi altri campi necessari

# serializers.py
from rest_framework import serializers
from .models import UserData

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = [
            'comune', 'indirizzo', 'civ', 'codice_letturista', 'data_lettura',
            'ora_lettura', 'latitude', 'longitude', 'altitude', 'lettura1',
            'lettura2', 'lettura3', 'link_map', 'flag','image'
        ]

    def create(self, validated_data):
        # Creare una nuova istanza di UserData utilizzando i dati validati
        return UserData.objects.create(**validated_data)
