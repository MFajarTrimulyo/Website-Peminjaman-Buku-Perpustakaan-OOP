DELIMITER //

-- Status Dikembalikan
CREATE PROCEDURE status_to_dikembalikan(IN id CHAR(20))
BEGIN
    UPDATE peminjaman
    SET fk_status = 2
    WHERE id_peminjaman = id;
END;

CREATE PROCEDURE status_to_terlambat(IN id CHAR(20))
BEGIN
    UPDATE peminjaman
    SET fk_status = 3
    WHERE id_peminjaman = id;
END;

-- Setor Buku Akhir
CREATE PROCEDURE setor_buku_akhir(
	IN nim CHAR(20),
	IN idbuku CHAR(20),
	IN departemen VARCHAR(50),
	IN fakultas VARCHAR(50)
)
BEGIN
	INSERT INTO buku_akhir (fk_nim, fk_buku, nama_departemen, nama_fakultas) VALUES 
	(nim, idbuku, departemen, nama_fakultas);
END;

-- Update Buku Akhir
CREATE PROCEDURE update_buku_akhir(
	IN nim CHAR(20),
	IN idbuku CHAR(20),
	IN departemen VARCHAR(50),
	IN fakultas VARCHAR(50)
)
BEGIN
	UPDATE buku_akhir 
	SET nama_departemen = departemen, nama_fakultas = fakultas
	WHERE fk_nim = nim AND fk_buku = idbuku;
END;

-- Delete Buku Akhir
CREATE PROCEDURE delete_buku_akhir(
	IN nim CHAR(20),
	IN idbuku CHAR(20)
)
BEGIN
	DELETE FROM buku_akhir WHERE fk_nim = nim AND fk_buku = idbuku;
END;

//
DELIMITER ;
