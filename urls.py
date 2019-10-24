from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index_sipekat'),
    path('ajax/load-kelurahan/', views.load_kelurahan, name='ajax_load_kelurahan'),
    
    # sertifikat
    path('list/sertifikat/', views.list_sertifikat, name='list_sertifikat'),
    path('ajax/table-list-sipekat/', views.table_list_sipekat, name='ajax_table_list_sipekat'),
    path('input/sertifikat/', views.input_sertifikat, name='input_sertifikat'),
    path('edit/<int:id>/sertifikat/', views.edit_sertifikat, name='edit_sertifikat'),
    path('hapus/sertifikat/', views.hapus_sertifikat, name='hapus_sertifikat'),

    # pengambil
    path('list/pengambil/', views.list_pengambil, name='list_pengambil'),
    path('ajax/table-list-pengambil/', views.table_list_pengambil, name='ajax_table_list_pengambil'),
    path('cetak/<str:id>/pengambil/', views.cetak_pengambil, name='cetak_pengambil'),

    # ambil_sertifikat
    path('list/ambil-sertifikat/', views.list_ambil_sertifikat, name='list_ambil_sertifikat'),
    path('ajax/table-list-ambil/', views.table_list_ambil, name='ajax_table_list_ambil'),
    path('ambil/<str:id>/sertifikat/', views.ambil_sertifikat, name='ambil_sertifikat'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)