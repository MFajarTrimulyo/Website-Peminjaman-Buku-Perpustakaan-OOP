-- VIEW BUKU
CREATE VIEW view_buku AS
SELECT b.id_buku, b.nama_buku, jb.nama_jenis, ps.nama_penulis, pt.nama_penerbit, s.nama_sumber

FROM buku b

INNER JOIN jenis_buku jb
ON b.fk_jbuku = jb.id_jbuku
INNER JOIN penulis ps
ON b.fk_penulis = ps.id_penulis
INNER JOIN penerbit pt
ON b.fk_penerbit = pt.id_penerbit
INNER JOIN sumber s
ON b.fk_sumber = s.id_sumber


-- VIEW PEMINJAMAN
CREATE VIEW view_peminjaman AS
SELECT p.id_peminjaman, a.nama_anggota, p.tanggal_diambil, p.tanggal_disetor, p.batas_peminjaman, s.`status`

FROM peminjaman p

INNER JOIN anggota a
ON p.fk_nim_nip = a.nim_nip
INNER JOIN `status` s
ON p.fk_status = s.id_status


-- VIEW DETAIL PEMINJAMAN
CREATE VIEW view_detail_peminjaman AS
SELECT dp.id_detail, p.id_peminjaman, b.nama_buku

FROM detail_peminjaman dp

INNER JOIN peminjaman p
ON dp.fk_peminjaman = p.id_peminjaman
INNER JOIN buku b
ON dp.fk_buku = b.id_buku


-- VIEW BUKU AKHIR
CREATE VIEW view_buku_akhir AS
SELECT a.nim_nip, b.nama_buku, ba.nama_departemen, ba.nama_fakultas
FROM buku_akhir ba
INNER JOIN anggota a
ON ba.fk_nim = a.nim_nip
INNER JOIN buku b
ON ba.fk_buku = b.id_buku