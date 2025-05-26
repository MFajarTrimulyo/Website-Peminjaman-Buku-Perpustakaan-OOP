from datetime import date, datetime
import secrets
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash

import sistem0
from sistem0 import  conn, cursor
from sistem0 import  Anggota, Dosen, Mahasiswa
from sistem0 import  Buku, Jenis_Buku, Penulis, Penerbit, Sumber
from sistem0 import  Peminjaman, DetailPeminjaman

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/")
def dashboard():
    object_anggota = Anggota("","","","")
    count_anggota = object_anggota.count_anggota(cursor, conn)
    
    object_buku = Buku("","","","","")
    count_buku = object_buku.count_buku(cursor, conn)
    
    object_peminjaman = Peminjaman("","","","","")
    count_peminjaman = object_peminjaman.count_peminjaman(cursor, conn)
    count_terlambat = object_peminjaman.count_terlambat(cursor, conn)
    return render_template('dashboard.html', 
            request=request, 
            count_anggota=count_anggota, count_buku=count_buku, 
            count_peminjaman=count_peminjaman, count_terlambat=count_terlambat)



# Buku Route
@app.route("/buku/index")
def buku_index():
    # Object Buku
    object_buku = Buku("","","","","")
    buku = object_buku.read_from_db(cursor)
    return render_template('buku/index.html', buku=buku)

@app.route("/buku/tambah")
def buku_create():
    # Object Jenis Buku
    object_jenisBuku = Jenis_Buku("")
    jenis_buku = object_jenisBuku.read_from_db(cursor)
    # Object Penerbit
    object_penerbit = Penerbit("")
    penerbit = object_penerbit.read_from_db(cursor)
    # Object Penulis
    object_penulis = Penulis("")
    penulis = object_penulis.read_from_db(cursor)
    # Object Sumber
    object_sumber = Sumber("")
    sumber = object_sumber.read_from_db(cursor)
    return render_template('buku/create.html', jenis_buku=jenis_buku, penerbit=penerbit, penulis=penulis, sumber=sumber)

@app.route("/buku/insert", methods=['POST'])
def buku_insert():
    if request.method == 'POST':
        nama_buku = request.form['nama_buku']
        jenis_buku = request.form['jenis_buku']
        penulis_buku = request.form['penulis_buku']
        penerbit_buku = request.form['penerbit_buku']
        sumber_buku = request.form['sumber_buku']

        # Validation
        if not all([nama_buku, jenis_buku, penulis_buku, penerbit_buku, sumber_buku]):
            flash("Form masih kosong!", "error")
            return redirect(url_for('buku_create'))
        
        cursor.execute("SELECT * FROM buku WHERE nama_buku = %s", (nama_buku,))
        buku = cursor.fetchone()

        # Pengecekan Data Buku
        if buku:
            flash("Buku sudah ada!", "error")
            return redirect(url_for('buku_create'))
        
        # Object Buku
        object_buku = Buku(nama_buku, jenis_buku, penulis_buku, penerbit_buku, sumber_buku)
        object_buku.insert_to_db(cursor, conn)
        flash("Buku berhasil ditambahkan!", "success")

    return redirect(url_for('buku_index'))

@app.route("/buku/edit/<id>", methods=['GET'])
def buku_edit(id):
    cursor.execute("SELECT * FROM buku WHERE id_buku = %s", (id,))
    buku = cursor.fetchone()
    
    if buku:
        # Object Jenis Buku
        object_jenisBuku = Jenis_Buku("")
        jenis_buku = object_jenisBuku.read_from_db(cursor)
        # Object Penerbit
        object_penerbit = Penerbit("")
        penerbit = object_penerbit.read_from_db(cursor)
        # Object Penulis
        object_penulis = Penulis("")
        penulis = object_penulis.read_from_db(cursor)
        # Object Sumber
        object_sumber = Sumber("")
        sumber = object_sumber.read_from_db(cursor)
        return render_template('buku/edit.html', buku=buku, jenis_buku=jenis_buku, penerbit=penerbit, penulis=penulis, sumber=sumber)
    else:
        flash("Buku tidak ditemukan!", "error")
        return redirect(url_for('buku_index'))

@app.route("/buku/update/<id>", methods=['POST'])
def buku_update(id):
    if request.method == 'POST':
        nama_buku = request.form['nama_buku']
        jenis_buku = request.form['jenis_buku']
        penulis_buku = request.form['penulis_buku']
        penerbit_buku = request.form['penerbit_buku']
        sumber_buku = request.form['sumber_buku']

        # Validation
        if not all([nama_buku, jenis_buku, penulis_buku, penerbit_buku, sumber_buku]):
            flash("Form masih kosong!", "error")
            return redirect(url_for('buku_edit', id))
        
        cursor.execute("SELECT * FROM buku WHERE id_buku = %s", (id,))
        buku = cursor.fetchone()

        if buku:
            # Object Buku
            object_buku = Buku(nama_buku, jenis_buku, penulis_buku, penerbit_buku, sumber_buku)
            object_buku.update_in_db(cursor, conn, id)
            flash("Buku berhasil diupdate!", "success")
        else:
            flash("Buku tidak ditemukan!", "error")

    return redirect(url_for('buku_index'))

@app.route("/buku/delete/<id>", methods=['POST'])
def buku_delete(id):
    try:
        cursor.execute("SELECT * FROM buku WHERE id_buku = %s", (id,))
        buku = cursor.fetchone()

        if not buku:
            flash("Buku tidak ditemukan!", "error")
            return redirect(url_for('buku_index'))

        # Cek apakah ada peminjaman aktif
        cursor.execute("SELECT COUNT(*) FROM detail_peminjaman WHERE fk_buku = %s", (id,))
        peminjaman_count = cursor.fetchone()[0]

        if peminjaman_count > 0:
            flash("Tidak bisa menghapus! Buku sedang dipinjam.", "error")
            return redirect(url_for('buku_index'))

        object_buku = Buku("", "", "", "", "")
        object_buku.delete_from_db(cursor, conn, id)
        flash("Buku berhasil dihapus!", "success")

    except mysql.connector.IntegrityError as e:
        flash("Gagal menghapus buku karena masih memiliki data terkait (integrity error).", "error")

    except mysql.connector.Error as e:
        flash(f"Terjadi kesalahan database: {e}", "error")
    
    return redirect(url_for('buku_index'))


# Jenis Buku Route
@app.route("/buku/jenis/index")
def jenis_index():
    # Object Jenis Buku
    object_jenisBuku = Jenis_Buku("")
    jenis_buku = object_jenisBuku.read_from_db(cursor)
    return render_template('buku/jenis_buku/index.html', jenis_buku=jenis_buku)

@app.route("/buku/jenis/tambah")
def jenis_create():
    return render_template('buku/jenis_buku/create.html')

@app.route("/buku/jenis/insert", methods=['POST'])
def jenis_insert():
    if request.method == 'POST':
        nama_jenis = request.form['nama_jenis']

        # Validation
        if not nama_jenis:
            flash("Form masih kosong!", "error")
            return redirect(url_for('jenis_create'))
        
        cursor.execute("SELECT * FROM jenis_buku WHERE nama_jenis = %s", (nama_jenis,))
        jenis_buku = cursor.fetchone()

        # Pengecekan Data Jenis Buku
        if jenis_buku:
            flash("Jenis Buku sudah ada!", "error")
            return redirect(url_for('jenis_create'))
        
        # Object Jenis Buku
        object_jenisBuku = Jenis_Buku(nama_jenis)
        object_jenisBuku.insert_to_db(cursor, conn)
        flash("Jenis Buku berhasil ditambahkan!", "success")

    return redirect(url_for('jenis_index'))

@app.route("/buku/jenis/edit/<id>", methods=['GET'])
def jenis_edit(id):
    cursor.execute("SELECT * FROM jenis_buku WHERE id_jbuku = %s", (id,))
    jenis_buku = cursor.fetchone()
    
    if jenis_buku:
        return render_template('buku/jenis_buku/edit.html', jenis_buku=jenis_buku)
    else:
        flash("Jenis Buku tidak ditemukan!", "error")
        return redirect(url_for('jenis_index'))

@app.route("/buku/jenis/update/<id>", methods=['POST'])
def jenis_update(id):
    if request.method == 'POST':
        nama_jenis = request.form['nama_jenis']

        if not nama_jenis:
            flash("Form masih kosong!", "error")
            return redirect(url_for('jenis_edit', id=id))
        
        cursor.execute("SELECT * FROM jenis_buku WHERE id_jbuku = %s", (id,))
        jenis_buku = cursor.fetchone()

        if jenis_buku:
            # Object Jenis Buku
            object_jenisBuku = Jenis_Buku(nama_jenis)
            object_jenisBuku.update_in_db(cursor, conn, id)
            flash("Jenis Buku berhasil diupdate!", "success")
        else:
            flash("Jenis Buku tidak ditemukan!", "error")

    return redirect(url_for('jenis_index'))

@app.route("/buku/jenis/delete/<id>", methods=['POST'])
def jenis_delete(id):
    try:
        cursor.execute("SELECT * FROM jenis_buku WHERE id_jbuku = %s", (id,))
        jenis_buku = cursor.fetchone()

        if jenis_buku:
            # Object Jenis Buku
            object_jenisBuku = Jenis_Buku("")
            object_jenisBuku.delete_from_db(cursor, conn, id)
            flash("Jenis Buku berhasil dihapus!", "success")
        else:
            flash("Jenis Buku tidak ditemukan!", "error")
    except mysql.connector.IntegrityError as e:
        flash("Gagal menghapus jenis buku karena masih memiliki data terkait (integrity error).", "error")

    except mysql.connector.Error as e:
        flash(f"Terjadi kesalahan database: {e}", "error")

    return redirect(url_for('jenis_index'))



# Penerbit Buku Route
@app.route("/buku/penerbit/index")
def penerbit_index():
    # Object Penerbit
    object_penerbit = Penerbit("")
    penerbit = object_penerbit.read_from_db(cursor)
    return render_template('buku/penerbit/index.html', penerbit=penerbit)

@app.route("/buku/penerbit/tambah")
def penerbit_create():
    return render_template('buku/penerbit/create.html')

@app.route("/buku/penerbit/insert", methods=['POST'])
def penerbit_insert():
    if request.method == 'POST':
        nama_penerbit = request.form['nama_penerbit']

        if not nama_penerbit:
            flash("Form masih kosong!", "error")
            return redirect(url_for('penerbit_create'))
        
        cursor.execute("SELECT * FROM penerbit WHERE nama_penerbit = %s", (nama_penerbit,))
        penerbit = cursor.fetchone()

        if penerbit:
            flash("Penerbit sudah ada!", "error")
            return redirect(url_for('penerbit_create'))
        else:
            # Object Penerbit
            object_penerbit = object_penerbit = Penerbit(nama_penerbit)
            object_penerbit.insert_to_db(cursor, conn)
            flash("Penerbit berhasil ditambahkan!", "success")

    return redirect(url_for('penerbit_index'))

@app.route("/buku/penerbit/edit/<id>", methods=['GET'])
def penerbit_edit(id):
    cursor.execute("SELECT * FROM penerbit WHERE id_penerbit = %s", (id,))
    penerbit = cursor.fetchone()
    
    if penerbit:
        return render_template('buku/penerbit/edit.html', penerbit=penerbit)
    else:
        flash("Penerbit tidak ditemukan!", "error")
        return redirect(url_for('penerbit_index'))

@app.route("/buku/penerbit/update/<id>", methods=['POST'])
def penerbit_update(id):
    if request.method == 'POST':
        nama_penerbit = request.form['nama_penerbit']

        if not nama_penerbit:
            flash("Form masih kosong!", "error")
            return redirect(url_for('penerbit_edit', id=id))
        
        cursor.execute("SELECT * FROM penerbit WHERE id_penerbit = %s", (id,))
        penerbit = cursor.fetchone()

        if penerbit:
            # Object Penerbit
            object_penerbit = object_penerbit = Penerbit(nama_penerbit)
            object_penerbit.update_in_db(cursor, conn, id)
            flash("Penerbit berhasil diupdate!", "success")
        else:
            flash("Penerbit tidak ditemukan!", "error")

    return redirect(url_for('penerbit_index'))

@app.route("/buku/penerbit/delete/<id>", methods=['POST'])
def penerbit_delete(id):
    try:
        cursor.execute("SELECT * FROM penerbit WHERE id_penerbit = %s", (id,))
        penerbit = cursor.fetchone()

        if penerbit:
            # Object Penerbit
            object_penerbit = object_penerbit = Penerbit("")
            object_penerbit.delete_from_db(cursor, conn, id)
            flash("Penerbit berhasil dihapus!", "success")
        else:
            flash("Penerbit tidak ditemukan!", "error")
    
    except mysql.connector.IntegrityError as e:
        flash("Gagal menghapus penerbit karena masih memiliki data terkait (integrity error).", "error")

    except mysql.connector.Error as e:
        flash(f"Terjadi kesalahan database: {e}", "error")

    return redirect(url_for('penerbit_index'))



# Penulis Buku Route
@app.route("/buku/penulis/index")
def penulis_index():
    # Object Penulis
    object_penulis = Penulis("")
    penulis = object_penulis.read_from_db(cursor)
    return render_template('buku/penulis/index.html', penulis=penulis)

@app.route("/buku/penulis/tambah")
def penulis_create():
    return render_template('buku/penulis/create.html')

@app.route("/buku/penulis/insert", methods=['POST'])
def penulis_insert():
    if request.method == 'POST':
        nama_penulis = request.form['nama_penulis']

        if not nama_penulis:
            flash("Form masih kosong!", "error")
            return redirect(url_for('penulis_create'))
        
        cursor.execute("SELECT * FROM penulis WHERE nama_penulis = %s", (nama_penulis,))
        penulis = cursor.fetchone()

        if penulis:
            flash("Penulis sudah ada!", "error")
            return redirect(url_for('penulis_create'))
        else:
            # Object Penulis
            object_penulis = Penulis(nama_penulis)
            object_penulis.insert_to_db(cursor, conn)
            flash("Penulis berhasil ditambahkan!", "success")

    return redirect(url_for('penulis_index'))

@app.route("/buku/penulis/edit/<id>", methods=['GET'])
def penulis_edit(id):
    cursor.execute("SELECT * FROM penulis WHERE id_penulis = %s", (id,))
    penulis = cursor.fetchone()
    
    if penulis:
        return render_template('buku/penulis/edit.html', penulis=penulis)
    else:
        flash("Penulis tidak ditemukan!", "error")
        return redirect(url_for('penulis_index'))

@app.route("/buku/penulis/update/<id>", methods=['POST'])
def penulis_update(id):
    if request.method == 'POST':
        nama_penulis = request.form['nama_penulis']

        if not nama_penulis:
            flash("Form masih kosong!", "error")
            return redirect(url_for('penulis_update', id))
        
        cursor.execute("SELECT * FROM penulis WHERE id_penulis = %s", (id,))
        penulis = cursor.fetchone()

        if penulis:
            # Object Penulis
            object_penulis = Penulis(nama_penulis)
            object_penulis.update_in_db(cursor, conn, id)
            flash("Penulis berhasil diupdate!", "success")
        else:
            flash("Penulis tidak ditemukan!", "error")

    return redirect(url_for('penulis_index'))

@app.route("/buku/penulis/delete/<id>", methods=['POST'])
def penulis_delete(id):
    try:
        cursor.execute("SELECT * FROM penulis WHERE id_penulis = %s", (id,))
        penulis = cursor.fetchone()

        if penulis:
            # Object Penulis
            object_penulis = Penulis("")
            object_penulis.delete_from_db(cursor, conn, id)
            flash("Penulis berhasil dihapus!", "success")
        else:
            flash("Penulis tidak ditemukan!", "error")
    except mysql.connector.IntegrityError as e:
        flash("Gagal menghapus penulis karena masih memiliki data terkait (integrity error).", "error")

    except mysql.connector.Error as e:
        flash(f"Terjadi kesalahan database: {e}", "error")

    return redirect(url_for('penulis_index'))



# Sumber Buku Route
@app.route("/buku/sumber/index")
def sumber_index():
    # Object Sumber
    object_sumber = Sumber("")
    sumber = object_sumber.read_from_db(cursor)
    return render_template('buku/sumber/index.html', sumber=sumber)

@app.route("/buku/sumber/tambah")
def sumber_create():
    return render_template('buku/sumber/create.html')

@app.route("/buku/sumber/insert", methods=['POST'])
def sumber_insert():
    if request.method == 'POST':
        nama_sumber = request.form['nama_sumber']

        if not nama_sumber:
            flash("Form masih kosong!", "error")
            return redirect(url_for('sumber_create'))
        
        cursor.execute("SELECT * FROM sumber WHERE nama_sumber = %s", (nama_sumber,))
        sumber = cursor.fetchone()

        if sumber:
            flash("Sumber sudah ada!", "error")
            return redirect(url_for('sumber_create'))
        else:
            # Object Sumber
            object_sumber = Sumber(nama_sumber)
            object_sumber.insert_to_db(cursor, conn)
            flash("Sumber berhasil ditambahkan!", "success")

    return redirect(url_for('sumber_index'))

@app.route("/buku/sumber/edit/<id>", methods=['GET'])
def sumber_edit(id):
    cursor.execute("SELECT * FROM sumber WHERE id_sumber = %s", (id,))
    sumber = cursor.fetchone()
    
    if sumber:
        return render_template('buku/sumber/edit.html', sumber=sumber)
    else:
        flash("Sumber tidak ditemukan!", "error")
        return redirect(url_for('sumber_index'))

@app.route("/buku/sumber/update/<id>", methods=['POST'])
def sumber_update(id):
    if request.method == 'POST':
        nama_sumber = request.form['nama_sumber']

        if not nama_sumber:
            flash("Form masih kosong!", "error")
            return redirect(url_for('sumber_update', id))
        
        cursor.execute("SELECT * FROM sumber WHERE id_sumber = %s", (id,))
        sumber = cursor.fetchone()

        if sumber:
            # Object Sumber
            object_sumber = Sumber(nama_sumber)
            object_sumber.update_in_db(cursor, conn, id)
            flash("Sumber berhasil diupdate!", "success")
        else:
            flash("Sumber tidak ditemukan!", "error")

    return redirect(url_for('sumber_index'))

@app.route("/buku/sumber/delete/<id>", methods=['POST'])
def sumber_delete(id):
    try:
        cursor.execute("SELECT * FROM sumber WHERE id_sumber = %s", (id,))
        sumber = cursor.fetchone()

        if sumber:
            # Object Sumber
            object_sumber = Sumber("")
            object_sumber.delete_from_db(cursor, conn, id)
            flash("Sumber berhasil dihapus!", "success")
        else:
            flash("Sumber tidak ditemukan!", "error")
            
    except mysql.connector.IntegrityError as e:
        flash("Gagal menghapus sumber karena masih memiliki data terkait (integrity error).", "error")

    except mysql.connector.Error as e:
        flash(f"Terjadi kesalahan database: {e}", "error")

    return redirect(url_for('sumber_index'))




# Anggota Route
@app.route("/anggota/index")
def anggota_index():
    # Object Anggota
    object_anggota = Anggota("","","","")
    anggota = object_anggota.read_from_db(cursor)
    return render_template('anggota/index.html', anggota=anggota)

@app.route("/anggota/tambah")
def anggota_create():
    return render_template('anggota/create.html')

@app.route("/anggota/insert", methods=['POST'])
def anggota_insert():
    if request.method == 'POST':
        nim_nip_anggota = request.form['nim_nip_anggota']
        nama_anggota = request.form['nama_anggota']
        alamat_anggota = request.form['alamat_anggota']
        no_hp_anggota = request.form['no_hp_anggota']
        
        # Untuk Melihat Panjang Angka NIM/NIP
        panjang_id = len(str(nim_nip_anggota))

        if not all([nim_nip_anggota, nama_anggota, alamat_anggota, no_hp_anggota]):
            flash("Form masih kosong atau ID Anggota tidak sesuai!", "error")
            return redirect(url_for('anggota_create'))
        
        if not nim_nip_anggota.isdigit():
            flash("NIM/NIP hanya boleh berupa angka!", "error")
            return redirect(url_for('anggota_create'))
        
        cursor.execute("SELECT * FROM anggota WHERE nim_nip = %s", (nim_nip_anggota,))
        anggota = cursor.fetchone()

        if anggota:
            flash("Anggota sudah ada!", "error")
            return redirect(url_for('anggota_create'))
        else:
            if panjang_id == 12:
                # Object Mahasiswa
                object_mahasiswa = Mahasiswa(nim_nip_anggota, nama_anggota, alamat_anggota, no_hp_anggota)
                object_mahasiswa.insert_to_db(cursor, conn)
                flash("Mahasiswa berhasil ditambahkan!", "success")
            elif panjang_id == 18:
                # Object Dosen
                object_dosen = Dosen(nim_nip_anggota, nama_anggota, alamat_anggota, no_hp_anggota)
                object_dosen.insert_to_db(cursor, conn)
                flash("Dosen berhasil ditambahkan!", "success")
            else:
                flash("NIM/NIP Anggota tidak sesuai!", "error")
                return redirect(url_for('anggota_create'))

    return redirect(url_for('anggota_index'))

@app.route("/anggota/edit/<id>", methods=['GET'])
def anggota_edit(id):
    cursor.execute("SELECT * FROM anggota WHERE nim_nip = %s", (id,))
    anggota = cursor.fetchone()
    
    if anggota:
        return render_template('anggota/edit.html', anggota=anggota)
    else:
        flash("Anggota tidak ditemukan!", "error")
        return redirect(url_for('anggota_index'))

@app.route("/anggota/update/<id>", methods=['POST'])
def anggota_update(id):
    if request.method == 'POST':
        nim_nip_anggota = request.form['nim_nip_anggota']
        nama_anggota = request.form['nama_anggota']
        alamat_anggota = request.form['alamat_anggota']
        no_hp_anggota = request.form['no_hp_anggota']
        
        # Untuk Melihat Panjang Angka NIM/NIP
        panjang_id = len(str(nim_nip_anggota))

        if not all([nim_nip_anggota, nama_anggota, alamat_anggota, no_hp_anggota]):
            flash("Form masih kosong", "error")
            return redirect(url_for('anggota_edit', id))
        
        if not nim_nip_anggota.isdigit():
            flash("NIM/NIP hanya boleh berupa angka!", "error")
            return redirect(url_for('anggota_edit', id))
        
        cursor.execute("SELECT * FROM anggota WHERE nim_nip = %s", (id,))
        anggota = cursor.fetchone()

        if anggota:
            if panjang_id == 12:
                # Object Mahasiswa
                object_mahasiswa = Mahasiswa(id, nama_anggota, alamat_anggota, no_hp_anggota)
                object_mahasiswa.update_in_db(cursor, conn, nim_nip_anggota)
                flash("Mahasiswa berhasil diupdate!", "success")
            elif panjang_id == 18:
                # Object Dosen
                object_dosen = Dosen(id, nama_anggota, alamat_anggota, no_hp_anggota)
                object_dosen.update_in_db(cursor, conn, nim_nip_anggota)
                flash("Dosen berhasil diupdate!", "success")
            else:
                flash("NIM/NIP Anggota tidak sesuai!", "error")
                return redirect(url_for('anggota_edit', id))
        else:
            flash("Anggota tidak ditemukan!", "error")

    return redirect(url_for('anggota_index'))

@app.route("/anggota/delete/<id>", methods=['POST'])
def anggota_delete(id):
    try:
        cursor.execute("SELECT * FROM anggota WHERE nim_nip = %s", (id,))
        anggota = cursor.fetchone()

        if anggota:
            # Untuk Melihat Panjang Angka NIM/NIP
            panjang_id = len(str(anggota[0]))
            
            if panjang_id == 12:
                # Object Mahasiswa
                object_mahasiswa = Mahasiswa(anggota[0],"","","")
                object_mahasiswa.delete_from_db(cursor, conn)
                flash("Mahasiswa berhasil dihapus!", "success")
            elif panjang_id == 18:
                # Object Dosen
                object_dosen = Dosen(anggota[0],"","","")
                object_dosen.delete_from_db(cursor, conn)
                flash("Dosen berhasil dihapus!", "success")
        else:
            flash("Anggota tidak ditemukan!", "error")
    
    except mysql.connector.IntegrityError as e:
        flash("Gagal menghapus anggota karena masih memiliki data terkait (integrity error).", "error")

    except mysql.connector.Error as e:
        flash(f"Terjadi kesalahan database: {e}", "error")

    return redirect(url_for('anggota_index'))



# Setor Buku Route
@app.route("/anggota/mahasiswa/setor_buku/index")
def mahasiswa_setor_buku_index():
    cursor.execute("SELECT * FROM view_buku_akhir")
    buku_akhir = cursor.fetchall()
    return render_template('anggota/setor_buku_akhir/index.html', buku_akhir=buku_akhir)

@app.route("/anggota/mahasiswa/setor_buku/create")
def mahasiswa_setor_buku_create():
    # Object Mahasiswa
    object_mahasiswa = Mahasiswa("", "", "", "")
    mahasiswa = object_mahasiswa.read_from_db(cursor, conn,)
    # Object Buku
    object_buku = Buku("","","","","")
    buku = object_buku.read_from_db(cursor, conn)
    return render_template('anggota/setor_buku_akhir/create.html', mahasiswa=mahasiswa, buku=buku)

@app.route("/anggota/mahasiswa/setor_buku/insert", methods=['POST'])
def mahasiswa_setor_buku_insert():
    if request.method == 'POST':
        nim = request.form['nim']
        id_buku = request.form['id_buku']
        nama_departemen = request.form['nama_departemen']
        nama_fakultas = request.form['nama_fakultas']

        # Validation
        if not all([nim, id_buku, nama_departemen, nama_fakultas]):
            flash("Form masih kosong!", "error")
            return redirect(url_for('mahasiswa_setor_buku_insert'))
        
        cursor.execute("SELECT * FROM buku_akhir WHERE fk_buku = %s", (id_buku,))
        buku_akhir = cursor.fetchone()

        # Pengecekan Data Buku Akhir dan Mahasiswa
        if buku_akhir:
            flash("Buku Akhir sudah ada!", "error")
            return redirect(url_for('mahasiswa_setor_buku_index'))
        
        # Object Buku Akhir
        object_mahasiswa = Mahasiswa(nim, "", "", "")
        object_mahasiswa.setor_buku_akhir(cursor, conn, id_buku, nama_departemen, nama_fakultas)
        flash("Buku Akhir berhasil ditambahkan!", "success")

    return redirect(url_for('mahasiswa_setor_buku_index'))

@app.route("/anggota/mahasiswa/setor_buku/edit/<id>", methods=['GET'])
def mahasiswa_setor_buku_edit(id):
    cursor.execute("SELECT * FROM buku_akhir WHERE fk_buku = %s", (id,))
    buku_akhir = cursor.fetchone()
    
    if buku_akhir:
        return render_template('anggota/setor_buku_akhir/edit.html', buku_akhir=buku_akhir)
    else:
        flash("Buku Akhir tidak ditemukan!", "error")
        return redirect(url_for('mahasiswa_setor_buku_index'))

@app.route("/anggota/mahasiswa/setor_buku/update/<id>", methods=['POST'])
def mahasiswa_setor_buku_update(id):
    if request.method == 'POST':
        nama_departemen = request.form['nama_departemen']
        nama_fakultas = request.form['nama_fakultas']

        # Validation
        if not all([nama_departemen, nama_fakultas]):
            flash("Form masih kosong!", "error")
            return redirect(url_for('mahasiswa_setor_buku_edit', id))
        
        cursor.execute("SELECT * FROM buku_akhir WHERE fk_buku = %s", (id,))
        buku_akhir = cursor.fetchone()
        
        if buku_akhir:
            # Object Buku Akhir
            object_mahasiswa = Mahasiswa("","","","")
            object_mahasiswa.update_buku_akhir(cursor, conn, id, nama_departemen, nama_fakultas)
            flash("Buku Akhir berhasil diupdate!", "success")
        else:
            flash("Buku Akhir tidak diupdate!", "error")

    return redirect(url_for('mahasiswa_setor_buku_index'))

@app.route("/anggota/mahasiswa/setor_buku/delete/<id>", methods=['POST'])
def mahasiswa_setor_buku_delete(id):
    try:
        cursor.execute("SELECT * FROM buku_akhir WHERE fk_buku = %s", (id,))
        buku_akhir = cursor.fetchone()

        if buku_akhir:
            # Object Buku Akhir
            object_mahasiswa = Mahasiswa("","","","")
            object_mahasiswa.delete_buku_akhir(cursor, conn, id)
            flash("Buku Akhir berhasil dihapus!", "success")
        else:
            flash("Buku Akhir tidak ditemukan!", "error")
        
    except mysql.connector.IntegrityError as e:
        flash("Gagal menghapus setor buku karena masih memiliki data terkait (integrity error).", "error")

    except mysql.connector.Error as e:
        flash(f"Terjadi kesalahan database: {e}", "error")

    return redirect(url_for('mahasiswa_setor_buku_index'))



# Peminjaman Route
@app.route("/peminjaman/index")
def peminjaman_index():
    object_peminjaman = Peminjaman("", "", "", "", "")
    object_peminjaman.perbarui_status_terlambat(cursor, conn)
    peminjaman = object_peminjaman.read_from_db(cursor)
    return render_template('peminjaman/index.html', peminjaman=peminjaman)

@app.route("/peminjaman/setor/index")
def peminjaman_setor_index():
    object_peminjaman = Peminjaman("", "", "", "", "")
    peminjaman = object_peminjaman.read_from_db_setor(cursor)
    return render_template('peminjaman/setor/index.html', peminjaman=peminjaman)

@app.route("/peminjaman/create")
def peminjaman_create():
    # Object Anggota
    object_anggota = Anggota("", "", "", "")
    anggota = object_anggota.read_from_db(cursor, conn)
    
    # Object Buku
    object_buku = Buku("", "", "", "", "")
    buku = object_buku.read_from_db(cursor, conn)
    return render_template('peminjaman/create.html', anggota=anggota, buku=buku)

@app.route("/peminjaman/insert", methods=['POST'])
def peminjaman_insert():
    if request.method == 'POST':
        nim_nip = request.form['nim_nip']
        batas_peminjaman = request.form['batas_peminjaman']
        id_buku_list = request.form.getlist("id_buku[]")

        # Menyimpan tanggal sekarang
        today = datetime.today()
        
        # Validation
        if not all([nim_nip, batas_peminjaman, id_buku_list]):
            flash("Form masih kosong!", "error")
            return redirect(url_for('peminjaman_insert'))
        
        # # Dicek apakah mahasiswa/dosen sudah mengembalikan buku yang dipinjam sebelumnya terlebih dahulu
        # cursor.execute("SELECT * FROM peminjaman WHERE fk_nim_nip = %s AND fk_status = %s", (nim_nip, 1))
        # exist = cursor.fetchone()
        
        # if exist:
        #     flash("Mohon Mengembalikan Buku yang Dipinjam Sebelumnya Terlebih Dahulu!", "error")
        #     return redirect(url_for('peminjaman_index'))
            
        # Object Buku
        object_peminjaman = Peminjaman(nim_nip, today, None, batas_peminjaman, 1)
        peminjaman_id = object_peminjaman.insert_to_db(cursor, conn)
        
        for id_buku in id_buku_list:
            object_detail = DetailPeminjaman(peminjaman_id, id_buku)
            object_detail.insert_to_db(cursor, conn)
        
        flash("Peminjaman berhasil ditambahkan!", "success")
    
    return redirect(url_for('peminjaman_index'))
    
@app.route("/peminjaman/edit/<id>", methods=['GET'])
def peminjaman_edit(id):
    cursor.execute("SELECT * FROM peminjaman WHERE id_peminjaman = %s", (id,))
    peminjaman = cursor.fetchone()
    
    if peminjaman:
        # Object Anggota
        object_anggota = Anggota("", "", "", "")
        anggota = object_anggota.read_from_db(cursor, conn)
        
        # Object Buku
        object_buku = Buku("", "", "", "", "")
        buku = object_buku.read_from_db(cursor, conn)
        
        # Load buku pada detail
        cursor.execute("SELECT fk_buku FROM detail_peminjaman WHERE fk_peminjaman = %s", (id,))
        detail = [row[0] for row in cursor.fetchall()]
        return render_template('peminjaman/edit.html', peminjaman=peminjaman, anggota=anggota, buku=buku, detail=detail)
    else:
        flash("Peminjaman tidak ditemukan!", "error")
    
    return redirect(url_for('peminjaman_index'))
    
@app.route("/peminjaman/update/<id>", methods=['POST'])
def peminjaman_update(id):
    nim_nip = request.form['nim_nip']
    batas_peminjaman = request.form['batas_peminjaman']
    id_buku_list = request.form.getlist("id_buku[]")

    # Menyimpan tanggal sekarang
    today = datetime.today()
    
    # Validation
    if not all([nim_nip, batas_peminjaman, id_buku_list]):
        flash("Form masih kosong!", "error")
        return redirect(url_for('peminjaman_update', id))
        
    # Object Peminjaman
    object_peminjaman = Peminjaman(nim_nip, today, None, batas_peminjaman, 1)
    object_peminjaman.update_in_db(cursor, conn, id)
    
    # Hapus Detail Peminjaman Lama
    object_detail = DetailPeminjaman(id, "")
    object_detail.delete_from_db(cursor, conn, id)
    
    for id_buku in id_buku_list:
        object_detail = DetailPeminjaman(id, id_buku)
        object_detail.insert_to_db(cursor, conn)
    
    flash("Peminjaman berhasil diupdate!", "success")

    return redirect(url_for('peminjaman_index'))

@app.route("/peminjaman/delete/<id>", methods=['POST'])
def peminjaman_delete(id):
    try:
        cursor.execute("SELECT * FROM peminjaman WHERE id_peminjaman = %s", (id,))
        peminjaman = cursor.fetchone()
        
        if peminjaman:
            # Object Peminjaman
            object_peminjaman = Peminjaman("","","","","")
            object_peminjaman.delete_from_db(cursor, conn, id)
            
            cursor.execute("SELECT * FROM detail_peminjaman WHERE fk_peminjaman = %s", (id,))
            detail = cursor.fetchone()
            
            if detail:
                # Object Detail
                object_detail = DetailPeminjaman(id, "")
                object_detail.delete_from_db(cursor, conn, id)
            else:
                flash("Detail tidak ditemukan!", "error")
                
            flash("Peminjaman berhasil dihapus!", "success")
        else:
            flash("Peminjaman tidak ditemukan!", "error")

    except mysql.connector.IntegrityError as e:
        flash("Gagal menghapus peminjaman karena masih memiliki data terkait (integrity error).", "error")

    except mysql.connector.Error as e:
        flash(f"Terjadi kesalahan database: {e}", "error")

    return redirect(url_for('peminjaman_index'))

@app.route("/peminjaman/<id>/approve", methods=['POST'])
def peminjaman_approve(id):
    cursor.execute("SELECT * FROM peminjaman WHERE id_peminjaman = %s", (id,))
    peminjaman = cursor.fetchone()

    if peminjaman:
        # Object Peminjaman
        object_peminjaman = Peminjaman("","","","","")
        object_peminjaman.perbarui_status_dikembalikan(cursor, conn, id)
        flash("Status Peminjaman berhasil diubah!", "success")
    else:
        flash("Peminjaman tidak ditemukan!", "error")
    
    return redirect(url_for('peminjaman_index'))


# Detail Route
@app.route("/peminjaman/detail/<id>", methods=['GET'])
def detail_peminjaman_index(id):
    # Object Detail
    object_detail = DetailPeminjaman(id, "")
    detail = object_detail.read_from_db(cursor)
    
    return render_template('peminjaman/detail/index.html', detail=detail, fk_peminjam=id)


# Main
if __name__ == '__main__':
    app.run(debug=True)