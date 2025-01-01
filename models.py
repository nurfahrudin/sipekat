import datetime
from django.db import models

from siwarkah.models import User, Kecamatan, Kelurahan


JENIS_PENGAMBIL = (('','---------'), (1, 'Atas Nama Sendiri'), (2, 'Melalui Kuasa'))
class Pengambil(models.Model):
	jenis = models.IntegerField(null=False)
	nama = models.CharField(max_length=100)
	nik = models.IntegerField(null=False)
	alamat = models.CharField(max_length=280)
	tlp = models.CharField(max_length=13)
	tgl = models.DateTimeField(default=datetime.datetime.today, null=False)
	keterangan = models.CharField(max_length=280)
	gambar =  models.ImageField(upload_to = 'Foto_Pengambil/', null=True)
	create_date = models.DateTimeField(auto_now_add=True, null=False)
	edit_date = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.nama+' - '+self.alamat



JENIS_SERTIFIKAT = (('','---------'), (1, 'Hak Atas Tanah'), (2, 'Hak Tanggungan'), (3, 'Tanah Wakaf'))
JENIS_BIDANG = (('','---------'), (1, 'Pekarangan'), (2, 'Pertanian'), (3, 'Perkebunan'))
class Sertifikat(models.Model):
	pemilik = models.CharField(max_length=100)
	jenis = models.PositiveSmallIntegerField(choices=JENIS_SERTIFIKAT, blank=False)
	nomor = models.CharField(max_length=5)
	nib = models.CharField(max_length=5)
	luas = models.IntegerField(null=False)
	jns_bidang = models.PositiveSmallIntegerField(choices=JENIS_BIDANG, null=False)
	kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
	kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
	tahun = models.IntegerField(null=False)
	keterangan = models.CharField(max_length=280)
	post = models.PositiveSmallIntegerField(default=0)
	post_date = models.DateTimeField(null=True)
	create_date = models.DateTimeField(auto_now_add=True, null=False)
	edit_date = models.DateTimeField(null=True)
	pengambil_id = models.IntegerField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.pemilik