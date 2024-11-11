import re
from django.shortcuts import render
import requests
import pandas as pd
import validators
from requests.exceptions import SSLError
from django.shortcuts import render
from .forms import FileUploadForm
from PyPDF2 import PdfReader
import time
from django.http import JsonResponse


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def faq(request):
    return render(request, 'faq.html')


def update_ping(request):
    links = request.GET.getlist('links[]')  # Получаем список ссылок из GET-запроса
    ping_data = []

    for link in links:
        try:
            start_time = time.time()
            response = requests.get(link, timeout=10)
            ping = int((time.time() - start_time) * 1000)  # Пинг в миллисекундах
            status = 'Online' if response.status_code == 200 else 'Offline'
        except requests.RequestException:
            ping = 'N/A'
            status = 'Offline'

        ping_data.append({'url': link, 'ping': ping, 'status': status})

    return JsonResponse({'ping_data': ping_data})


def check_links(links):
    incorrect_links = []
    correct_links = []
    for link in links:
        if not validators.url(link):
            print(f"Invalid URL structure: {link}")
            incorrect_links.append({'url': link, 'ssl': 'No', 'ping': 'N/A'})
            continue
        try:
            start_time = time.time()
            response = requests.get(link, timeout=10, verify=True)
            ping = int((time.time() - start_time) * 1000)  # пинг в миллисекундах
            print(f"URL: {link}, Status Code: {response.status_code}, Ping: {ping} ms")

            if response.status_code == 200:
                correct_links.append({'url': link, 'ssl': 'Yes', 'ping': ping})
            else:
                incorrect_links.append({'url': link, 'ssl': 'Yes', 'ping': ping})
        except SSLError:
            print(f"SSL certificate error for {link}")
            incorrect_links.append({'url': link, 'ssl': 'No', 'ping': 'N/A'})
        except requests.RequestException as e:
            print(f"Failed to reach {link}. Error: {e}")
            incorrect_links.append({'url': link, 'ssl': 'No', 'ping': 'N/A'})
    return incorrect_links, correct_links


def handle_uploaded_file(file):
    links = []
    url_pattern = r'\b(?:https?|ftp):\/\/[^\s/$.?#].[^\s]*|\b(?:[a-z]+:\/\/)?www\.[^\s/$.?#].[^\s]*|\b[a-z]+:\/\/[^\s]*'

    if file.name.endswith('.pdf'):
        reader = PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            extracted_links = re.findall(url_pattern, text)
            links.extend(extracted_links)

    elif file.name.endswith('.xlsx'):
        data = pd.read_excel(file)
        links.extend(data['links_column'].dropna())

    elif file.name.endswith('.csv'):
        data = pd.read_csv(file)
        links.extend(data['links_column'].dropna())

    unique_links = list(set(links))
    print("All extracted links:", unique_links)

    return check_links(unique_links)


def upload_file0(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            incorrect_links, correct_links = handle_uploaded_file(file)
            return render(request, 'result.html', {
                'incorrect_links': incorrect_links,
                'correct_links': correct_links
            })
    else:
        form = FileUploadForm()
    return render(request, 'upload_index/upload_excel.html', {'form': form})


def upload_file1(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            incorrect_links, correct_links = handle_uploaded_file(file)
            return render(request, 'result.html', {
                'incorrect_links': incorrect_links,
                'correct_links': correct_links
            })
    else:
        form = FileUploadForm()
    return render(request, 'upload_index/upload_csv.html', {'form': form})


def upload_file2(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            incorrect_links, correct_links = handle_uploaded_file(file)
            return render(request, 'result.html', {
                'incorrect_links': incorrect_links,
                'correct_links': correct_links
            })
    else:
        form = FileUploadForm()
    return render(request, 'upload_index/upload_pdf.html', {'form': form})
