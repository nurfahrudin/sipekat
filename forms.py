import datetime
from django import forms

from .models import Sertifikat, Pengambil, JENIS_KEGIATAN, JENIS_PENGAMBIL, JENIS_BIDANG, Kelurahan, Kecamatan


def year_choices():
	return [(r,r) for r in range(1980, datetime.date.today().year+1)]

class SertifikatForm(forms.ModelForm):
	class Meta:
		model = Sertifikat
		fields = ('pemilik', 'jenis', 'nomor', 'berkas', 'kecamatan', 'kelurahan', 'keterangan')

	pemilik = forms.CharField(label='Nama Pemilik', required=True, widget=forms.TextInput(
				attrs={'class':'form-control', 'placeholder':'Nama Pemilik'}
				))
	jenis = forms.ChoiceField(label='Jenis Kegiatan', required=True, choices=JENIS_KEGIATAN, widget=forms.Select(
				attrs={'class':'form-control custom-select'}
				))
	nomor = forms.CharField(label='Nomor Hak', widget=forms.TextInput(
				attrs={'class':'form-control', 'placeholder':'Nomor Hak'}
				))
	berkas = forms.CharField(label='Nomor Berkas', required=True, widget=forms.TextInput(
				attrs={'class':'form-control', 'placeholder':'Nomor Berkas Pendaftaran'}
				))
	kecamatan = forms.ModelChoiceField(label='Kecamatan', required=True, queryset=Kecamatan.objects.all(), widget=forms.Select(
				attrs={'class':'form-control custom-select'}
				))
	kelurahan = forms.ModelChoiceField(label='Kelurahan', required=False, queryset=Kelurahan.objects.all(), widget=forms.Select(
				attrs={'class':'form-control custom-select'}
				))
	keterangan = forms.CharField(label='Keterangan (Kegiatan)', required=True, widget=forms.TextInput(
				attrs={'class':'form-control', 'placeholder':'Tulis Kegiatan Sertifikat (ex : lokasi/tempat penyimpanan, dll)'}
				))

class PengambilForm(forms.ModelForm):
	class Meta:
		model = Pengambil
		fields = ('jenis', 'nama', 'nik', 'alamat', 'tlp', 'gambar')
	
	jenis = forms.ChoiceField(label='Jenis Pengambilan', required=True, choices=JENIS_PENGAMBIL, widget=forms.Select(
			attrs={'class':'form-control custom select'}
			))
	nama = forms.CharField(label='Nama', required=True, widget=forms.TextInput(
			attrs={'class':'form-control', 'placeholder':'Nama Pengambil Sertifikat'}
			))
	nik = forms.IntegerField(label='NIK', required=True, widget=forms.TextInput(
			attrs={'class':'form-control', 'placeholder':'NIK Pengambil Sertifikat'}
			))
	alamat = forms.CharField(label='Alamat', required=True, widget=forms.Textarea(
			attrs={'class':'form-control', 'placeholder':'Alamat Pengambil Sertifikat'}
			))
	tlp = forms.CharField(label='No. HP', required=True, widget=forms.TextInput(
			attrs={'class':'form-control', 'placeholder':'Nomor Tlp/HP Pengambil Sertifikat'}
			))
	keterangan = forms.CharField(label='Keterangan', required=False, widget=forms.TextInput(
				attrs={'class':'form-control', 'placeholder':'Tulis Keterangan Pengambilan'}
				))
	gambar = forms.FileField(label='Upload Foto Pengambil', required=False, widget=forms.FileInput(
				attrs={'class':'form-control'}
				))