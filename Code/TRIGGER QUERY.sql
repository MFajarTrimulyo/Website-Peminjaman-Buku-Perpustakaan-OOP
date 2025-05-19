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
END;



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
END;


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
END;


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
END;


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
END;



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
END;



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
END;
//

DELIMITER ;
