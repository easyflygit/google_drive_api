import os
from django.shortcuts import render
import json
import io
from django.http import JsonResponse
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseUpload
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import File


def file_list(request):
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})


@csrf_exempt
@require_http_methods(["POST"])
def create_file(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON', 'details': str(e)}, status=400)

    file_name = data.get('name')
    file_content = data.get('data')

    if not file_name or not file_content:
        return JsonResponse({'error': 'Missing name or data in the request'}, status=400)

    try:
        # Проверка существования файла token.json
        token_path = os.path.join(os.path.dirname(__file__), '..', 'token.json')
        token_path = os.path.abspath(token_path)

        if not os.path.exists(token_path):
            return JsonResponse({'error': 'Token file not found'}, status=500)

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
        return JsonResponse({'error': 'Token file not found'}, status=500)
    except Exception as e:
        return JsonResponse({'error': 'Failed to to to create file', 'details': str(e)}, status=500)

    return JsonResponse({'message': 'File created successfully'}, status=201)