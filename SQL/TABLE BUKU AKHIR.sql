CREATE TABLE buku_akhir (
	fk_nim CHAR(20) NOT NULL,
	fk_buku CHAR(50) NOT NULL,
	nama_departemen VARCHAR(50) NOT NULL,
	nama_fakultas VARCHAR(50) NOT NULL,
	
	
	FOREIGN KEY (fk_buku) REFERENCES buku(id_buku),
	FOREIGN KEY (fk_nim) REFERENCES anggota(nim_nip)
);
