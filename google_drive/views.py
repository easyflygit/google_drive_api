import os
from django.shortcuts import render
import io
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseUpload
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import File
from .serializers import FileSerializer


def file_list(request):
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})


@api_view(['POST'])
def create_file(request):
    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
        file_name = serializer.validated_data.get('name')
        file_content = serializer.validated_data.get('data')

        try:
            # Проверка существования файла token.json
            token_path = os.path.join(os.path.dirname(__file__), '..', 'token.json')
            token_path = os.path.abspath(token_path)

            if not os.path.exists(token_path):
                return Response({'error': 'Token file not found'}, status=500)

            creds = Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/drive.file'])

            service = build('drive', 'v3', credentials=creds)
            file_metadata = {'name': file_name}

            # Использование MediaIoBaseUpload для загрузки содержимого файла
            file_stream = io.BytesIO(file_content.encode('utf-8'))
            media = MediaIoBaseUpload(file_stream, mimetype='text/plain')

            service.files().create(body=file_metadata, media_body=media).execute()

            # Сохраняем информацию о файле в базе данных
            file_obj = File(name=file_name, data=file_content)
            file_obj.save()
        except FileNotFoundError:
            return Response({'error': 'Token file not found'}, status=500)
        except Exception as e:
            return Response({'error': 'Failed to create file', 'details': str(e)}, status=500)

        return Response({'message': 'File created successfully'}, status=201)
    else:
        return Response(serializer.errors, status=400)
