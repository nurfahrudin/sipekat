import os
import json
import datetime
from django.conf import settings
from django.db import connection
from django.contrib import messages
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseServerError, JsonResponse

from siwarkah.views import items
from siwarkah.models import Kecamatan, Kelurahan, dictfetchall
from .models import Sertifikat, Pengambil
from .forms import SertifikatForm, PengambilForm



def error_404(request, exception):
	return render(request, 'warkah/404.html', {'name':'404'})
def error_500(request):
	return render(request, 'warkah/404.html', {'name':'500'})


cursor = connection.cursor()

def ZeroDivision(num1, num2):
	try:
		result = (num1/num2)*100
	except ZeroDivisionError:
		result = 0
	return int(result)



#-----------------------#
#	   START INDEX  	#
#-----------------------#
def index(request):
	if ('user' in request.session) and ('uid' in request.session):
		p_query1 = 'select count(p.id) FROM sipekat_pengambil p WHERE p.jenis==1'
		p_query2 = 'select count(p.id) FROM sipekat_pengambil p WHERE p.jenis==2'
		p_cursor1, p_cursor2 = connection.cursor(), connection.cursor()
		p_cursor1.execute(p_query1)
		p_cursor2.execute(p_query2)
		p_data = p_cursor1.fetchall()+p_cursor2.fetchall()

		cs, cs1, cs2, cp, cp1, cp2 = connection.cursor(), connection.cursor(), connection.cursor(),\
										connection.cursor(), connection.cursor(), connection.cursor()
		qs = 'select count(s.id) FROM sipekat_sertifikat s'
		qp = 'select count(p.id) FROM sipekat_pengambil p'
		cs.execute(qs)
		cs1.execute(qs + ' WHERE s.post==0')
		cs2.execute(qs + ' WHERE s.post==1')
		cp.execute(qp)
		cp1.execute(qp + ' WHERE p.jenis==1')
		cp2.execute(qp + ' WHERE p.jenis==2')
		data = cs.fetchall()+cp.fetchall()+cs1.fetchall()+cs2.fetchall()+cp1.fetchall()+cp2.fetchall()

		return render(request, 'sipekat/index.html', {'s_total':data[0][0], 'p_total':data[1][0],
														's_post_0':ZeroDivision(data[2][0],data[0][0]), 's_post_1':ZeroDivision(data[3][0],data[0][0]),
														'p_jenis_1':ZeroDivision(data[4][0],p_data[0][0]), 'p_jenis_2':ZeroDivision(data[5][0],p_data[1][0])})
	else:
		return redirect('/login')
#-----------------------#
#		END INDEX		#
#-----------------------#



#-----------------------#
#	START SERTIFIKAT	#
#-----------------------#
def list_sertifikat(request):
	if ('user' in request.session) and ('uid' in request.session):
		query = 'select count(s.id) from sipekat_sertifikat s '
		cursor, cursor2, cursor3 = connection.cursor(), connection.cursor(), connection.cursor()
		cursor.execute(query)
		cursor2.execute(query + 'where s.jenis==1')
		cursor3.execute(query + 'where s.jenis==2')
		data = cursor.fetchall()+cursor2.fetchall()+cursor3.fetchall()
		return render(request, 'sipekat/data_sertifikat.html', {'s_total':data[0][0], 's_hak_milik':data[1][0], 's_hak_tanggungan':data[2][0], 'items':items()})
	else:
		return redirect('/login')

def table_list_sipekat(request):
	query = 'select s.id,  s.pemilik, s.jenis, s.nomor, s.nib, s.luas, s.keterangan, s.post, k.nama kelurahan from sipekat_sertifikat s join siwarkah_kelurahan k on s.kelurahan_id==k.id'
	cursor = connection.cursor()
	cursor.execute(query)
	obj_list = dictfetchall(cursor)
	result = json.dumps({"data": list(obj_list)})
	return HttpResponse(result, content_type="application/json")

def input_sertifikat(request):
	data = {}
	if request.is_ajax() and request.method == 'POST':
		post = request.POST
		new_sertifikat = Sertifikat(pemilik=post['pemilik'], jenis=post['jenis'], nomor=post['nomor'], nib=post['nib'], luas=post['luas'],
									jns_bidang=post['jns_bidang'], kecamatan_id=post['kecamatan'], kelurahan_id=post['kelurahan'], tahun=post['tahun'],
									keterangan=post['keterangan'], user_id=request.session['uid'])
		try:
			new_sertifikat.save()
			data['msg'] = 'Success'
		except:
			data['msg'] = 'Error'
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		form = SertifikatForm(label_suffix='').as_p()
		split = str(form).split('<p>')
		form_list = list()
		for a in range(len(split)):
			b = (split[a].split('</p>'))
			form_list.append(b)
		result = json.dumps({"form": form_list})
		return HttpResponse(result, content_type="application/json")

def edit_sertifikat(request, id):
	data = {}
	try:
		edit_sertifikat = get_object_or_404(Sertifikat, pk=id)
		if request.method == 'POST':
			post = request.POST
			edit_sertifikat.pemilik			= post['pemilik']
			edit_sertifikat.jenis			= post['jenis']
			edit_sertifikat.nomor			= post['nomor']
			edit_sertifikat.nib				= post['nib']
			edit_sertifikat.luas			= post['luas']
			edit_sertifikat.jns_bidang		= post['jns_bidang']
			edit_sertifikat.kecamatan_id	= post['kecamatan']
			edit_sertifikat.kelurahan_id	= post['kelurahan']
			edit_sertifikat.tahun			= post['tahun']
			edit_sertifikat.keterangan		= post['keterangan']
			edit_sertifikat.edit_date		= datetime.datetime.now()
			edit_sertifikat.user_id			= request.session['uid']
			try:
				edit_sertifikat.save()
				data['msg'] = 'Success'
			except:
				data['msg'] = 'Error'
			return HttpResponse(json.dumps(data), content_type="application/json")
		else:
			form = SertifikatForm(label_suffix='', instance=edit_sertifikat).as_p()
			split = str(form).split('<p>')
			form_list = list()
			for a in range(len(split)):
				b = (split[a].split('</p>'))
				form_list.append(b)
			result = json.dumps({"form": form_list})
			return HttpResponse(result, content_type="application/json")
	except:
		data['msg'] = 'Unknown ID'
		return HttpResponse(json.dumps(data), content_type="application/json")

def hapus_sertifikat(request):
	pk = request.GET.get('pk')
	data = dict()
	try:
		sertifikat = get_object_or_404(Sertifikat, pk=pk)
		sertifikat.delete()
		data['title'] = 'Success!'
		data['msg'] = '<p>Data Sertifikat <b>'+str(sertifikat)+'</b> berhasil dihapus.</p>'
	except:
		data['title'] = 'Peringatan!'
		data['msg'] = '<p>Pilih dulu data yang mau dihapus!</p>\
						<p class="text-secondary"><small>Klik baris data pada tabel untuk memilih data yang ingin dirubah.</small></p>'
	return HttpResponse(json.dumps(data), content_type="application/json")
#-----------------------#
#	 END SERTIFIKAT		#
#-----------------------#



#------------------------------#
# START PENGAMBILAN SERTIFIKAT #
#------------------------------#
def list_ambil_sertifikat(request):
	if ('user' in request.session) and ('uid' in request.session):
		query = 'select count(s.id) from sipekat_sertifikat s '
		cursor, cursor2, cursor3 = connection.cursor(), connection.cursor(), connection.cursor()
		cursor.execute(query)
		cursor2.execute(query + 'where s.post==1')
		cursor3.execute(query + 'where s.post==0')
		data = cursor.fetchall()+cursor2.fetchall()+cursor3.fetchall()
		return render(request, 'sipekat/data_ambil_sertifikat.html', {'s_total':data[0][0], 's_sudah_ambil':data[1][0], 's_belum_ambil':data[2][0], 'items':items()})
	else:
		return redirect('/login')

def ambil_sertifikat(request, id):
	if ('user' in request.session) and ('uid' in request.session):
		dt_sertifikat = []
		sr_id = id.split(",")
		for i in range(len(sr_id)):
			qr_sertifikat = 'select s.pemilik, s.nomor, s.nib, s.luas, s.tahun, kc.nama kecamatan, kl.nama kelurahan, s.keterangan, case when s.jns_bidang == 1 then "Pekarangan" when s.jns_bidang == 2 then "Pertanian" else "Perkebunan" end jns_bidang from sipekat_sertifikat s, siwarkah_kecamatan kc, siwarkah_kelurahan kl where s.id=='+str(sr_id[i])+' and s.kelurahan_id == kl.id and kc.id == kl.kecamatan_id'
			cursor.execute(qr_sertifikat)
			rs_sertifikat = dictfetchall(cursor)
			no = rs_sertifikat[0]
			no['no'] = (i+1)
			dt_sertifikat.append(no)

		if request.method == 'POST':
			post = request.POST
			new_pengambil = Pengambil(jenis=post['jenis'], nama=post['nama'], nik=post['nik'], alamat=post['alamat'], tlp=post['tlp'], keterangan=post['keterangan'],
									gambar=request.FILES['gambar'], user_id=request.session['uid'])
			try:
				new_pengambil.save()
				
				p_edit = get_object_or_404(Pengambil, pk=new_pengambil.id)
				img_src_path = os.path.join(settings.BASE_DIR, 'media/'+str(p_edit.gambar))
				file_name = str(p_edit.gambar).split('/',1)[1]
				from PIL import Image
				im = Image.open(img_src_path)
				im_resized = im.resize((im.width // 2, im.height // 2))
				im_resized.save(str(settings.BASE_DIR)+file_name)

				for i in range(len(sr_id)):
					post_sertifikat = get_object_or_404(Sertifikat, pk=sr_id[i])
					post_sertifikat.post = 1
					post_sertifikat.pengambil_id = new_pengambil.id
					post_sertifikat.post_date = datetime.datetime.now()
					post_sertifikat.save()
				messages.success(request, 'Pengambilan Sertifikat Sukses.')
				return redirect('/sipekat/list/pengambil')
			except:
				messages.error(request, 'Pengambilan Sertifikat Gagal.')
				return redirect('/sipekat/list/ambil-sertifikat')
		return render(request, 'sipekat/form_ambil_sertifikat.html', {'data':dt_sertifikat})
	else:
		return redirect('/login')
#------------------------------#
#  END PENGAMBILAN SERTIFIKAT  #
#------------------------------#



#-----------------------#
#	 START PENGAMBIL	#
#-----------------------#
def list_pengambil(request):
	if ('user' in request.session) and ('uid' in request.session):
		query = 'select count(p.id) from sipekat_pengambil p '
		cursor, cursor2, cursor3 = connection.cursor(), connection.cursor(), connection.cursor()
		cursor.execute(query)
		cursor2.execute(query + 'where p.jenis==1')
		cursor3.execute(query + 'where p.jenis==2')
		data = cursor.fetchall()+cursor2.fetchall()+cursor3.fetchall()
		return render(request, 'sipekat/data_pengambil.html', {'p_total':data[0][0], 'p_sendiri':data[1][0], 'p_kuasa':data[2][0], 'items':items()})
	else:
		return redirect('/login')

def table_list_pengambil(request):
	query = 'select p.id, p.nama, p.nik, p.alamat, p.tlp, strftime("%d-%m-%Y %H:%M:%S", p.tgl) tgl from sipekat_pengambil p order by p.tgl'
	cursor = connection.cursor()
	cursor.execute(query)
	obj_list = dictfetchall(cursor)
	result = json.dumps({"data": list(obj_list)}, cls=DjangoJSONEncoder)
	return HttpResponse(result, content_type="application/json")
#-----------------------#
#	 END PENGAMBIL		#
#-----------------------#



#-----------------------#
#	 CETAK PENGAMBIL	#
#-----------------------#
def cetak_pengambil(request, id):
	if ('user' in request.session) and ('uid' in request.session):
		data_pengambil = {}
		data_sertifikat = []
		idnya = id.split(",")

		qr_pengambil = 'select p.nama, p.nik, p.alamat, p.tlp, strftime("%d-%m-%Y %H:%M:%S", p.tgl) tgl, p.gambar from sipekat_pengambil p where p.id=='+idnya[0]
		cursor.execute(qr_pengambil)
		obj_pengambil = dictfetchall(cursor)
		data_pengambil['nama'] 		= obj_pengambil[0]['nama']
		data_pengambil['nik'] 		= obj_pengambil[0]['nik']
		data_pengambil['alamat'] 	= obj_pengambil[0]['alamat']
		data_pengambil['tlp'] 		= obj_pengambil[0]['tlp']
		data_pengambil['tgl'] 		= obj_pengambil[0]['tgl']
		data_pengambil['gambar']	= '/sipekat/media/'+obj_pengambil[0]['gambar']

		for i in range(len(idnya)):
			qr_sertifikat = 'select p.nama p_nama, p.tgl, s.pemilik, s.nomor, s.nib, s.luas, s.tahun, kc.nama kecamatan, kl.nama kelurahan, s.keterangan, case when s.jns_bidang == 1 then "Pekarangan" when s.jns_bidang == 2 then "Pertanian" else "Perkebunan" end jns_bidang from sipekat_pengambil p, sipekat_sertifikat s, siwarkah_kecamatan kc, siwarkah_kelurahan kl where s.pengambil_id == p.id and p.id=='+str(idnya[i])+' and s.kelurahan_id == kl.id and kc.id == kl.kecamatan_id'
			cursor.execute(qr_sertifikat)
			obj_sertifikat = dictfetchall(cursor)

			print ('++++++++++++++++++++++++++++++++')
			print (len(obj_sertifikat))

			for a in range(len(obj_sertifikat)):
				no = obj_sertifikat[a]
				no['no'] = str(a+1)+'.'
				data_sertifikat.append(no)
		return render(request, 'sipekat/report.html', {'sertifikat':data_sertifikat, 'pengambil':data_pengambil})
	else:
		return redirect('/login')



#-----------#
#	AJAX	#
#-----------#
def load_kelurahan(request):
	kecamatan_id = request.GET.get('kecamatan')
	kelurahan = Kelurahan.objects.all().filter(kecamatan_id=kecamatan_id).order_by('nama')
	result = serializers.serialize("json", kelurahan)
	return HttpResponse(result, content_type="application/json")