from datetime import date
import mysql.connector

# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="perpustakaan_dtei"
)
cursor = conn.cursor()

class Anggota:
    def __init__(self, nim_nip, nama_anggota, alamat, no_hp):
        self.__nim_nip = nim_nip
        self.nama_anggota = nama_anggota
        self.alamat = alamat
        self.no_hp = no_hp
        
    def get_nim_nip(self):
        return self.__nim_nip

    def count_anggota(self, cursor, conn=None):
            cursor.execute("SELECT COUNT(*) FROM anggota")
            return cursor.fetchone()
        
    def insert_to_db(self, cursor, conn):
        sql = """
            INSERT INTO anggota (nim_nip, nama_anggota, alamat, no_hp)
            VALUES (%s, %s, %s, %s)
        """
        val = (self.__nim_nip, self.nama_anggota, self.alamat, self.no_hp)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "data berhasil ditambahkan.")

    def read_from_db(self, cursor, conn=None, nim_nip=None):
        if nim_nip:
            cursor.execute("SELECT * FROM anggota WHERE nim_nip = %s", (nim_nip,))
            return cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM anggota")
            return cursor.fetchall()

    def update_in_db(self, cursor, conn, new_nim_nip):
        sql = """
            UPDATE anggota
            SET nim_nip = %s, nama_anggota = %s, alamat = %s, no_hp = %s
            WHERE nim_nip = %s
        """
        val = (new_nim_nip, self.nama_anggota, self.alamat, self.no_hp, self.__nim_nip)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "anggota berhasil diperbarui.")

    def delete_from_db(self, cursor, conn):
        cursor.execute("DELETE FROM anggota WHERE nim_nip = %s", (self.__nim_nip,))
        conn.commit()
        print(cursor.rowcount, "anggota berhasil dihapus.")

class Mahasiswa(Anggota):
    def __init__(self, nim, nama, alamat, no_hp):
        super().__init__(nim, nama, alamat, no_hp)
        
    def read_from_db(self, cursor, conn=None, nim_nip=None):
        if nim_nip:
            cursor.execute("SELECT * FROM anggota WHERE LENGTH(nim_nip) = 12 AND nim_nip = %s", (nim_nip,))
            return cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM anggota WHERE LENGTH(nim_nip) = 12")
            return cursor.fetchall()
        
    def setor_buku_akhir(self, cursor, conn, id_buku, departemen, fakultas):
        sql = "CALL setor_buku_akhir (%s, %s, %s, %s) "
        val = (self.get_nim_nip(), id_buku, departemen, fakultas)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "buku berhasil ditambahkan.")
    
    def update_buku_akhir(self, cursor, conn, id_buku, departemen, fakultas):
        sql = "CALL update_buku_akhir (%s, %s, %s) "
        val = (id_buku, departemen, fakultas)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "buku berhasil diupdate.")
    
    def delete_buku_akhir(self, cursor, conn, id_buku):
        sql = "CALL delete_buku_akhir ( %s) "
        val = (id_buku,)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "buku berhasil dihapus.")

class Dosen(Anggota):
    def __init__(self, nip, nama, alamat, no_hp):
        super().__init__(nip, nama, alamat, no_hp)



class Nama:
    def __init__(self, nama):
        self.nama = nama

    def insert_to_db(self, cursor, conn):
        pass

class Buku(Nama):
    def __init__(self, nama_buku, fk_jbuku, fk_penulis, fk_penerbit, sumber):
        super().__init__(nama_buku)
        self.fk_jbuku = fk_jbuku
        self.fk_penulis = fk_penulis
        self.fk_penerbit = fk_penerbit
        self.sumber = sumber
        
    def count_buku(self, cursor, conn=None):
            cursor.execute("SELECT COUNT(*) FROM buku")
            return cursor.fetchone()

    def insert_to_db(self, cursor, conn):
        sql = """
            INSERT INTO buku (nama_buku, fk_jbuku, fk_penulis, fk_penerbit, fk_sumber)
            VALUES (%s, %s, %s, %s, %s)
        """
        val = (self.nama, self.fk_jbuku, self.fk_penulis, self.fk_penerbit, self.sumber)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "buku berhasil ditambahkan.")

    def read_from_db(self, cursor, conn=None, id_buku=None):
        if id_buku:
            cursor.execute("SELECT * FROM view_buku WHERE id_buku = %s", (id_buku,))
            return cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM view_buku")
            return cursor.fetchall()
        
    def update_in_db(self, cursor, conn, id_buku):
        sql = """
            UPDATE buku
            SET nama_buku = %s, fk_jbuku = %s, fk_penulis = %s, fk_penerbit = %s, fk_sumber = %s
            WHERE id_buku = %s
        """
        val = (self.nama, self.fk_jbuku, self.fk_penulis, self.fk_penerbit, self.sumber, id_buku)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "buku berhasil diperbarui.")

    def delete_from_db(self, cursor, conn, id_buku):
        cursor.execute("DELETE FROM buku WHERE id_buku = %s", (id_buku,))
        conn.commit()
        print(cursor.rowcount, "buku berhasil dihapus.")

class Jenis_Buku(Nama):
    def __init__(self, nama_jenis):
        super().__init__(nama_jenis)

    def insert_to_db(self, cursor, conn):
        sql = "INSERT INTO jenis_buku (nama_jenis) VALUES (%s)"
        cursor.execute(sql, (self.nama,))
        conn.commit()
        print(cursor.rowcount, "jenis buku berhasil ditambahkan.")

    def read_from_db(self, cursor, conn=None, id_jbuku=None):
        if id_jbuku:
            cursor.execute("SELECT * FROM jenis_buku WHERE id_jbuku = %s", (id_jbuku,))
            return cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM jenis_buku")
            return cursor.fetchall()

    def update_in_db(self, cursor, conn, id_jbuku):
        cursor.execute("UPDATE jenis_buku SET nama_jenis = %s WHERE id_jbuku = %s", (self.nama, id_jbuku))
        conn.commit()
        print(cursor.rowcount, "jenis buku berhasil diperbarui.")

    def delete_from_db(self, cursor, conn, id_jbuku):
        cursor.execute("DELETE FROM jenis_buku WHERE id_jbuku = %s", (id_jbuku,))
        conn.commit()
        print(cursor.rowcount, "jenis buku berhasil dihapus.")

class Penerbit(Nama):
    def __init__(self, nama_penerbit):
        super().__init__(nama_penerbit)

    def insert_to_db(self, cursor, conn):
        cursor.execute("INSERT INTO penerbit (nama_penerbit) VALUES (%s)", (self.nama,))
        conn.commit()
        print(cursor.rowcount, "penerbit berhasil ditambahkan.")

    def read_from_db(self, cursor, conn=None, id_penerbit=None):
        if id_penerbit:
            cursor.execute("SELECT * FROM penerbit WHERE id_penerbit = %s", (id_penerbit,))
            return cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM penerbit")
            return cursor.fetchall()

    def update_in_db(self, cursor, conn, id_penerbit):
        cursor.execute("UPDATE penerbit SET nama_penerbit = %s WHERE id_penerbit = %s", (self.nama, id_penerbit))
        conn.commit()
        print(cursor.rowcount, "penerbit berhasil diperbarui.")

    def delete_from_db(self, cursor, conn, id_penerbit):
        cursor.execute("DELETE FROM penerbit WHERE id_penerbit = %s", (id_penerbit,))
        conn.commit()
        print(cursor.rowcount, "penerbit berhasil dihapus.")

class Penulis(Nama):
    def __init__(self, nama_penulis):
        super().__init__(nama_penulis)

    def insert_to_db(self, cursor, conn):
        cursor.execute("INSERT INTO penulis (nama_penulis) VALUES (%s)", (self.nama,))
        conn.commit()
        print(cursor.rowcount, "penulis berhasil ditambahkan.")

    def read_from_db(self, cursor, conn=None, id_penulis=None):
        if id_penulis:
            cursor.execute("SELECT * FROM penulis WHERE id_penulis = %s", (id_penulis,))
            return cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM penulis")
            return cursor.fetchall()

    def update_in_db(self, cursor, conn, id_penulis):
        cursor.execute("UPDATE penulis SET nama_penulis = %s WHERE id_penulis = %s", (self.nama, id_penulis))
        conn.commit()
        print(cursor.rowcount, "penulis berhasil diperbarui.")

    def delete_from_db(self, cursor, conn, id_penulis):
        cursor.execute("DELETE FROM penulis WHERE id_penulis = %s", (id_penulis,))
        conn.commit()
        print(cursor.rowcount, "penulis berhasil dihapus.")

class Sumber(Nama):
    def __init__(self, nama_sumber):
        super().__init__(nama_sumber)

    def insert_to_db(self, cursor, conn):
        cursor.execute("INSERT INTO sumber (nama_sumber) VALUES (%s)", (self.nama,))
        conn.commit()
        print(cursor.rowcount, "sumber berhasil ditambahkan.")

    def read_from_db(self, cursor, conn=None, id_sumber=None):
        if id_sumber:
            cursor.execute("SELECT * FROM sumber WHERE id_sumber = %s", (id_sumber,))
            return cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM sumber")
            return cursor.fetchall()

    def update_in_db(self, cursor, conn, id_sumber):
        cursor.execute("UPDATE sumber SET nama_sumber = %s WHERE id_sumber = %s", (self.nama, id_sumber))
        conn.commit()
        print(cursor.rowcount, "sumber berhasil diperbarui.")

    def delete_from_db(self, cursor, conn, id_sumber):
        cursor.execute("DELETE FROM sumber WHERE id_sumber = %s", (id_sumber,))
        conn.commit()
        print(cursor.rowcount, "sumber berhasil dihapus.")


class Transaksi:
    def insert_to_db(self, cursor, conn):
        pass

    def read_from_db(self, cursor, id_data=None):
        pass

    def update_in_db(self, cursor, conn, id_data):
        pass

    def delete_from_db(self, cursor, conn, id_data):
        pass


class Peminjaman(Transaksi):
    def __init__(self, fk_nim_nip, tanggal_diambil, tanggal_disetor, batas_peminjaman, fk_status):
        self.fk_nim_nip = fk_nim_nip
        self.tanggal_diambil = tanggal_diambil
        self.tanggal_disetor = tanggal_disetor
        self.batas_peminjaman = batas_peminjaman
        self.fk_status = fk_status

    def count_peminjaman(self, cursor, conn=None):
            cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE fk_status != 3")
            return cursor.fetchone()
    
    def count_terlambat(self, cursor, conn=None):
            cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE fk_status = 3")
            return cursor.fetchone()
        
    def insert_to_db(self, cursor, conn):
        sql = """
            INSERT INTO peminjaman (fk_nim_nip, tanggal_diambil, tanggal_disetor, batas_peminjaman)
            VALUES (%s, %s, %s, %s)
        """
        val = (self.fk_nim_nip, self.tanggal_diambil, self.tanggal_disetor, self.batas_peminjaman)
        cursor.execute(sql, val)
        conn.commit()
        
        # Return Custom ID Peminjaman
        cursor.execute("""
            SELECT id_peminjaman FROM peminjaman
            WHERE fk_nim_nip = %s
            ORDER BY id_peminjaman DESC
            LIMIT 1
        """, (self.fk_nim_nip,))
        result = cursor.fetchone()
        return result[0] if result else None
        print(cursor.rowcount, "data peminjaman berhasil ditambahkan.")

    def read_from_db(self, cursor, id_peminjaman=None):
        if id_peminjaman:
            cursor.execute("SELECT * FROM view_peminjaman WHERE id_peminjaman = %s AND (status = 'Dipinjam' OR status = 'Terlambat')", (id_peminjaman,))
            return cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM view_peminjaman WHERE status = 'Dipinjam' OR status = 'Terlambat'")
            return cursor.fetchall()
    
    def read_from_db_setor(self, cursor, id_peminjaman=None):
        if id_peminjaman:
            cursor.execute("SELECT * FROM view_peminjaman WHERE id_peminjaman = %s AND fk_status = 3", (id_peminjaman,))
            return cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM view_peminjaman WHERE status = 'Dikembalikan'")
            return cursor.fetchall()

    def update_in_db(self, cursor, conn, id_peminjaman):
        sql = """
            UPDATE peminjaman
            SET fk_nim_nip = %s, batas_peminjaman = %s
            WHERE id_peminjaman = %s
        """
        val = (self.fk_nim_nip, self.batas_peminjaman, id_peminjaman,)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "data peminjaman berhasil diperbarui.")

    def delete_from_db(self, cursor, conn, id):
        cursor.execute("DELETE FROM peminjaman WHERE id_peminjaman = %s", (id,))
        conn.commit()
        print(cursor.rowcount, "data peminjaman berhasil dihapus.")
        
    def perbarui_status_terlambat(self, cursor, conn):
        today = date.today()

        cursor.execute("SELECT * FROM view_peminjaman")
        rows = cursor.fetchall()

        for row in rows:
            id_peminjaman = row[0]
            tanggal_disetor = row[4]
            batas_peminjaman = row[5]
            fk_status = row[6]

            # Jika belum dikembalikan dan sudah melewati batas peminjaman
            if tanggal_disetor is None and batas_peminjaman < today and fk_status != 'Terlambat':
                cursor.execute("CALL status_to_terlambat(%s)", (id_peminjaman,))
        
        conn.commit()
    
    def perbarui_status_dikembalikan(self, cursor, conn, id_peminjaman):
        sql = "CALL status_to_dikembalikan(%s)"
        val = (id_peminjaman,)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "status peminjaman berhasil diperbarui.")
        
        conn.commit()


class DetailPeminjaman(Transaksi):
    def __init__(self, id_peminjaman, fk_buku):
        self.id_peminjaman = id_peminjaman
        self.fk_buku = fk_buku

    def insert_to_db(self, cursor, conn):
        sql = "INSERT INTO detail_peminjaman (fk_peminjaman, fk_buku) VALUES (%s, %s)"
        val = (self.id_peminjaman, self.fk_buku)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "detail peminjaman berhasil ditambahkan.")

    def read_from_db(self, cursor):
        cursor.execute("SELECT * FROM view_detail_peminjaman WHERE fk_peminjaman = %s", (self.id_peminjaman,))
        return cursor.fetchall()

    def update_in_db(self, cursor, conn, fk_peminjaman):
        sql = """
            UPDATE detail_peminjaman
            SET fk_buku = %s
            WHERE fk_peminjaman = %s
        """
        val = (self.fk_buku, fk_peminjaman)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "detail peminjaman berhasil diperbarui.")

    def delete_from_db(self, cursor, conn, fk_peminjaman):
        cursor.execute("DELETE FROM detail_peminjaman WHERE fk_peminjaman = %s", (fk_peminjaman,))
        conn.commit()
        print(cursor.rowcount, "detail peminjaman berhasil dihapus.")