import datetime
from django.db import models

from warkah.models import User, Kecamatan, Kelurahan



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



JENIS_KEGIATAN = (('','---------'), (1, 'Hak Tanggungan'), (2, 'Jual Beli'), (3, 'Pemecahan'), (4, 'Pendaftaran SK Hak 1X'),
									(5, 'Pengecekan'), (6, 'Pewarisan'), (7, 'Roya'), (8, 'Wakaf'), (9, 'Lain-Lain'))
JENIS_BIDANG = (('','---------'), (1, 'Pekarangan'), (2, 'Pertanian'), (3, 'Perkebunan'))
class Sertifikat(models.Model):
	pemilik = models.CharField(max_length=100)
	jenis = models.PositiveSmallIntegerField(choices=JENIS_KEGIATAN, blank=False)
	nomor = models.CharField(max_length=5)
	berkas = models.CharField(max_length=5)
	kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
	kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
	keterangan = models.CharField(max_length=280)
	post = models.PositiveSmallIntegerField(default=0)
	post_date = models.DateTimeField(null=True)
	create_date = models.DateTimeField(auto_now_add=True, null=False)
	edit_date = models.DateTimeField(null=True)
	pengambil_id = models.IntegerField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.pemilik