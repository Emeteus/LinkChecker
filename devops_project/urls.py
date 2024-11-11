from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from link_checker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('uploas_excel/', views.upload_file0, name='upload_excel'),   # Главная страница
    path('upload_csv/', views.upload_file1, name='upload_csv'),  # Страница для CSV
    path('upload_pdf/', views.upload_file2, name='upload_pdf'),  # Страница для PDF
    path('update_ping/', views.update_ping, name='update_ping'), # Страница для update_ping
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
