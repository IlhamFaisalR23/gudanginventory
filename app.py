import os
from flask import Flask, render_template,Response, request, redirect, url_for, session, flash, send_from_directory,jsonify
from flask_mysqldb import MySQL,MySQLdb
import MySQLdb.cursors
from werkzeug.utils import secure_filename
import io
import xlwt
import datetime

style1 = xlwt.XFStyle()
style1.num_format_str = 'DD-MM-YYYY'

#Format Currency
style2 = xlwt.XFStyle()
style2.num_format_str = '$#,##0.00'
app = Flask(__name__)

UPLOAD_FOLDER = 'static/img/barang/'

app.secret_key = 'kunci rahasia'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventarisgudang'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'nip' in request.form:
        email = request.form['email']
        nip = request.form['nip']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pegawai WHERE email = %s AND nip = %s', (email, nip,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id_user'] = account['id_user']
            session['email'] = account['email']
            session['tingkat'] = account['tingkat']
            session['id_status'] = account['id_status']
            return redirect(url_for('index'))
        else:
            msg = 'Nama Pengguna atau Kata Sandi Salah!'
    return render_template('loginpage/login.html', msg=msg)

@app.route('/index')
def index():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pegawai INNER JOIN jabatan on jabatan.kode_jabatan = pegawai.kode_jabatan WHERE id_user = %s', (session['id_user'],))
        account = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahbarang FROM masterbarang')
        jumlahbarang = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT SUM(jumlah*hrg_satuan) AS totalpengeluaran FROM barangkeluar INNER JOIN stokbarang ON stokbarang.`id_stok`=barangkeluar.`id_stok` ORDER BY MONTH(tgl_keluar)')
        totalpengeluaran = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahpermintaan FROM permintaan')
        jumlahpermintaan = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahpegawai FROM pegawai')
        jumlahpegawai = cursor.fetchone()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM masterbarang LEFT JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` LEFT JOIN satuanbarang ON satuanbarang.`id_satuan` = masterbarang.`id_satuan` LEFT JOIN sumberdana ON sumberdana.idsumberdana = masterbarang.idsumberdana LEFT JOIN kategoribarang ON kategoribarang.`id_kategori`=masterbarang.`id_kategori`')
        data = cur.fetchall()
        cur.close()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS barangsedikit FROM masterbarang INNER JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` WHERE stok < 3')
        barangsedikit = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS totalpegawai FROM pegawai')
        totalpegawai = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjanuari FROM permintaan WHERE MONTH(tanggalpesan)=1; ')
        permintaanjanuari = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanfebruari FROM permintaan WHERE MONTH(tanggalpesan)=2; ')
        permintaanfebruari = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanmaret FROM permintaan WHERE MONTH(tanggalpesan)=3; ')
        permintaanmaret = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanapril FROM permintaan WHERE MONTH(tanggalpesan)=4; ')
        permintaanapril = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanmei FROM permintaan WHERE MONTH(tanggalpesan)=5; ')
        permintaanmei = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjuni FROM permintaan WHERE MONTH(tanggalpesan)=6; ')
        permintaanjuni = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjuli FROM permintaan WHERE MONTH(tanggalpesan)=7; ')
        permintaanjuli = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanagustus FROM permintaan WHERE MONTH(tanggalpesan)=8; ')
        permintaanagustus = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanseptember FROM permintaan WHERE MONTH(tanggalpesan)=9; ')
        permintaanseptember = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanoktober FROM permintaan WHERE MONTH(tanggalpesan)=10; ')
        permintaanoktober = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaannovember FROM permintaan WHERE MONTH(tanggalpesan)=11; ')
        permintaannovember = cursor.fetchall()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaandesember FROM permintaan WHERE MONTH(tanggalpesan)=12; ')
        permintaandesember = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM masterbarang LEFT JOIN permintaan ON permintaan.`id_barang`=masterbarang.`id_barang` WHERE MONTH(tanggalpesan)=MONTH(CURRENT_DATE()) ORDER BY RAND() LIMIT 1')
        permintaanbarang = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT SUM(jumlahpesan) AS totalpermintaan,namabarang FROM permintaan LEFT JOIN masterbarang ON masterbarang.`id_barang`=permintaan.`id_barang` GROUP BY permintaan.id_barang')
        permintaanbaranglagi = cursor.fetchall()
        return render_template('index.html',daftarbarang=data,totalpengeluaran=totalpengeluaran, permintaanbaranglagi=permintaanbaranglagi,permintaanjanuari=permintaanjanuari,permintaanfebruari=permintaanfebruari,permintaanmaret=permintaanmaret,permintaanapril=permintaanapril,permintaanmei=permintaanmei,permintaanjuni=permintaanjuni,permintaanjuli=permintaanjuli,permintaanagustus=permintaanagustus,permintaanseptember=permintaanseptember,permintaanoktober=permintaanoktober,permintaannovember=permintaannovember,permintaandesember=permintaandesember,jumlahbarang=jumlahbarang, jumlahpermintaan=jumlahpermintaan, jumlahpegawai=jumlahpegawai, barangsedikit=barangsedikit, account=account, totalpegawai=totalpegawai)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):

    return render_template('500.html'),500

    
@app.route('/kepgud/formatpengadaan/download/report/excel', methods=['GET','POST'])
def laporan_pengadaan():

  tgl_masuk = request.form['tgl_masuk']

  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
       
  cursor.execute("SELECT id_barang,namabarang, namakategori, stok,nama_satuan,merk,namasumberdana,hrg_satuan,total,tgl_masuk FROM masterbarang LEFT JOIN kategoribarang ON kategoribarang.`id_kategori`=masterbarang.`id_kategori` LEFT JOIN stokbarang ON stokbarang.`id_stok`=masterbarang.`id_stok` LEFT JOIN satuanbarang ON satuanbarang.`id_satuan`=masterbarang.`id_satuan` LEFT JOIN sumberdana ON sumberdana.`idsumberdana`=masterbarang.`idsumberdana` WHERE DATE_FORMAT(tgl_masuk, '%%Y-%%m') = %s",[tgl_masuk])
  mysql.connection.commit()
  result = cursor.fetchall()
   
  #output in bytes
  output = io.BytesIO()
  #create WorkBook object
  workbook = xlwt.Workbook()
  #add a sheet
  sh = workbook.add_sheet('Daftar Barang')
   
  #add headers
  sh.write(0, 0, 'ID Barang')
  sh.write(0, 1, 'Nama Barang')
  sh.write(0, 2, 'Kategori')
  sh.write(0, 3, 'Jumlah Barang')
  sh.write(0, 4, 'Satuan')
  sh.write(0, 5, 'Merk Barang')
  sh.write(0, 6, 'Sumber Dana')
  sh.write(0, 7, 'Harga Satuan')
  sh.write(0, 8, 'Total Harga')
  sh.write(0, 9, 'Tanggal Masuk')
   
  idx = 0
  for row in result:
   sh.write(idx+1, 0, str(row['id_barang']))
   sh.write(idx+1, 1, row['namabarang'])
   sh.write(idx+1, 2, row['namakategori'])
   sh.write(idx+1, 3, row['stok'])
   sh.write(idx+1, 4, row['nama_satuan'])
   sh.write(idx+1, 5, row['merk'])
   sh.write(idx+1, 6, row['namasumberdana'])
   sh.write(idx+1, 7, row['hrg_satuan'])
   sh.write(idx+1, 8, row['total'])
   sh.write(idx+1, 9,row['tgl_masuk'],style1)
   idx += 1
   
  workbook.save(output)
  output.seek(0)
   
  return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=laporan_pengadaan.xls"})


@app.route('/download/report/excel')
def laporan_pengambilan():
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   
  cursor.execute("SELECT * FROM permintaan INNER JOIN masterbarang on masterbarang.id_barang = permintaan.id_barang INNER JOIN jabatan on jabatan.kode_jabatan = permintaan.kode_jabatan INNER JOIN pegawai on pegawai.id_user = permintaan.id_user INNER JOIN unitkerja ON unitkerja.id_unitkerja=permintaan.id_unitkerja INNER JOIN statuspesanan ON statuspesanan.idstatuspesanan=permintaan.idstatuspesanan")
  result = cursor.fetchall()
   
  #output in bytes
  output = io.BytesIO()
  #create WorkBook object
  workbook = xlwt.Workbook()
  #add a sheet
  sh = workbook.add_sheet('Daftar Barang')
   
  #add headers
  sh.write(0, 0, 'ID Permintaan')
  sh.write(0, 1, 'Nama Barang')
  sh.write(0, 2, 'Jumlah Permintaan')
  sh.write(0, 3, 'Nama Pemesan')
  sh.write(0, 4, 'Status Pesanan')
   
  idx = 0
  for row in result:
   sh.write(idx+1, 0, str(row['id_permintaan']))
   sh.write(idx+1, 1, row['namabarang'])
   sh.write(idx+1, 2, row['jumlahpesan'])
   sh.write(idx+1, 3, row['nama'])
   sh.write(idx+1, 4, row['namastatuspesanan'])
   idx += 1
   
  workbook.save(output)
  output.seek(0)
   
  return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=laporan_pengambilan.xls"})

@app.route('/kepsek/homekepsek')
def homekepsek():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pegawai INNER JOIN jabatan on jabatan.kode_jabatan = pegawai.kode_jabatan WHERE id_user = %s', (session['id_user'],))
        account = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahbarang FROM masterbarang')
        jumlahbarang = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahpermintaan FROM permintaan')
        jumlahpermintaan = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahpegawai FROM pegawai')
        jumlahpegawai = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS barangsedikit FROM masterbarang INNER JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` WHERE stok < 3')
        barangsedikit = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS totalpegawai FROM pegawai')
        totalpegawai = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjanuari FROM permintaan WHERE MONTH(tanggalpesan)=1; ')
        permintaanjanuari = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanfebruari FROM permintaan WHERE MONTH(tanggalpesan)=2; ')
        permintaanfebruari = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanmaret FROM permintaan WHERE MONTH(tanggalpesan)=3; ')
        permintaanmaret = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanapril FROM permintaan WHERE MONTH(tanggalpesan)=4; ')
        permintaanapril = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanmei FROM permintaan WHERE MONTH(tanggalpesan)=5; ')
        permintaanmei = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjuni FROM permintaan WHERE MONTH(tanggalpesan)=6; ')
        permintaanjuni = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjuli FROM permintaan WHERE MONTH(tanggalpesan)=7; ')
        permintaanjuli = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanagustus FROM permintaan WHERE MONTH(tanggalpesan)=8; ')
        permintaanagustus = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanseptember FROM permintaan WHERE MONTH(tanggalpesan)=9; ')
        permintaanseptember = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanoktober FROM permintaan WHERE MONTH(tanggalpesan)=10; ')
        permintaanoktober = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaannovember FROM permintaan WHERE MONTH(tanggalpesan)=11; ')
        permintaannovember = cursor.fetchall()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaandesember FROM permintaan WHERE MONTH(tanggalpesan)=12; ')
        permintaandesember = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM masterbarang LEFT JOIN permintaan ON permintaan.`id_barang`=masterbarang.`id_barang` WHERE MONTH(tanggalpesan)=MONTH(CURRENT_DATE()) ORDER BY RAND() LIMIT 1')
        permintaanbarang = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT SUM(jumlah*hrg_satuan) AS totalpengeluaran FROM barangkeluar INNER JOIN stokbarang ON stokbarang.`id_stok`=barangkeluar.`id_stok` ORDER BY MONTH(tgl_keluar)')
        totalpengeluaran = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT SUM(jumlahpesan) AS totalpermintaan,namabarang FROM permintaan LEFT JOIN masterbarang ON masterbarang.`id_barang`=permintaan.`id_barang` GROUP BY permintaan.id_barang')
        permintaanbaranglagi = cursor.fetchall()

        return render_template('halamankepalasekolah/homekepsek.html', totalpengeluaran=totalpengeluaran ,permintaanbaranglagi=permintaanbaranglagi,permintaanjanuari=permintaanjanuari,permintaanfebruari=permintaanfebruari,permintaanmaret=permintaanmaret,permintaanapril=permintaanapril,permintaanmei=permintaanmei,permintaanjuni=permintaanjuni,permintaanjuli=permintaanjuli,permintaanagustus=permintaanagustus,permintaanseptember=permintaanseptember,permintaanoktober=permintaanoktober,permintaannovember=permintaannovember,permintaandesember=permintaandesember,jumlahbarang=jumlahbarang, jumlahpermintaan=jumlahpermintaan, jumlahpegawai=jumlahpegawai, barangsedikit=barangsedikit, account=account, totalpegawai=totalpegawai)
    return redirect(url_for('login'))

@app.route('/kepsek/homekepsek/profile')
def profilkepsek():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pegawai LEFT JOIN jabatan ON jabatan.kode_jabatan = pegawai.kode_jabatan LEFT JOIN status ON status.`id_status` = pegawai.`id_status` WHERE id_user = %s', (session['id_user'],))
        account = cursor.fetchone()
        return render_template('halamankepalasekolah/profilkepsek.html', account=account)
    return redirect(url_for('login'))

@app.route('/img/<int:img_id>')
def serve_img(img_id):
    pass

@app.route('/kepsek/grafikkepsek')
def grafikkepsek():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pegawai INNER JOIN jabatan on jabatan.kode_jabatan = pegawai.kode_jabatan WHERE id_user = %s', (session['id_user'],))
        account = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahbarang FROM masterbarang')
        jumlahbarang = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahpermintaan FROM permintaan')
        jumlahpermintaan = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahpegawai FROM pegawai')
        jumlahpegawai = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS barangsedikit FROM masterbarang INNER JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` WHERE stok < 3')
        barangsedikit = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS totalpegawai FROM pegawai')
        totalpegawai = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjanuari FROM permintaan WHERE MONTH(tanggalpesan)=1; ')
        permintaanjanuari = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanfebruari FROM permintaan WHERE MONTH(tanggalpesan)=2; ')
        permintaanfebruari = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanmaret FROM permintaan WHERE MONTH(tanggalpesan)=3; ')
        permintaanmaret = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanapril FROM permintaan WHERE MONTH(tanggalpesan)=4; ')
        permintaanapril = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanmei FROM permintaan WHERE MONTH(tanggalpesan)=5; ')
        permintaanmei = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjuni FROM permintaan WHERE MONTH(tanggalpesan)=6; ')
        permintaanjuni = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjuli FROM permintaan WHERE MONTH(tanggalpesan)=7; ')
        permintaanjuli = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanagustus FROM permintaan WHERE MONTH(tanggalpesan)=8; ')
        permintaanagustus = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanseptember FROM permintaan WHERE MONTH(tanggalpesan)=9; ')
        permintaanseptember = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanoktober FROM permintaan WHERE MONTH(tanggalpesan)=10; ')
        permintaanoktober = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaannovember FROM permintaan WHERE MONTH(tanggalpesan)=11; ')
        permintaannovember = cursor.fetchall()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaandesember FROM permintaan WHERE MONTH(tanggalpesan)=12; ')
        permintaandesember = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM masterbarang LEFT JOIN permintaan ON permintaan.`id_barang`=masterbarang.`id_barang` WHERE MONTH(tanggalpesan)=MONTH(CURRENT_DATE()) ORDER BY RAND() LIMIT 1')
        permintaanbarang = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT SUM(jumlahpesan) AS totalpermintaan,namabarang FROM permintaan LEFT JOIN masterbarang ON masterbarang.`id_barang`=permintaan.`id_barang` GROUP BY permintaan.id_barang')
        permintaanbaranglagi = cursor.fetchall()

    return render_template('halamankepalasekolah/grafik.html',permintaanbaranglagi=permintaanbaranglagi,permintaanjanuari=permintaanjanuari,permintaanfebruari=permintaanfebruari,permintaanmaret=permintaanmaret,permintaanapril=permintaanapril,permintaanmei=permintaanmei,permintaanjuni=permintaanjuni,permintaanjuli=permintaanjuli,permintaanagustus=permintaanagustus,permintaanseptember=permintaanseptember,permintaanoktober=permintaanoktober,permintaannovember=permintaannovember,permintaandesember=permintaandesember,jumlahbarang=jumlahbarang, jumlahpermintaan=jumlahpermintaan, jumlahpegawai=jumlahpegawai, barangsedikit=barangsedikit, account=account, totalpegawai=totalpegawai)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id_user', None)
   session.pop('email', None)
   return redirect(url_for('login'))

@app.route('/kepsek/listpermintaan')
def daftarpermintaan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM permintaan INNER JOIN masterbarang on masterbarang.id_barang = permintaan.id_barang INNER JOIN jabatan on jabatan.kode_jabatan = permintaan.kode_jabatan INNER JOIN pegawai on pegawai.id_user = permintaan.id_user WHERE idstatuspesanan='1'")
    data = cur.fetchall()
    cur.close()
    return render_template('halamankepalasekolah/permintaan.html', permintaans=data)

@app.route('/kepsek/listpermintaan/accpermintaan/<string:id>', methods=['GET','POST'])
def accpermintaan(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        UPDATE permintaan SET idstatuspesanan = '5' WHERE id_permintaan=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('daftarpermintaan'))

    return render_template('halamankepalasekolah/permintaan.html')

@app.route('/kepsek/listpermintaan/tolakpermintaan/<string:id>', methods=['GET','POST'])
def tolakpermintaan(id):
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
        SELECT * FROM permintaan WHERE id_permintaan=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalasekolah/tolakpermintaan.html', row=row)
    else:
        alasan = request.form['alasan']

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        UPDATE permintaan 
        SET 
            idstatuspesanan = '4',
            alasan = %s
        WHERE
            id_permintaan = %s;
        ''',(alasan,id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('daftarpermintaan'))

# Batas Dari Halaman Kepala Sekolah #

@app.route('/kepgud/homekepgud')
def homekepgud():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pegawai INNER JOIN jabatan on jabatan.kode_jabatan = pegawai.kode_jabatan WHERE id_user = %s', (session['id_user'],))
        account = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT SUM(jumlah*hrg_satuan) AS totalpengeluaran FROM barangkeluar INNER JOIN stokbarang ON stokbarang.`id_stok`=barangkeluar.`id_stok` ORDER BY MONTH(tgl_keluar)')
        totalpengeluaran = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahbarang FROM masterbarang')
        jumlahbarang = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahpermintaan FROM permintaan')
        jumlahpermintaan = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS jumlahpegawai FROM pegawai')
        jumlahpegawai = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS barangsedikit FROM masterbarang INNER JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` WHERE stok < 3')
        barangsedikit = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS totalpegawai FROM pegawai')
        totalpegawai = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjanuari FROM permintaan WHERE MONTH(tanggalpesan)=1; ')
        permintaanjanuari = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanfebruari FROM permintaan WHERE MONTH(tanggalpesan)=2; ')
        permintaanfebruari = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanmaret FROM permintaan WHERE MONTH(tanggalpesan)=3; ')
        permintaanmaret = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanapril FROM permintaan WHERE MONTH(tanggalpesan)=4; ')
        permintaanapril = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanmei FROM permintaan WHERE MONTH(tanggalpesan)=5; ')
        permintaanmei = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjuni FROM permintaan WHERE MONTH(tanggalpesan)=6; ')
        permintaanjuni = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanjuli FROM permintaan WHERE MONTH(tanggalpesan)=7; ')
        permintaanjuli = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanagustus FROM permintaan WHERE MONTH(tanggalpesan)=8; ')
        permintaanagustus = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanseptember FROM permintaan WHERE MONTH(tanggalpesan)=9; ')
        permintaanseptember = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaanoktober FROM permintaan WHERE MONTH(tanggalpesan)=10; ')
        permintaanoktober = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaannovember FROM permintaan WHERE MONTH(tanggalpesan)=11; ')
        permintaannovember = cursor.fetchall()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS permintaandesember FROM permintaan WHERE MONTH(tanggalpesan)=12; ')
        permintaandesember = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM masterbarang LEFT JOIN permintaan ON permintaan.`id_barang`=masterbarang.`id_barang` WHERE MONTH(tanggalpesan)=MONTH(CURRENT_DATE()) ORDER BY RAND() LIMIT 1')
        permintaanbarang = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT SUM(jumlahpesan) AS totalpermintaan,namabarang FROM permintaan LEFT JOIN masterbarang ON masterbarang.`id_barang`=permintaan.`id_barang` GROUP BY permintaan.id_barang')
        permintaanbaranglagi = cursor.fetchall()

        return render_template('halamankepalagudang/homekepgud.html',totalpengeluaran=totalpengeluaran,permintaanbaranglagi=permintaanbaranglagi,permintaanjanuari=permintaanjanuari,permintaanfebruari=permintaanfebruari,permintaanmaret=permintaanmaret,permintaanapril=permintaanapril,permintaanmei=permintaanmei,permintaanjuni=permintaanjuni,permintaanjuli=permintaanjuli,permintaanagustus=permintaanagustus,permintaanseptember=permintaanseptember,permintaanoktober=permintaanoktober,permintaannovember=permintaannovember,permintaandesember=permintaandesember,jumlahbarang=jumlahbarang, jumlahpermintaan=jumlahpermintaan, jumlahpegawai=jumlahpegawai, barangsedikit=barangsedikit, account=account, totalpegawai=totalpegawai)
    return redirect(url_for('login'))
@app.route('/kepgud/homekepgud/barangsedikit')
def barangsedikit():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM masterbarang LEFT JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` LEFT JOIN rak ON rak.id_rak = stokbarang.id_rak LEFT JOIN satuanbarang ON satuanbarang.id_satuan = masterbarang.id_satuan LEFT JOIN kategoribarang ON kategoribarang.id_kategori=masterbarang.id_kategori WHERE stok < 3')
        barangsedikit = cursor.fetchall()
        return render_template('halamankepalagudang/baranghampirhabis.html', barangsedikit=barangsedikit)
    return redirect(url_for('login'))
    
@app.route('/kepgud/homekepgud/barangsedikit/download/report/excel', methods=['GET','POST'])
def laporan_baranghampirhabis():

  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute("SELECT * FROM masterbarang LEFT JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` LEFT JOIN rak ON rak.id_rak = stokbarang.id_rak LEFT JOIN satuanbarang ON satuanbarang.id_satuan = masterbarang.id_satuan LEFT JOIN kategoribarang ON kategoribarang.id_kategori=masterbarang.id_kategori WHERE stok < 3")
  mysql.connection.commit()
  result = cursor.fetchall()
   
  #output in bytes
  output = io.BytesIO()
  #create WorkBook object
  workbook = xlwt.Workbook()
  #add a sheet
  sh = workbook.add_sheet('Daftar Barang Hampir Habis')
   
  #add headers
  sh.write(0, 0, 'Kode Stok')
  sh.write(0, 1, 'Nama Barang')
  sh.write(0, 2, 'Merk Barang')
  sh.write(0, 3, 'Stok Barang')
  sh.write(0, 4, 'Kategori Barang')
  sh.write(0, 5, 'Satuan Barang')
  sh.write(0, 6, 'Nama Rak')
   
  idx = 0
  for row in result:
   sh.write(idx+1, 0, str(row['id_stok']))
   sh.write(idx+1, 1, row['namabarang'])
   sh.write(idx+1, 2, row['merk'])
   sh.write(idx+1, 3, row['stok'])
   sh.write(idx+1, 4, row['namakategori'])
   sh.write(idx+1, 5,row['nama_satuan'])
   sh.write(idx+1, 6,row['nama_rak'])
   idx += 1
   
  workbook.save(output)
  output.seek(0)
   
  return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=barang_hampirhabis.xls"})


@app.route('/kepgud/logout')
def logoutkepgud():
   session.pop('loggedin', None)
   session.pop('id_user', None)
   session.pop('email', None)
   return redirect(url_for('login'))

@app.route('/kepgud/homekepgud/profile')
def profilkepgud():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pegawai LEFT JOIN jabatan ON jabatan.kode_jabatan = pegawai.kode_jabatan LEFT JOIN status ON status.`id_status` = pegawai.`id_status` LEFT JOIN unitkerja ON unitkerja.id_unitkerja = pegawai.id_unitkerja WHERE id_user = %s', (session['id_user'],))
        account = cursor.fetchone()
        return render_template('halamankepalagudang/profilkepgud.html', account=account)
    return redirect(url_for('login'))

@app.route('/kepgud/listpermintaan')
def listpermintaankepgud():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM permintaan INNER JOIN masterbarang ON masterbarang.id_barang = permintaan.id_barang INNER JOIN jabatan ON jabatan.kode_jabatan = permintaan.kode_jabatan INNER JOIN pegawai ON pegawai.id_user = permintaan.id_user INNER JOIN unitkerja ON unitkerja.id_unitkerja=permintaan.id_unitkerja INNER JOIN statuspesanan ON statuspesanan.`idstatuspesanan`=permintaan.`idstatuspesanan`")
    data = cur.fetchall()
    cur.close()
    return render_template('halamankepalagudang/permintaan.html', permintaans=data)

@app.route('/kepgud/daftarpengguna')
def daftarpengguna():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pegawai LEFT JOIN jabatan ON jabatan.`kode_jabatan`=pegawai.`kode_jabatan` LEFT JOIN unitkerja ON unitkerja.`id_unitkerja`=pegawai.`id_unitkerja` LEFT JOIN status ON status.`id_status`=pegawai.`id_status`")
    pengguna = cur.fetchall()
    cur.close()
    return render_template('halamankepalagudang/daftarpengguna.html', pengguna=pengguna)

@app.route('/kepgud/daftarpengguna/editpengguna/<int:id>', methods=['GET', 'POST'])
def editpengguna(id):
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM jabatan')
        jabatan = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM unitkerja')
        unitkerja = cursor.fetchall()
        cursor.close()


        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM pegawai LEFT JOIN jabatan ON jabatan.kode_jabatan = pegawai.kode_jabatan LEFT JOIN unitkerja ON unitkerja.id_unitkerja = pegawai.id_unitkerja WHERE id_user=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalagudang/editpengguna.html', jabatan=jabatan,unitkerja=unitkerja,row=row)
    else:
        kode_jabatan = request.form['kode_jabatan']
        nama = request.form['nama']
        nip = request.form['nip']
        email = request.form['email']
        nomor_tlp = request.form['nomor_tlp']
        id_unitkerja = request.form['id_unitkerja']
        tingkat = request.form['tingkat']

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        UPDATE pegawai 
        SET 
            kode_jabatan = %s,
            nama = %s,
            nip = %s,
            email = %s,
            nomor_tlp = %s,
            id_unitkerja = %s,
            tingkat = %s
        WHERE
            id_user = %s;
        ''',(kode_jabatan, nama, nip, email,nomor_tlp,id_unitkerja,tingkat,id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('daftarpengguna'))

@app.route('/kepgud/daftarpengguna/aktifakun/<int:id>', methods=['GET','POST'])
def aktifakun(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        UPDATE pegawai SET id_status = 'S1' WHERE id_user=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('daftarpengguna'))

    return render_template('halamankepalagudang/daftarpengguna.html')

@app.route('/kepgud/daftarpengguna/nonaktifakun/<int:id>', methods=['GET','POST'])
def nonaktifakun(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        UPDATE pegawai SET id_status = 'S2' WHERE id_user=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('daftarpengguna'))

    return render_template('halamankepalagudang/daftarpengguna.html')

@app.route('/kepgud/daftarbarang')
def daftarbarang():

    cursor = mysql.connection.cursor()
    cursor.execute('select * from satuanbarang')
    satuanbarang = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute('select * from supplier')
    supplier = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute('select * from sumberdana')
    sumberdana = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute('select * from rak')
    rak = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM kategoribarang')
    kategoribarang = cursor.fetchall()
    cursor.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM masterbarang LEFT JOIN stokbarang ON stokbarang.id_stok = masterbarang.id_stok LEFT JOIN rak ON rak.id_rak = stokbarang.id_rak LEFT JOIN sumberdana On sumberdana.idsumberdana = masterbarang.idsumberdana LEFT JOIN kategoribarang ON kategoribarang.id_kategori=masterbarang.id_kategori LEFT JOIN satuanbarang ON satuanbarang.id_satuan=masterbarang.id_satuan")
    data = cur.fetchall()
    cur.close()
    return render_template('halamankepalagudang/masterbarang.html', permintaans=data, kategoribarang=kategoribarang, rak=rak, satuanbarang=satuanbarang, supplier=supplier, sumberdana=sumberdana)

@app.route('/kepgud/daftarbarang/edit/<string:id>', methods=['GET', 'POST'])
def editmasterbarang(id):
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('select * from satuanbarang')
        satuanbarang = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from supplier')
        supplier = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from sumberdana')
        sumberdana = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from rak')
        rak = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM kategoribarang')
        kategoribarang = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM masterbarang INNER JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` INNER JOIN kategoribarang ON kategoribarang.id_kategori = masterbarang.id_kategori INNER JOIN satuanbarang ON satuanbarang.id_satuan = masterbarang.id_satuan INNER JOIN sumberdana ON sumberdana.idsumberdana = masterbarang.idsumberdana WHERE masterbarang.id_stok=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalagudang/editmasterbarang.html', row=row, satuanbarang=satuanbarang, rak=rak, supplier=supplier,sumberdana=sumberdana,kategoribarang=kategoribarang)
    else:
        id_kategori = request.form['id_kategori']
        id_satuan = request.form['id_satuan']
        namabarang = request.form['namabarang']
        merk = request.form['merk']
        idsumberdana = request.form['idsumberdana']

        stok = request.form['stok']

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        UPDATE masterbarang 
        SET 
            id_kategori = %s,
            id_satuan = %s,
            namabarang = %s,
            merk = %s,
            idsumberdana = %s
        WHERE
            id_stok = %s;
        ''',(id_kategori,id_satuan,namabarang,merk,idsumberdana,id))

        cursor.execute(''' 
        UPDATE stokbarang 
        SET 
            stok = %s
        WHERE
            id_stok = %s;
        ''',([stok],id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('daftarbarang'))

@app.route('/kepgud/daftarbarang/detailbarang/<int:id>', methods=['GET'])
def detailbarang(id):
    if request.method == 'GET':
        prev_page = id - 1
        next_page = id + 1

        cursor = mysql.connection.cursor()
        cursor.execute('''
        SELECT * FROM masterbarang INNER JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` INNER JOIN kategoribarang ON kategoribarang.id_kategori = masterbarang.id_kategori INNER JOIN satuanbarang ON satuanbarang.id_satuan = masterbarang.id_satuan INNER JOIN sumberdana ON sumberdana.idsumberdana = masterbarang.idsumberdana INNER JOIN rak ON rak.id_rak = stokbarang.id_rak WHERE id_barang=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalagudang/detailbarang.html', prev_page=prev_page,next_page=next_page,row=row)

@app.route('/kepgud/daftarbarang/hapusbarang/<string:id>', methods=['GET'])
def hapusbarang(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM masterbarang WHERE id_stok=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM stokbarang WHERE id_stok=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('daftarbarang'))

    return render_template('halamankepalagudang/daftarbarang.html')

@app.route('/kepgud/daftarbarang/tambahbarang', methods=['GET', 'POST'])
def tambahbarang():
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM kategoribarang')
        kategoribarang = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from satuanbarang')
        satuanbarang = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from supplier')
        supplier = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from sumberdana')
        sumberdana = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from rak')
        rak = cursor.fetchall()
        cursor.close()

        return render_template('halamankepalagudang/tambahbarang.html', kategoribarang=kategoribarang, sumberdana=sumberdana, satuanbarang=satuanbarang, rak=rak, supplier=supplier)
    else:
        stok = request.form['stok']
        jml_barang_msk = request.form['jml_barang_msk']
        hrg_satuan = request.form['hrg_satuan']
        total = request.form['total']
        id_supplier = request.form['id_supplier']
        id_rak = request.form['id_rak']

        id_stok = request.form['id_stok']
        id_kategori = request.form['id_kategori']
        id_satuan = request.form['id_satuan']
        namabarang = request.form['namabarang']
        merk = request.form['merk']
        idsumberdana = request.form['idsumberdana']
        cursor = mysql.connection.cursor()
        files = request.files.getlist('files[]')
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute('INSERT INTO stokbarang(id_stok,stok,jml_barang_msk,tgl_masuk,hrg_satuan,total,id_supplier,id_rak) VALUES(%s,%s,%s,NOW(),%s,%s,%s,%s)',(id_stok, stok, jml_barang_msk, hrg_satuan, total, id_supplier, id_rak))
                cursor.execute('INSERT INTO masterbarang(id_stok, id_kategori, id_satuan, namabarang, merk, idsumberdana,files) VALUES(%s,%s,%s,%s,%s,%s,%s)',( id_stok, id_kategori, id_satuan, namabarang, merk , idsumberdana,[filename]))
                mysql.connection.commit()
            print(file)
        cursor.close()   
        flash('File(s) successfully uploaded')    
        return redirect(url_for('daftarbarang'))

@app.route('/kepgud/listpermintaan/barangsiap/<string:id>', methods=['GET','POST'])
def barangsiap(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        UPDATE permintaan SET idstatuspesanan = '2' WHERE id_permintaan=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('listpermintaankepgud'))

    return render_template('halamankepalagudang/permintaan.html')

@app.route('/kepgud/barangkeluar')
def barangkeluar():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from masterbarang')
    daftarbarang = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute('select * from pegawai')
    daftarpegawai = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute('select * from jabatan')
    daftarjabatan = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM barangkeluar LEFT JOIN masterbarang ON masterbarang.`id_barang`= barangkeluar.`id_barang` LEFT JOIN pegawai ON pegawai.`id_user`=barangkeluar.`id_user` LEFT JOIN jabatan ON jabatan.`kode_jabatan`=pegawai.`kode_jabatan` GROUP BY barangkeluar.id_permintaan')
    databarangkeluar = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalagudang/barangkeluar.html', databarangkeluar=databarangkeluar, daftarbarang=daftarbarang,daftarpegawai=daftarpegawai,daftarjabatan=daftarjabatan)

@app.route('/kepgud/barangkeluar/download/report/excel', methods=['GET','POST'])
def laporan_barangkeluar():

  tgl_keluar = request.form['tgl_keluar']

  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
       
  cursor.execute("SELECT * FROM barangkeluar LEFT JOIN masterbarang ON masterbarang.`id_barang`= barangkeluar.`id_barang` LEFT JOIN pegawai ON pegawai.`id_user`=barangkeluar.`id_user` LEFT JOIN jabatan ON jabatan.`kode_jabatan`=pegawai.`kode_jabatan` WHERE DATE_FORMAT(tgl_keluar, '%%Y-%%m') = %s GROUP BY barangkeluar.id_permintaan ",[tgl_keluar])
  mysql.connection.commit()
  result = cursor.fetchall()
   
  #output in bytes
  output = io.BytesIO()
  #create WorkBook object
  workbook = xlwt.Workbook()
  #add a sheet
  sh = workbook.add_sheet('Daftar Barang Keluar')
   
  #add headers
  sh.write(0, 0, 'Kode Stok')
  sh.write(0, 1, 'Nama Barang')
  sh.write(0, 2, 'Nama Penerima')
  sh.write(0, 3, 'Jabatan Penerima')
  sh.write(0, 4, 'Jumlah  Keluar')
  sh.write(0, 5, 'Tanggal Keluar')
   
  idx = 0
  for row in result:
   sh.write(idx+1, 0, str(row['id_stok']))
   sh.write(idx+1, 1, row['namabarang'])
   sh.write(idx+1, 2, row['nama'])
   sh.write(idx+1, 3, row['nama_jabatan'])
   sh.write(idx+1, 4, row['jumlah'])
   sh.write(idx+1, 5,row['tgl_keluar'],style1)
   idx += 1
   
  workbook.save(output)
  output.seek(0)
   
  return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=barang_keluar.xls"})


@app.route('/kepgud/barangkeluar/tambahbarangkeluar', methods=['GET', 'POST'])
def tambahbarangkeluar():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('select * from masterbarang')
        daftarbarang = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from pegawai')
        daftarpegawai = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from jabatan')
        daftarjabatan = cursor.fetchall()
        cursor.close()

        return render_template('halamankepalagudang/barangkeluar.html', daftarbarang=daftarbarang, daftarpegawai=daftarpegawai,daftarjabatan=daftarjabatan)
    else:

        id_barangkeluar = request.form['id_barangkeluar']
        id_barang = request.form['id_barang']
        id_user = request.form['id_user']
        kode_jabatan = request.form['kode_jabatan']
        jumlah = request.form['jumlah']

        cursor = mysql.connection.cursor()
        cursor.execute(
            '''INSERT INTO barangkeluar(id_barangkeluar,id_barang, id_user, kode_jabatan, jumlah) VALUES(%s,%s,%s,%s,%s)''',
            (id_barangkeluar, id_barang, id_user, kode_jabatan, jumlah))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('barangkeluar'))

@app.route('/kepgud/barangkeluar/hapusbarangkeluar/<int:id>', methods=['GET'])
def hapusbarangkeluar(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        DELETE FROM barangkeluar WHERE id=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('barangkeluar'))

    return render_template('halamankepalagudang/barangkeluar.html')

@app.route('/kepgud/datasupplier')
def datasupplier():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM supplier')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalagudang/supplier.html', datasupplier=row)

@app.route('/kepgud/datasupplier/tambahsupplier', methods=['GET', 'POST'])
def tambahsupplier():
    if request.method == 'GET':
        return render_template('halamankepalagudang/tambahsupplier.html')
    else:
        namasupplier = request.form['namasupplier']
        nomortelepon = request.form['nomortelepon']
        email = request.form['email']
        alamat = request.form['alamat']
      
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO supplier(namasupplier, nomortelepon, email, alamat) VALUES(%s,%s,%s,%s)''',(namasupplier,nomortelepon,email,alamat))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('datasupplier'))

@app.route('/kepgud/datasupplier/editsupplier/<string:id>', methods=['GET', 'POST'])
def editsupplier(id):
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
        SELECT * 
        FROM supplier 
        WHERE id_supplier=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalagudang/editsupplier.html', row=row)
    else:
        namasupplier = request.form['namasupplier']
        nomortelepon = request.form['nomortelepon']
        email = request.form['email']
        alamat = request.form['alamat']

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        UPDATE supplier 
        SET 
            namasupplier = %s,
            nomortelepon = %s,
            email = %s,
            alamat = %s
        WHERE
            id_supplier = %s;
        ''',(namasupplier, nomortelepon, email, alamat,id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('datasupplier'))

@app.route('/kepgud/datasupplier/hapussupplier/<string:id>', methods=['GET'])
def hapussupplier(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        DELETE FROM supplier WHERE id_supplier=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('datasupplier'))

    return render_template('halamankepalagudang/supplier.html')


@app.route('/kepgud/sumberdana')
def sumberdana():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM sumberdana')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalagudang/sumberdana.html', sumberdana=row)

@app.route('/kepgud/sumberdana/tambahsumberdana', methods=['GET', 'POST'])
def tambahsumberdana():
    if request.method == 'GET':
        return render_template('halamankepalagudang/tambahsumberdana.html')
    else:
        namasumberdana = request.form['namasumberdana']
      
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO sumberdana(namasumberdana) VALUES(%s)''',[namasumberdana])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('sumberdana'))

@app.route('/kepgud/sumberdana/editsumberdana/<string:id>', methods=['GET', 'POST'])
def editsumberdana(id):
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
        SELECT * 
        FROM sumberdana 
        WHERE idsumberdana=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalagudang/editsumberdana.html', row=row)
    else:
        namasumberdana = request.form['namasumberdana']

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        UPDATE sumberdana 
        SET 
            namasumberdana = %s
        WHERE
            idsumberdana = %s;
        ''',(namasumberdana,id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('sumberdana'))

@app.route('/kepgud/sumberdana/hapussumberdana/<string:id>', methods=['GET'])
def hapussumberdana(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        DELETE FROM sumberdana WHERE idsumberdana=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('sumberdana'))

    return render_template('halamankepalagudang/sumberdana.html')

@app.route('/kepgud/rakbarang')
def rakbarang():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM rak')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalagudang/rak.html', rakbarang=row)

@app.route('/kepgud/rakbarang/tambahrakbarang', methods=['GET', 'POST'])
def tambahrakbarang():
    if request.method == 'GET':
        return render_template('halamankepalagudang/tambahrakbarang.html')
    else:
        nama_rak = request.form['nama_rak']
        kapasitas_rak = request.form['kapasitas_rak']
      
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO rak(nama_rak,kapasitas_rak) VALUES(%s,%s)''',(nama_rak,kapasitas_rak))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('rakbarang'))

@app.route('/kepgud/rakbarang/editrak/<string:id>', methods=['GET', 'POST'])
def editrak(id):
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
        SELECT * 
        FROM rak 
        WHERE id_rak=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalagudang/editrak.html', row=row)
    else:
        nama_rak = request.form['nama_rak']
        kapasitas_rak = request.form['kapasitas_rak']

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        UPDATE rak 
        SET 
            nama_rak = %s,
            kapasitas_rak = %s
        WHERE
            id_rak = %s;
        ''',(nama_rak, kapasitas_rak,id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('rakbarang'))

@app.route('/kepgud/rakbarang/hapusrak/<string:id>', methods=['GET'])
def hapusrak(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        DELETE FROM rak WHERE id_rak=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('rakbarang'))

    return render_template('halamankepalagudang/rak.html')

@app.route('/kepgud/kategoribarang', defaults={'page':0})
@app.route('/kepgud/kategoribarang/<int:page>')
def kategoribarang(page):
    prev_page = page - 1
    next_page = page + 1
    perpage = 5
    first_page = page*perpage
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) AS totalkategori FROM kategoribarang")
    totalkategori = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM kategoribarang limit "+str(first_page)+", "+str(perpage)+";", 
    mysql.connection.commit())
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalagudang/kategoribarang.html',totalkategori=totalkategori, kategoribarang=row,next_page=next_page, prev_page=prev_page)

@app.route('/kepgud/kategoribarang/tambahkategoribarang', methods=['POST'])
def tambahkategoribarang():
    namakategori = request.form['namakategori']
      
    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO kategoribarang(namakategori) VALUES(%s)''',[namakategori])
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('kategoribarang'))

@app.route('/kepgud/kategoribarang/editkategori/<string:id>', methods=['GET', 'POST'])
def editkategori(id):
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM kategoribarang WHERE id_kategori=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalagudang/editkategoribarang.html', row=row)
    else:
        namakategori = request.form['namakategori']

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        UPDATE kategoribarang 
        SET 
            namakategori = %s
        WHERE
            id_kategori = %s;
        ''',(namakategori,id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('kategoribarang'))

@app.route('/kepgud/kategoribarang/hapuskategori/<int:id>', methods=['GET'])
def hapuskategori(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        DELETE FROM kategoribarang WHERE id_kategori=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('kategoribarang'))

    return render_template('halamankepalagudang/kategoribarang.html')



@app.route('/kepgud/satuanbarang', defaults={'page':0})
@app.route('/kepgud/satuanbarang/<int:page>')
def satuanbarang(page):
    prev_page = page - 1
    next_page = page + 1
    perpage = 5
    first_page = page*perpage
    cur = mysql.connection.cursor()
    cur.execute("select * from satuanbarang limit "+str(first_page)+", "+str(perpage)+";", mysql.connection.commit())
    data = cur.fetchall()
    return render_template('halamankepalagudang/satuanbarang.html', data=data, next_page=next_page, prev_page=prev_page)

@app.route('/kepgud/satuanbarang/tambahsatuanbarang', methods=['GET', 'POST'])
def tambahsatuanbarang():
    if request.method == 'GET':
        return render_template('halamankepalagudang/tambahsatuanbarang.html')
    else:
        nama_satuan = request.form['nama_satuan']
      
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO satuanbarang(nama_satuan) VALUES(%s)''',[nama_satuan])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('satuanbarang'))

@app.route('/kepgud/satuanbarang/editsatuan/<string:id>', methods=['GET', 'POST'])
def editsatuan(id):
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
        SELECT * 
        FROM satuanbarang 
        WHERE id_satuan=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalagudang/editsatuan.html', row=row)
    else:
        nama_satuan = request.form['nama_satuan']

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        UPDATE satuanbarang 
        SET 
            nama_satuan = %s
        WHERE
            id_satuan = %s;
        ''',(nama_satuan,id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('satuanbarang'))

@app.route('/kepgud/satuanbarang/hapussatuan/<string:id>', methods=['GET'])
def hapussatuan(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        DELETE 
        FROM satuanbarang 
        WHERE id_satuan=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('satuanbarang'))

    return render_template('halamankepalagudang/satuanbarang.html')

@app.route('/kepgud/stokbarang')
def stokbarang():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM stokbarang LEFT JOIN masterbarang ON masterbarang.id_stok = stokbarang.id_stok')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalagudang/stokbarang.html', stokbarang=row)

@app.route('/kepgud/unitkerja')
def unitkerja():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM unitkerja')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalagudang/unitkerja.html', unitkerja=row)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/kepgud/unitkerja/tambahunitkerja', methods=['GET', 'POST'])
def tambahunitkerja():
    if request.method == 'GET':
        return render_template('halamankepalagudang/tambahstatus.html')
    else:
        namaunitkerja = request.form['namaunitkerja']
        alamat = request.form['alamat']
        no_telp = request.form['no_telp']
        no_fax = request.form['no_fax']
        email = request.form['email']
        web = request.form['web']
        cabang = request.form['cabang']
      
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO unitkerja( namaunitkerja, alamat, no_telp, no_fax, email, web, cabang) VALUES(%s,%s,%s,%s,%s,%s,%s)''',( namaunitkerja, alamat, no_telp, no_fax, email, web, cabang))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('unitkerja'))

@app.route('/kepgud/unitkerja/hapusunitkerja/<string:id>', methods=['GET'])
def hapusunitkerja(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM unitkerja WHERE id_unitkerja=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('unitkerja'))

    return render_template('halamankepalagudang/unitkerja.html')

@app.route('/kepgud/unitkerja/editunitkerja/<int:id>', methods=['GET', 'POST'])
def editunitkerja(id):
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
        SELECT * 
        FROM unitkerja 
        WHERE id_unitkerja=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalagudang/editunitkerja.html', row=row)
    else:
        namaunitkerja = request.form['namaunitkerja']
        alamat = request.form['alamat']
        no_telp = request.form['no_telp']
        no_fax = request.form['no_fax']
        email = request.form['email']
        web = request.form['web']
        cabang = request.form['cabang']

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        UPDATE unitkerja 
        SET 
            namaunitkerja = %s,
            alamat = %s,
            no_telp = %s,
            no_fax = %s,
            email = %s,
            web = %s,
            cabang = %s
            
        WHERE
            id_unitkerja = %s;
        ''',(namaunitkerja, alamat, no_telp, no_fax, email, web, cabang,id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('unitkerja'))


@app.route('/kepgud/daftarstatus')
def daftarstatus():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM status')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalagudang/daftarstatus.html', daftarstatus=row)

@app.route('/kepgud/daftarstatus/tambahstatus', methods=['GET', 'POST'])
def tambahstatus():
    if request.method == 'GET':
        return render_template('halamankepalagudang/tambahstatus.html')
    else:
        id_status = request.form['id_status']
        nama_status = request.form['nama_status']
      
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO status(id_status,nama_status) VALUES(%s,%s)''',(id_status,nama_status))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('daftarstatus'))

@app.route('/kepgud/daftarstatus/editstatus/<string:id>', methods=['GET', 'POST'])
def editstatus(id):
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
        SELECT * 
        FROM status 
        WHERE id_status=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalagudang/editstatus.html', row=row)
    else:
        nama_status = request.form['nama_status']

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        UPDATE status 
        SET 
            nama_status = %s
        WHERE
            id_status = %s;
        ''',(nama_status,id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('daftarstatus'))

@app.route('/kepgud/daftarstatus/hapusstatus/<string:id>', methods=['GET'])
def hapusstatus(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        DELETE 
        FROM status WHERE id_status=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('daftarstatus'))

    return render_template('halamankepalagudang/daftarstatus.html')

@app.route('/kepgud/daftarjabatan')
def daftarjabatan():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM jabatan')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalagudang/daftarjabatan.html', daftarjabatan=row)

@app.route('/kepgud/daftarjabatan/tambahjabatan', methods=['GET', 'POST'])
def tambahjabatan():
    if request.method == 'GET':
        return render_template('halamankepalagudang/tambahjabatan.html')
    else:
        nama_jabatan = request.form['nama_jabatan']
      
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO jabatan(nama_jabatan) VALUES(%s)''',[nama_jabatan])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('daftarjabatan'))

@app.route('/kepgud/daftarjabatan/editjabatan/<string:id>', methods=['GET', 'POST'])
def editjabatan(id):
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
        SELECT * 
        FROM jabatan 
        WHERE kode_jabatan=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()

        return render_template('halamankepalagudang/editjabatan.html', row=row)
    else:
        nama_jabatan = request.form['nama_jabatan']

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        UPDATE jabatan 
        SET 
            nama_jabatan = %s
        WHERE
            kode_jabatan = %s;
        ''',(nama_jabatan,id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('daftarjabatan'))

@app.route('/kepgud/daftarjabatan/hapusjabatan/<string:id>', methods=['GET'])
def hapusjabatan(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
        DELETE 
        FROM jabatan WHERE kode_jabatan=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('daftarjabatan'))

    return render_template('halamankepalagudang/daftarjabatan.html')

@app.route('/kepgud/grafik')
def grafik():
    return render_template('halamankepalagudang/grafik.html')

# Batas halaman kepala gudang #
@app.route('/pegawai/homepegawai', defaults={'page':0})
@app.route('/pegawai/homepegawai/<int:page>')
def homepegawai(page):
    if 'loggedin' in session:

        prev_page = page - 1
        next_page = page + 1
        perpage = 6
        first_page = page*perpage
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) AS totalbarang FROM masterbarang")
        totalbarang = cursor.fetchall()

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM masterbarang LEFT JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` LEFT JOIN satuanbarang ON satuanbarang.`id_satuan` = masterbarang.`id_satuan` LEFT JOIN sumberdana ON sumberdana.idsumberdana = masterbarang.idsumberdana LEFT JOIN kategoribarang ON kategoribarang.`id_kategori`=masterbarang.`id_kategori` LIMIT "+str(first_page)+", "+str(perpage)+";", 
        mysql.connection.commit())
        row = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pegawai INNER JOIN jabatan on jabatan.kode_jabatan = pegawai.kode_jabatan LEFT JOIN permintaan ON permintaan.id_user = pegawai.id_user WHERE pegawai.id_user = %s', (session['id_user'],))
        account = cursor.fetchone()
        return render_template('halamanpegawai/homepegawai.html', account=account, totalbarang=totalbarang, daftarbarang=row,next_page=next_page, prev_page=prev_page)
        
    return redirect(url_for('login'))



@app.route('/pegawai/logout')
def logoutpegawai():
   session.pop('loggedin', None)
   session.pop('id_user', None)
   session.pop('email', None)
   session.pop('kode_jabatan', None)
   return redirect(url_for('login'))

@app.route('/pegawai/homepegawai/profile')
def profilpegawai():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pegawai LEFT JOIN jabatan ON jabatan.kode_jabatan = pegawai.kode_jabatan LEFT JOIN status ON status.`id_status` = pegawai.`id_status` WHERE id_user = %s', (session['id_user'],))
        account = cursor.fetchone()
        return render_template('halamanpegawai/profilpegawai.html', account=account)
    return redirect(url_for('login'))


@app.route('/pegawai/homepegawai/profile/gantipassword/<int:id>', methods=['GET', 'POST'])
def gantipassword(id):
    if request.method == 'GET':

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM pegawai WHERE id_user=%s''', (session['id_user'],))
        account = cursor.fetchone()
        cursor.close()

        return render_template('halamanpegawai/gantipassword.html', account=account)
    else:
        nip = request.form['nip']

        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE pegawai SET nip = %s WHERE id_user = %s;''', (nip, id))

        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('profilpegawai'))


@app.route('/pegawai/homepegawai/listpermintaan')
def listpesanan():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM permintaan INNER JOIN masterbarang on masterbarang.id_barang = permintaan.id_barang INNER JOIN jabatan on jabatan.kode_jabatan = permintaan.kode_jabatan INNER JOIN pegawai on pegawai.id_user = permintaan.id_user INNER JOIN statuspesanan ON statuspesanan.idstatuspesanan = permintaan.idstatuspesanan WHERE permintaan.id_user = %s", (session['id_user'],))
        account = cur.fetchall()
        cur.close()
        return render_template('halamanpegawai/permintaan.html', account=account)
    return redirect(url_for('login'))

@app.route('/pegawai/homepegawai/notifikasipegawai')
def notifikasipegawai():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM permintaan INNER JOIN masterbarang on masterbarang.id_barang = permintaan.id_barang INNER JOIN jabatan on jabatan.kode_jabatan = permintaan.kode_jabatan INNER JOIN pegawai on pegawai.id_user = permintaan.id_user INNER JOIN statuspesanan ON statuspesanan.idstatuspesanan = permintaan.idstatuspesanan WHERE permintaan.id_user = %s AND permintaan.idstatuspesanan = 2", (session['id_user'],))
        permintaansiap = cur.fetchall()
        cur.close()
    return render_template('halamanpegawai/notifikasipegawai.html', permintaansiap=permintaansiap)

@app.route('/pegawai/homepegawai/listpermintaan/konfirmasipesanan/<int:id>', methods=['GET','POST'])
def konfirmasipesanan(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE permintaan SET idstatuspesanan = '3' WHERE id_permintaan=%s''', (id, ))
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE barangkeluar SET tgl_keluar = NOW() WHERE id_permintaan=%s''', (id, ))
        mysql.connection.commit()
        
        cursor.close()

        return redirect(url_for('listpesanan'))

    return render_template('halamankepalagudang/permintaan.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM jabatan')
        row = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM unitkerja')
        unitkerja = cursor.fetchall()
        cursor.close()

        return render_template('register.html', row=row,unitkerja=unitkerja, msg=msg)
    else:
        kode_jabatan = request.form['kode_jabatan']
        nama = request.form['nama']
        nip = request.form['nip']
        email = request.form['email']
        nomor_tlp = request.form['nomor_tlp']
        id_unitkerja=request.form['id_unitkerja']
        tingkat = request.form['tingkat']

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO pegawai(kode_jabatan, nama, nip, email, id_status, nomor_tlp,id_unitkerja,tingkat) VALUES(%s,%s,%s,%s,'S1',%s,%s,%s)''',( kode_jabatan, nama, nip, email, nomor_tlp,id_unitkerja,tingkat))
        mysql.connection.commit()
        msg = 'You have successfully registered!'
        cursor.close()
        return redirect(url_for('login'))

@app.route('/pegawai/homepegawai/buatpermintaan')
def buatpermintaan():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM masterbarang LEFT JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` LEFT JOIN satuanbarang ON satuanbarang.`id_satuan` = masterbarang.`id_satuan` LEFT JOIN sumberdana ON sumberdana.idsumberdana = masterbarang.idsumberdana LEFT JOIN kategoribarang ON kategoribarang.`id_kategori`=masterbarang.`id_kategori`')
    data = cur.fetchall()
    cur.close()
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) AS jumlahbarang FROM masterbarang')
    jumlahdata = cur.fetchall()
    cur.close()
    return render_template('halamanpegawai/buatpermintaan.html',jumlahdata=jumlahdata, daftarbarang=data)

@app.route('/pegawai/homepegawai/semuabarang')
def semuabarang():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM masterbarang LEFT JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` LEFT JOIN satuanbarang ON satuanbarang.`id_satuan` = masterbarang.`id_satuan` LEFT JOIN sumberdana ON sumberdana.idsumberdana = masterbarang.idsumberdana LEFT JOIN kategoribarang ON kategoribarang.`id_kategori`=masterbarang.`id_kategori`')
    data = cur.fetchall()
    cur.close()
    return render_template('halamanpegawai/semuabarang.html', daftarbarang=data)

@app.route('/pegawai/homepegawai/buatpermintaan/orderbarang/<int:id>', methods=['GET', 'POST'])
def orderbarang(id):
    if request.method=='GET':

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pegawai INNER JOIN jabatan on jabatan.kode_jabatan = pegawai.kode_jabatan LEFT JOIN permintaan ON permintaan.id_user = pegawai.id_user WHERE pegawai.id_user = %s', (session['id_user'],))
        account = cursor.fetchone()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute (''' SELECT * FROM masterbarang LEFT JOIN permintaan ON permintaan.`id_barang`= masterbarang.`id_barang` LEFT JOIN pegawai ON pegawai.`id_user`=permintaan.`id_user` LEFT JOIN jabatan ON jabatan.kode_jabatan = pegawai.kode_jabatan LEFT JOIN stokbarang ON stokbarang.id_stok = masterbarang.id_stok WHERE masterbarang.id_barang=%s''', (id, ))
        row = cursor.fetchone()
        cursor.close()
        return render_template('halamanpegawai/orderbarang.html', row=row,account=account)

    elif 'loggedin' in session:
        id_unitkerja = request.form['id_unitkerja']
        id_user = request.form['id_user']
        kode_jabatan = request.form['kode_jabatan']
        id_barang = request.form['id_barang']
        jumlahpesan = request.form['jumlahpesan']
        id_stok = request.form['id_stok']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''INSERT INTO permintaan(id_unitkerja, id_user, kode_jabatan, id_barang, jumlahpesan, tanggalpesan, idstatuspesanan,id_stok) VALUES ( %s, %s, %s, %s, %s, NOW(), '1', %s) ''',(id_unitkerja, id_user, kode_jabatan, id_barang, jumlahpesan,id_stok,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('listpesanan'))

@app.route('/kepgud/notifikasi')
def notifikasikepgud():
    return render_template('halamankepalagudang/notifikasi.html')

@app.route('/kepgud/formatpengadaan')
def formatpengadaan():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id_barang,namabarang, namakategori, stok,nama_satuan,merk,namasumberdana,hrg_satuan,total,tgl_masuk FROM masterbarang LEFT JOIN kategoribarang ON kategoribarang.`id_kategori`=masterbarang.`id_kategori` LEFT JOIN stokbarang ON stokbarang.`id_stok`=masterbarang.`id_stok` LEFT JOIN satuanbarang ON satuanbarang.`id_satuan`=masterbarang.`id_satuan` LEFT JOIN sumberdana ON sumberdana.`idsumberdana`=masterbarang.`idsumberdana`")
    data = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalagudang/formatpengadaan.html', data=data)

@app.route('/kepgud/formatpendanaan')
def formatpendanaan():
    return render_template('halamankepalagudang/formatpendanaan.html')

@app.route('/kepsek/unitkerjakepsek')
def unitkerjakepsek():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM unitkerja')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalasekolah/unitkerja.html',unitkerja=row)

@app.route('/kepsek/sumberdana')
def sumberdanakepsek():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM sumberdana')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalasekolah/sumberdana.html', sumberdana=row)

@app.route('/kepgud/datasupplierkepsek')
def datasupplierkepsek():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM supplier')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalasekolah/supplier.html', datasupplier=row)

@app.route('/kepsek/satuan', defaults={'page':0})
@app.route('/kepsek/satuan/<int:page>')
def satuan(page):
    prev_page = page - 1
    next_page = page + 1
    perpage = 5
    first_page = page*perpage
    cur = mysql.connection.cursor()
    cur.execute("select * from satuanbarang limit "+str(first_page)+", "+str(perpage)+";", mysql.connection.commit())
    data = cur.fetchall()
    return render_template('halamankepalasekolah/satuan.html', data=data, next_page=next_page, prev_page=prev_page)

@app.route('/kepgud/kategori')
def kategori():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM kategoribarang')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalasekolah/kategori.html', kategoribarang=row)

@app.route('/kepsek/jabatan')
def jabatan():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM jabatan')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalasekolah/jabatan.html', daftarjabatan=row)

@app.route('/kepsek/status')
def status():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM status')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalasekolah/status.html', daftarstatus=row)

@app.route('/kepsek/rak')
def rak():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM rak')
    row = cursor.fetchall()
    cursor.close()

    return render_template('halamankepalasekolah/inforak.html', rakbarang=row)

@app.route('/pegawai/order')
def order():
    return render_template('halamanpegawai/order.html')


@app.route("/kepgud/tambahbarangkepgud")
def tambahbarangkepgud():
    if request.method == 'GET':
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM kategoribarang')
        kategoribarang = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from satuanbarang')
        satuanbarang = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from supplier')
        supplier = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from sumberdana')
        sumberdana = cursor.fetchall()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('select * from rak')
        rak = cursor.fetchall()
        cursor.close()

        return render_template('halamankepalagudang/masterbarang.html', kategoribarang=kategoribarang, sumberdana=sumberdana, satuanbarang=satuanbarang, rak=rak, supplier=supplier)
    else:
        stok = request.form['stok']
        jml_barang_msk = request.form['jml_barang_msk']
        hrg_satuan = request.form['hrg_satuan']
        total = request.form['total']
        id_supplier = request.form['id_supplier']
        id_rak = request.form['id_rak']

        id_stok = request.form['id_stok']
        id_kategori = request.form['id_kategori']
        id_satuan = request.form['id_satuan']
        namabarang = request.form['namabarang']
        merk = request.form['merk']
        idsumberdana = request.form['idsumberdana']
        cursor = mysql.connection.cursor()
        files = request.files.getlist('files[]')
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute('INSERT INTO stokbarang(id_stok,stok,jml_barang_msk,tgl_masuk,hrg_satuan,total,id_supplier,id_rak) VALUES(%s,%s,%s,NOW(),%s,%s,%s,%s)',(id_stok, stok, jml_barang_msk, hrg_satuan, total, id_supplier, id_rak))
                cursor.execute('INSERT INTO masterbarang(id_stok, id_kategori, id_satuan, namabarang, merk, idsumberdana,files) VALUES(%s,%s,%s,%s,%s,%s,%s)',( id_stok, id_kategori, id_satuan, namabarang, merk , idsumberdana,[filename]))
                mysql.connection.commit()
            print(file)
        cursor.close()   
        flash('File(s) successfully uploaded')    
        return redirect(url_for('daftarbarang'))

@app.route("/ajaxlivesearch",methods=["POST","GET"])
def ajaxlivesearch():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        search_word = request.form['query']
        print(search_word)
        if search_word == '':
            query = "SELECT * FROM masterbarang ORDER BY id_barang"
            cur.execute(query)
            employee = cur.fetchall()
        else:    
            query = "SELECT * FROM masterbarang LEFT JOIN stokbarang ON stokbarang.`id_stok` = masterbarang.`id_stok` LEFT JOIN satuanbarang ON satuanbarang.`id_satuan` = masterbarang.`id_satuan` LEFT JOIN sumberdana ON sumberdana.idsumberdana = masterbarang.idsumberdana LEFT JOIN kategoribarang ON kategoribarang.`id_kategori`=masterbarang.`id_kategori` WHERE namabarang LIKE '%{}%' OR merk LIKE '%{}%' OR namakategori LIKE '%{}%' ORDER BY id_barang DESC LIMIT 20".format(search_word,search_word,search_word)
            cur.execute(query)
            numrows = int(cur.rowcount)
            employee = cur.fetchall()
            print(numrows)
    return jsonify({'htmlresponse': render_template('halamanpegawai/caribarang.html', employee=employee, numrows=numrows)})


if __name__ == '__main__':
    app.run(debug=True)