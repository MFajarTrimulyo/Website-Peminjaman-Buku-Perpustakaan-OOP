-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.32-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.0.0.6468
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for perpustakaan_dtei
CREATE DATABASE IF NOT EXISTS `perpustakaan_dtei` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `perpustakaan_dtei`;

-- Dumping structure for table perpustakaan_dtei.anggota
CREATE TABLE IF NOT EXISTS `anggota` (
  `nim_nip` char(18) NOT NULL DEFAULT '0',
  `nama_anggota` varchar(50) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `no_hp` varchar(20) NOT NULL,
  PRIMARY KEY (`nim_nip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table perpustakaan_dtei.anggota: ~1 rows (approximately)
INSERT IGNORE INTO `anggota` (`nim_nip`, `nama_anggota`, `alamat`, `no_hp`) VALUES
	('240533607939', 'Fajar', '<p>Malang</p>', '0881');

-- Dumping structure for table perpustakaan_dtei.buku
CREATE TABLE IF NOT EXISTS `buku` (
  `id_buku` char(20) NOT NULL DEFAULT '',
  `nama_buku` varchar(50) NOT NULL,
  `fk_jbuku` char(20) NOT NULL DEFAULT '',
  `fk_penulis` char(20) NOT NULL DEFAULT '',
  `fk_penerbit` char(20) NOT NULL DEFAULT '',
  `fk_sumber` char(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_buku`),
  KEY `FK_jbuku` (`fk_jbuku`) USING BTREE,
  KEY `FK_penulis` (`fk_penulis`),
  KEY `FK_penerbit` (`fk_penerbit`),
  KEY `FK_sumber` (`fk_sumber`),
  CONSTRAINT `FK_jbuku` FOREIGN KEY (`fk_jbuku`) REFERENCES `jenis_buku` (`id_jbuku`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_penerbit` FOREIGN KEY (`fk_penerbit`) REFERENCES `penerbit` (`id_penerbit`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_penulis` FOREIGN KEY (`fk_penulis`) REFERENCES `penulis` (`id_penulis`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_sumber` FOREIGN KEY (`fk_sumber`) REFERENCES `sumber` (`id_sumber`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table perpustakaan_dtei.buku: ~1 rows (approximately)
INSERT IGNORE INTO `buku` (`id_buku`, `nama_buku`, `fk_jbuku`, `fk_penulis`, `fk_penerbit`, `fk_sumber`) VALUES
	('B250001', 'Halo Bang', 'JB250002', 'PS250001', 'PT250001', 'S250001');

-- Dumping structure for table perpustakaan_dtei.buku_akhir
CREATE TABLE IF NOT EXISTS `buku_akhir` (
  `fk_nim` char(20) NOT NULL,
  `fk_buku` char(50) NOT NULL,
  `nama_departemen` varchar(50) NOT NULL,
  `nama_fakultas` varchar(50) NOT NULL,
  KEY `fk_buku` (`fk_buku`),
  KEY `fk_nim` (`fk_nim`),
  CONSTRAINT `buku_akhir_ibfk_1` FOREIGN KEY (`fk_buku`) REFERENCES `buku` (`id_buku`),
  CONSTRAINT `buku_akhir_ibfk_2` FOREIGN KEY (`fk_nim`) REFERENCES `anggota` (`nim_nip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table perpustakaan_dtei.buku_akhir: ~0 rows (approximately)

-- Dumping structure for procedure perpustakaan_dtei.delete_buku_akhir
DELIMITER //
CREATE PROCEDURE `delete_buku_akhir`(
	IN `idbuku` CHAR(20)
)
BEGIN
	DELETE FROM buku_akhir WHERE fk_buku = idbuku;
END//
DELIMITER ;

-- Dumping structure for table perpustakaan_dtei.detail_peminjaman
CREATE TABLE IF NOT EXISTS `detail_peminjaman` (
  `id_detail` char(20) NOT NULL DEFAULT '',
  `fk_peminjaman` char(20) NOT NULL DEFAULT '',
  `fk_buku` char(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_detail`),
  KEY `FK_peminjaman` (`fk_peminjaman`),
  KEY `FK_buku` (`fk_buku`),
  CONSTRAINT `FK_buku` FOREIGN KEY (`fk_buku`) REFERENCES `buku` (`id_buku`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_peminjaman` FOREIGN KEY (`fk_peminjaman`) REFERENCES `peminjaman` (`id_peminjaman`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table perpustakaan_dtei.detail_peminjaman: ~0 rows (approximately)

-- Dumping structure for table perpustakaan_dtei.id_counter
CREATE TABLE IF NOT EXISTS `id_counter` (
  `table_name` varchar(50) NOT NULL,
  `year_suffix` char(2) NOT NULL,
  `last_number` int(11) DEFAULT NULL,
  PRIMARY KEY (`table_name`,`year_suffix`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table perpustakaan_dtei.id_counter: ~5 rows (approximately)
INSERT IGNORE INTO `id_counter` (`table_name`, `year_suffix`, `last_number`) VALUES
	('buku', '25', 1),
	('jenis_buku', '25', 2),
	('penerbit', '25', 1),
	('penulis', '25', 1),
	('sumber', '25', 1);

-- Dumping structure for table perpustakaan_dtei.jenis_buku
CREATE TABLE IF NOT EXISTS `jenis_buku` (
  `id_jbuku` char(20) NOT NULL DEFAULT '',
  `nama_jenis` varchar(50) NOT NULL,
  PRIMARY KEY (`id_jbuku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table perpustakaan_dtei.jenis_buku: ~1 rows (approximately)
INSERT IGNORE INTO `jenis_buku` (`id_jbuku`, `nama_jenis`) VALUES
	('JB250002', 'Skripsi');

-- Dumping structure for table perpustakaan_dtei.peminjaman
CREATE TABLE IF NOT EXISTS `peminjaman` (
  `id_peminjaman` char(20) NOT NULL DEFAULT '',
  `fk_nim_nip` char(18) NOT NULL,
  `tanggal_diambil` date DEFAULT NULL,
  `tanggal_disetor` date DEFAULT NULL,
  `batas_peminjaman` varchar(50) NOT NULL,
  `fk_status` enum('1','2','3') NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_peminjaman`),
  KEY `FK_nim_nip` (`fk_nim_nip`),
  KEY `FK_status` (`fk_status`),
  CONSTRAINT `FK_nim_nip` FOREIGN KEY (`fk_nim_nip`) REFERENCES `anggota` (`nim_nip`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_status` FOREIGN KEY (`fk_status`) REFERENCES `status` (`id_status`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table perpustakaan_dtei.peminjaman: ~0 rows (approximately)

-- Dumping structure for table perpustakaan_dtei.penerbit
CREATE TABLE IF NOT EXISTS `penerbit` (
  `id_penerbit` char(20) NOT NULL DEFAULT '',
  `nama_penerbit` varchar(50) NOT NULL,
  PRIMARY KEY (`id_penerbit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table perpustakaan_dtei.penerbit: ~1 rows (approximately)
INSERT IGNORE INTO `penerbit` (`id_penerbit`, `nama_penerbit`) VALUES
	('PT250001', 'Universitas Negeri Malang');

-- Dumping structure for table perpustakaan_dtei.penulis
CREATE TABLE IF NOT EXISTS `penulis` (
  `id_penulis` char(20) NOT NULL DEFAULT '',
  `nama_penulis` varchar(50) NOT NULL,
  PRIMARY KEY (`id_penulis`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table perpustakaan_dtei.penulis: ~1 rows (approximately)
INSERT IGNORE INTO `penulis` (`id_penulis`, `nama_penulis`) VALUES
	('PS250001', 'Fajar');

-- Dumping structure for procedure perpustakaan_dtei.setor_buku_akhir
DELIMITER //
CREATE PROCEDURE `setor_buku_akhir`(
	IN nim CHAR(20),
	IN idbuku CHAR(20),
	IN departemen VARCHAR(50),
	IN fakultas VARCHAR(50)
)
BEGIN
	INSERT INTO buku_akhir (fk_nim, fk_buku, nama_departemen, nama_fakultas) VALUES 
	(nim, idbuku, departemen, nama_fakultas);
END//
DELIMITER ;

-- Dumping structure for table perpustakaan_dtei.status
CREATE TABLE IF NOT EXISTS `status` (
  `id_status` enum('1','2','3') NOT NULL,
  `status` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table perpustakaan_dtei.status: ~3 rows (approximately)
INSERT IGNORE INTO `status` (`id_status`, `status`) VALUES
	('1', 'Dipinjam'),
	('2', 'Dikembalikan'),
	('3', 'Terlambat');

-- Dumping structure for procedure perpustakaan_dtei.status_to_dikembalikan
DELIMITER //
CREATE PROCEDURE `status_to_dikembalikan`(IN id CHAR(20))
BEGIN
    UPDATE peminjaman
    SET fk_status = 2
    WHERE id_peminjaman = id;
END//
DELIMITER ;

-- Dumping structure for table perpustakaan_dtei.sumber
CREATE TABLE IF NOT EXISTS `sumber` (
  `id_sumber` char(20) NOT NULL DEFAULT '',
  `nama_sumber` varchar(50) NOT NULL,
  PRIMARY KEY (`id_sumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table perpustakaan_dtei.sumber: ~1 rows (approximately)
INSERT IGNORE INTO `sumber` (`id_sumber`, `nama_sumber`) VALUES
	('S250001', 'Hibah');

-- Dumping structure for procedure perpustakaan_dtei.update_buku_akhir
DELIMITER //
CREATE PROCEDURE `update_buku_akhir`(
	IN `idbuku` CHAR(20),
	IN `departemen` VARCHAR(50),
	IN `fakultas` VARCHAR(50)
)
BEGIN
	UPDATE buku_akhir 
	SET nama_departemen = departemen, nama_fakultas = fakultas
	WHERE fk_buku = idbuku;
END//
DELIMITER ;

-- Dumping structure for view perpustakaan_dtei.view_buku
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `view_buku` (
	`id_buku` CHAR(20) NOT NULL COLLATE 'utf8mb4_general_ci',
	`nama_buku` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	`nama_jenis` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	`nama_penulis` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	`nama_penerbit` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	`nama_sumber` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for view perpustakaan_dtei.view_buku_akhir
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `view_buku_akhir` (
	`nim_nip` CHAR(18) NOT NULL COLLATE 'utf8mb4_general_ci',
	`id_buku` CHAR(20) NOT NULL COLLATE 'utf8mb4_general_ci',
	`nama_buku` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	`nama_departemen` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	`nama_fakultas` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for view perpustakaan_dtei.view_detail_peminjaman
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `view_detail_peminjaman` (
	`id_detail` CHAR(20) NOT NULL COLLATE 'utf8mb4_general_ci',
	`id_peminjaman` CHAR(20) NOT NULL COLLATE 'utf8mb4_general_ci',
	`nama_buku` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for view perpustakaan_dtei.view_peminjaman
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `view_peminjaman` (
	`id_peminjaman` CHAR(20) NOT NULL COLLATE 'utf8mb4_general_ci',
	`nim_nip` CHAR(18) NOT NULL COLLATE 'utf8mb4_general_ci',
	`nama_anggota` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	`tanggal_diambil` DATE NULL,
	`tanggal_disetor` DATE NULL,
	`batas_peminjaman` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci',
	`status` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for trigger perpustakaan_dtei.before_insert_buku
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER before_insert_buku
BEFORE INSERT ON buku
FOR EACH ROW
BEGIN
    DECLARE prefix CHAR(2) DEFAULT 'B';
    DECLARE suffix_year CHAR(2);
    DECLARE next_number INT;
    DECLARE formatted_id VARCHAR(10);

    SET suffix_year = RIGHT(YEAR(CURDATE()), 2);

    -- Jika tidak ada data tahun sekarang, inisialisasi tahun
    IF (SELECT COUNT(*) FROM id_counter WHERE table_name = 'buku' AND year_suffix = suffix_year) = 0 THEN
        INSERT INTO id_counter (table_name, year_suffix, last_number) VALUES ('buku', suffix_year, 0);
    END IF;

    -- Mendapatkan nomer selanjutnya
    SELECT last_number + 1 INTO next_number
    FROM id_counter
    WHERE table_name = 'buku' AND year_suffix = suffix_year;

    -- Update counter
    UPDATE id_counter
    SET last_number = next_number
    WHERE table_name = 'buku' AND year_suffix = suffix_year;

    -- ID Akhir
    SET formatted_id = CONCAT(prefix, suffix_year, LPAD(next_number, 4, '0'));

    SET NEW.id_buku = formatted_id;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger perpustakaan_dtei.before_insert_detail_peminjaman
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER before_insert_detail_peminjaman
BEFORE INSERT ON detail_peminjaman
FOR EACH ROW
BEGIN
    DECLARE prefix CHAR(2) DEFAULT 'DP';
    DECLARE suffix_year CHAR(2);
    DECLARE next_number INT;
    DECLARE formatted_id VARCHAR(10);

    SET suffix_year = RIGHT(YEAR(CURDATE()), 2);

    -- Jika tidak ada data tahun sekarang, inisialisasi tahun
    IF (SELECT COUNT(*) FROM id_counter WHERE TABLE_NAME = 'detail_peminjaman' AND year_suffix = suffix_year) = 0 THEN
        INSERT INTO id_counter (table_name, year_suffix, last_number) VALUES ('detail_peminjaman', suffix_year, 0);
    END IF;

    -- Mendapatkan nomer selanjutnya
    SELECT last_number + 1 INTO next_number
    FROM id_counter
    WHERE table_name = 'detail_peminjaman' AND year_suffix = suffix_year;

    -- Update counter
    UPDATE id_counter
    SET last_number = next_number
    WHERE table_name = 'detail_peminjaman' AND year_suffix = suffix_year;

    -- ID Akhir
    SET formatted_id = CONCAT(prefix, suffix_year, LPAD(next_number, 4, '0'));

    SET NEW.id_detail = formatted_id;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger perpustakaan_dtei.before_insert_jenis_buku
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER before_insert_jenis_buku
BEFORE INSERT ON jenis_buku
FOR EACH ROW
BEGIN
    DECLARE prefix CHAR(2) DEFAULT 'JB';
    DECLARE suffix_year CHAR(2);
    DECLARE next_number INT;
    DECLARE formatted_id VARCHAR(10);

    SET suffix_year = RIGHT(YEAR(CURDATE()), 2);

    -- Jika tidak ada data tahun sekarang, inisialisasi tahun
    IF (SELECT COUNT(*) FROM id_counter WHERE TABLE_NAME = 'jenis_buku' AND year_suffix = suffix_year) = 0 THEN
        INSERT INTO id_counter (table_name, year_suffix, last_number) VALUES ('jenis_buku', suffix_year, 0);
    END IF;

    -- Mendapatkan nomer selanjutnya
    SELECT last_number + 1 INTO next_number
    FROM id_counter
    WHERE table_name = 'jenis_buku' AND year_suffix = suffix_year;

    -- Update counter
    UPDATE id_counter
    SET last_number = next_number
    WHERE table_name = 'jenis_buku' AND year_suffix = suffix_year;

    -- ID Akhir
    SET formatted_id = CONCAT(prefix, suffix_year, LPAD(next_number, 4, '0'));

    SET NEW.id_jbuku = formatted_id;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger perpustakaan_dtei.before_insert_peminjaman
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER before_insert_peminjaman
BEFORE INSERT ON peminjaman
FOR EACH ROW
BEGIN
    DECLARE prefix CHAR(2) DEFAULT 'P';
    DECLARE suffix_year CHAR(2);
    DECLARE next_number INT;
    DECLARE formatted_id VARCHAR(10);

    SET suffix_year = RIGHT(YEAR(CURDATE()), 2);

    -- Jika tidak ada data tahun sekarang, inisialisasi tahun
    IF (SELECT COUNT(*) FROM id_counter WHERE TABLE_NAME = 'peminjaman' AND year_suffix = suffix_year) = 0 THEN
        INSERT INTO id_counter (table_name, year_suffix, last_number) VALUES ('peminjaman', suffix_year, 0);
    END IF;

    -- Mendapatkan nomer selanjutnya
    SELECT last_number + 1 INTO next_number
    FROM id_counter
    WHERE table_name = 'peminjaman' AND year_suffix = suffix_year;

    -- Update counter
    UPDATE id_counter
    SET last_number = next_number
    WHERE table_name = 'peminjaman' AND year_suffix = suffix_year;

    -- ID Akhir
    SET formatted_id = CONCAT(prefix, suffix_year, LPAD(next_number, 4, '0'));

    SET NEW.id_peminjaman = formatted_id;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger perpustakaan_dtei.before_insert_penerbit
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER before_insert_penerbit
BEFORE INSERT ON penerbit
FOR EACH ROW
BEGIN
    DECLARE prefix CHAR(2) DEFAULT 'PT';
    DECLARE suffix_year CHAR(2);
    DECLARE next_number INT;
    DECLARE formatted_id VARCHAR(10);

    SET suffix_year = RIGHT(YEAR(CURDATE()), 2);

    -- Jika tidak ada data tahun sekarang, inisialisasi tahun
    IF (SELECT COUNT(*) FROM id_counter WHERE TABLE_NAME = 'penerbit' AND year_suffix = suffix_year) = 0 THEN
        INSERT INTO id_counter (table_name, year_suffix, last_number) VALUES ('penerbit', suffix_year, 0);
    END IF;

    -- Mendapatkan nomer selanjutnya
    SELECT last_number + 1 INTO next_number
    FROM id_counter
    WHERE table_name = 'penerbit' AND year_suffix = suffix_year;

    -- Update counter
    UPDATE id_counter
    SET last_number = next_number
    WHERE table_name = 'penerbit' AND year_suffix = suffix_year;

    -- ID Akhir
    SET formatted_id = CONCAT(prefix, suffix_year, LPAD(next_number, 4, '0'));

    SET NEW.id_penerbit = formatted_id;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger perpustakaan_dtei.before_insert_penulis
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER before_insert_penulis
BEFORE INSERT ON penulis
FOR EACH ROW
BEGIN
    DECLARE prefix CHAR(2) DEFAULT 'PS';
    DECLARE suffix_year CHAR(2);
    DECLARE next_number INT;
    DECLARE formatted_id VARCHAR(10);

    SET suffix_year = RIGHT(YEAR(CURDATE()), 2);

    -- Jika tidak ada data tahun sekarang, inisialisasi tahun
    IF (SELECT COUNT(*) FROM id_counter WHERE TABLE_NAME = 'penulis' AND year_suffix = suffix_year) = 0 THEN
        INSERT INTO id_counter (table_name, year_suffix, last_number) VALUES ('penulis', suffix_year, 0);
    END IF;

    -- Mendapatkan nomer selanjutnya
    SELECT last_number + 1 INTO next_number
    FROM id_counter
    WHERE table_name = 'penulis' AND year_suffix = suffix_year;

    -- Update counter
    UPDATE id_counter
    SET last_number = next_number
    WHERE table_name = 'penulis' AND year_suffix = suffix_year;

    -- ID Akhir
    SET formatted_id = CONCAT(prefix, suffix_year, LPAD(next_number, 4, '0'));

    SET NEW.id_penulis = formatted_id;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger perpustakaan_dtei.before_insert_sumber
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER before_insert_sumber
BEFORE INSERT ON sumber
FOR EACH ROW
BEGIN
    DECLARE prefix CHAR(2) DEFAULT 'S';
    DECLARE suffix_year CHAR(2);
    DECLARE next_number INT;
    DECLARE formatted_id VARCHAR(10);

    SET suffix_year = RIGHT(YEAR(CURDATE()), 2);

    -- Jika tidak ada data tahun sekarang, inisialisasi tahun
    IF (SELECT COUNT(*) FROM id_counter WHERE TABLE_NAME = 'sumber' AND year_suffix = suffix_year) = 0 THEN
        INSERT INTO id_counter (table_name, year_suffix, last_number) VALUES ('sumber', suffix_year, 0);
    END IF;

    -- Mendapatkan nomer selanjutnya
    SELECT last_number + 1 INTO next_number
    FROM id_counter
    WHERE table_name = 'sumber' AND year_suffix = suffix_year;

    -- Update counter
    UPDATE id_counter
    SET last_number = next_number
    WHERE table_name = 'sumber' AND year_suffix = suffix_year;

    -- ID Akhir
    SET formatted_id = CONCAT(prefix, suffix_year, LPAD(next_number, 4, '0'));

    SET NEW.id_sumber = formatted_id;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for view perpustakaan_dtei.view_buku
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `view_buku`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `view_buku` AS SELECT b.id_buku, b.nama_buku, jb.nama_jenis, ps.nama_penulis, pt.nama_penerbit, s.nama_sumber

FROM buku b

INNER JOIN jenis_buku jb
ON b.fk_jbuku = jb.id_jbuku
INNER JOIN penulis ps
ON b.fk_penulis = ps.id_penulis
INNER JOIN penerbit pt
ON b.fk_penerbit = pt.id_penerbit
INNER JOIN sumber s
ON b.fk_sumber = s.id_sumber ;

-- Dumping structure for view perpustakaan_dtei.view_buku_akhir
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `view_buku_akhir`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `view_buku_akhir` AS SELECT a.nim_nip, b.id_buku, b.nama_buku, ba.nama_departemen, ba.nama_fakultas
FROM buku_akhir ba
INNER JOIN anggota a
ON ba.fk_nim = a.nim_nip
INNER JOIN buku b
ON ba.fk_buku = b.id_buku ;

-- Dumping structure for view perpustakaan_dtei.view_detail_peminjaman
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `view_detail_peminjaman`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `view_detail_peminjaman` AS SELECT dp.id_detail, p.id_peminjaman, b.nama_buku

FROM detail_peminjaman dp

INNER JOIN peminjaman p
ON dp.fk_peminjaman = p.id_peminjaman
INNER JOIN buku b
ON dp.fk_buku = b.id_buku ;

-- Dumping structure for view perpustakaan_dtei.view_peminjaman
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `view_peminjaman`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `view_peminjaman` AS SELECT p.id_peminjaman, a.nim_nip, a.nama_anggota, p.tanggal_diambil, p.tanggal_disetor, p.batas_peminjaman, s.`status`

FROM peminjaman p

INNER JOIN anggota a
ON p.fk_nim_nip = a.nim_nip
INNER JOIN status s
ON p.fk_status = s.id_status ;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
