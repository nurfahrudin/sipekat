import datetime
from django import forms

from .models import Sertifikat, Pengambil, JENIS_SERTIFIKAT, JENIS_PENGAMBIL, JENIS_BIDANG, Kelurahan, Kecamatan


def year_choices():
	return [(r,r) for r in range(1980, datetime.date.today().year+1)]

class SertifikatForm(forms.ModelForm):
	class Meta:
		model = Sertifikat
		fields = ('pemilik', 'jenis', 'nomor', 'nib', 'luas', 'jns_bidang', 'kecamatan', 'kelurahan', 'tahun', 'keterangan',)

	pemilik = forms.CharField(label='Nama Pemilik', required=True, widget=forms.TextInput(
				attrs={'class':'form-control', 'placeholder':'Nama Pemilik'}
				))
	jenis = forms.ChoiceField(label='Jenis Sertifikat', required=True, choices=JENIS_SERTIFIKAT, widget=forms.Select(
				attrs={'class':'form-control custom-select'}
				))
	nomor = forms.CharField(label='Nomor Hak', required=True, widget=forms.TextInput(
				attrs={'class':'form-control', 'placeholder':'Nomor Hak'}
				))
	nib = forms.CharField(label='Nomor Identitas Bidang', required=True, widget=forms.TextInput(
				attrs={'class':'form-control', 'placeholder':'NIB'}
				))
	luas = forms.IntegerField(label='Luas Tanah (M²)', required=True, widget=forms.TextInput(
				attrs={'class':'form-control', 'placeholder':'Luas Tanah', 'type':'number', 'min':'1'}
				))
	jns_bidang = forms.ChoiceField(label='Jenis Tanah', required=True, choices=JENIS_BIDANG, widget=forms.Select(
				attrs={'class':'form-control custom-select'}
				))
	kecamatan = forms.ModelChoiceField(label='Kecamatan', required=True, queryset=Kecamatan.objects.all(), widget=forms.Select(
				attrs={'class':'form-control custom-select'}
				))
	kelurahan = forms.ModelChoiceField(label='Kelurahan', required=False, queryset=Kelurahan.objects.all(), widget=forms.Select(
				attrs={'class':'form-control custom-select'}
				))
	tahun = forms.TypedChoiceField(label='Tahun', choices=year_choices, initial=datetime.date.today().year, widget=forms.Select(
				attrs={'class':'form-control custom-select'}
				))
	keterangan = forms.CharField(label='Keterangan (Kegiatan)', required=True, widget=forms.Textarea(
				attrs={'class':'form-control', 'placeholder':'Tulis Kegiatan Sertifikat (ex : Hak Tanggungan, Roya, Pemecahan, dll)'}
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
	keterangan = forms.CharField(label='Keterangan', required=False, widget=forms.Textarea(
				attrs={'class':'form-control', 'placeholder':'Tulis Keterangan Pengambilan'}
				))
	gambar = forms.FileField(label='Upload Foto Pengambil', required=False, widget=forms.FileInput(
				attrs={'class':'form-control'}
				))