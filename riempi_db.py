import os
import django
import pandas as pd
from datetime import datetime
from myapp.models import UserData  # Replace 'your_app' with the name of your Django app

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')  # Replace 'your_project' with your project name
django.setup()

# Load the Excel file
file_path = 'Report_Complessivo_AqA_blocco35_Apr.mag.24.xlsx'
df = pd.read_excel(file_path, sheet_name='Letture')

# Data Preprocessing: Convert columns to appropriate data types
df['Data Lettura'] = pd.to_datetime(df['Data Lettura'], errors='coerce', dayfirst=True).dt.date
df['Ora Lettura'] = pd.to_datetime(df['Ora Lettura'], format='%H:%M', errors='coerce').dt.time
specific_date = '2024-05-06'  # Adjust the year if needed
df_filtered = df[(df['Data Lettura'] == specific_date) & (df['Codice Letturista'] == 'LO0414')]
df_sorted = df_filtered.sort_values(by='Ora Lettura')
for _, row in df.iterrows():
    try:
        user_data = UserData(
            comune=row['Comune'],
            indirizzo=row['Indirizzo'],
            civ=row['Civ'],
            codice_letturista=row['Codice Letturista'],
            data_lettura=row['Data Lettura'],
            ora_lettura=row['Ora Lettura'],
            latitude=row['Latitude'],
            longitude=row['Longitude'],
            altitude=row.get('Altitude', None),
            lettura1=row.get('Lettura1', None),
            lettura2=row.get('Lettura2', None),
            lettura3=row.get('Lettura3', None),
            link_map=row.get('Link Map', None),
            flag=False
        )
        user_data.save()
        print(f"Saved entry: {user_data}")
    except Exception as e:
        print(f"Error saving entry: {e}")
