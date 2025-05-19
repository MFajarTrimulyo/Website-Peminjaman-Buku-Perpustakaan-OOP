import mysql.connector

# Koneksi ke data base
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "perpustakaan_dtei"
)
cursor = conn.cursor()

class Anggota:
    def __init__(self, nim_nip, nama_anggota, alamat, no_hp):
        self.__nim_nip = nim_nip
        self.nama_anggota = nama_anggota
        self.alamat = alamat
        self.no_hp = no_hp

    def insert_to_db(self, cursor, conn):
        sql = """
            INSERT INTO anggota (nim_nip, nama_anggota, alamat, no_hp)
            VALUES (%s, %s, %s, %s)
        """
        val = (self.__nim_nip, self.nama_anggota, self.alamat, self.no_hp)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "data berhasil ditambahkan.")

class Mahasiswa(Anggota):
    def __init__(self, nim, nama, alamat, no_hp):
        super().__init__(nim, nama, alamat, no_hp)

class Dosen(Anggota):
    def __init__(self, nip, nama, alamat, no_hp):
        super().__init__(nip, nama, alamat, no_hp)
        
        
        

class Nama:
    def __init__(self, nama):
        self.nama = nama

    def insert_to_db(self, cursor, conn):
        print("Subclass harus mengimplementasikan method ini.")

class Buku(Nama):
    def __init__(self, nama_buku, fk_jbuku, fk_penulis, fk_penerbit, sumber):
        super().__init__(nama_buku)
        self.fk_jbuku = fk_jbuku
        self.fk_penulis = fk_penulis
        self.fk_penerbit = fk_penerbit
        self.sumber = sumber

    def insert_to_db(self, cursor, conn):
        sql = """
            CALL insert_buku(%s, %s, %s, %s, %s)
        """
        val = (self.nama, self.fk_jbuku, self.fk_penulis, self.fk_penerbit, self.sumber)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "buku berhasil ditambahkan.")
        
    def read_from_db(self, cursor, id_buku=None):
        if id_buku:
            cursor.execute("CALL read_buku_by_id(%s)", (id_buku,))
        else:
            cursor.execute("CALL read_buku()")
        for row in cursor.fetchall():
            print(row)

    def update_in_db(self, cursor, conn, id_buku):
        cursor.execute("CALL update_buku(%s, %s, %s, %s, %s, %s)",
                       (id_buku, self.nama, self.fk_jbuku, self.fk_penulis, self.fk_penerbit, self.sumber))
        conn.commit()
        print(cursor.rowcount, "buku berhasil diperbarui.")

    def delete_from_db(self, cursor, conn, id_buku):
        cursor.execute("CALL delete_buku(%s)", (id_buku,))
        conn.commit()
        print(cursor.rowcount, "buku berhasil dihapus.")

class Jenis_Buku(Nama):
    def __init__(self, nama_jenis):
        super().__init__(nama_jenis)

    def insert_to_db(self, cursor, conn):
        sql = "CALL insert_jbuku(%s)"
        val = (self.nama,)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "penerbit berhasil ditambahkan.")

    def read_from_db(self, cursor, id_jbuku=None):
        if id_jbuku:
            cursor.execute("CALL read_jbuku_by_id(%s)", (id_jbuku,))
        else:
            cursor.execute("CALL read_jbuku()")
        for row in cursor.fetchall():
            print(row)

    def update_in_db(self, cursor, conn, id_jbuku):
        cursor.execute("CALL update_jbuku(%s, %s)", (id_jbuku, self.nama))
        conn.commit()
        print(cursor.rowcount, "jenis buku berhasil diperbarui.")

    def delete_from_db(self, cursor, conn, id_jbuku):
        cursor.execute("CALL delete_jbuku(%s)", (id_jbuku,))
        conn.commit()
        print(cursor.rowcount, "jenis buku berhasil dihapus.")

class Penerbit(Nama):
    def __init__(self, nama_penerbit):
        super().__init__(nama_penerbit)

    def insert_to_db(self, cursor, conn):
        sql = "CALL insert_penerbit(%s)"
        val = (self.nama,)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "penerbit berhasil ditambahkan.")

    def read_from_db(self, cursor, id_penerbit=None):
        if id_penerbit:
            cursor.execute("CALL read_penerbit_by_id(%s)", (id_penerbit,))
        else:
            cursor.execute("CALL read_penerbit()")
        for row in cursor.fetchall():
            print(row)

    def update_in_db(self, cursor, conn, id_penerbit):
        cursor.execute("CALL update_penerbit(%s, %s)", (id_penerbit, self.nama))
        conn.commit()
        print(cursor.rowcount, "penerbit berhasil diperbarui.")

    def delete_from_db(self, cursor, conn, id_penerbit):
        cursor.execute("CALL delete_penerbit(%s)", (id_penerbit,))
        conn.commit()
        print(cursor.rowcount, "penerbit berhasil dihapus.")

class Penulis(Nama):
    def __init__(self, nama_penulis):
        super().__init__(nama_penulis)

    def insert_to_db(self, cursor, conn):
        sql = "CALL insert_penulis(%s)"
        val = (self.nama,)
        cursor.execute(sql, val)
        conn.commit()
        print(cursor.rowcount, "penulis berhasil ditambahkan.")

    def read_from_db(self, cursor, id_penulis=None):
        if id_penulis:
            cursor.execute("CALL read_penulis_by_id(%s)", (id_penulis,))
        else:
            cursor.execute("CALL read_penulis()")
        for row in cursor.fetchall():
            print(row)

    def update_in_db(self, cursor, conn, id_penulis):
        cursor.execute("CALL update_penulis(%s, %s)", (id_penulis, self.nama))
        conn.commit()
        print(cursor.rowcount, "penulis berhasil diperbarui.")

    def delete_from_db(self, cursor, conn, id_penulis):
        cursor.execute("CALL delete_penulis(%s)", (id_penulis,))
        conn.commit()
        print(cursor.rowcount, "penulis berhasil dihapus.")