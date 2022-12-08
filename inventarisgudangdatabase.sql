/*
SQLyog Ultimate v12.5.1 (64 bit)
MySQL - 10.4.25-MariaDB : Database - inventarisgudang
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`inventarisgudang` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `inventarisgudang`;

/*Table structure for table `barangkeluar` */

DROP TABLE IF EXISTS `barangkeluar`;

CREATE TABLE `barangkeluar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_stok` varchar(255) DEFAULT NULL,
  `id_barang` int(11) DEFAULT NULL,
  `id_user` int(11) DEFAULT NULL,
  `kode_jabatan` int(11) DEFAULT NULL,
  `jumlah` varchar(50) DEFAULT NULL,
  `tgl_keluar` date DEFAULT NULL,
  `id_permintaan` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_stok` (`id_stok`),
  KEY `id_barang` (`id_barang`),
  KEY `id_user` (`id_user`),
  KEY `id_jurusan` (`kode_jabatan`),
  KEY `id_permintaan` (`id_permintaan`),
  CONSTRAINT `barangkeluar_ibfk_3` FOREIGN KEY (`id_stok`) REFERENCES `stokbarang` (`id_stok`),
  CONSTRAINT `barangkeluar_ibfk_4` FOREIGN KEY (`id_barang`) REFERENCES `masterbarang` (`id_barang`),
  CONSTRAINT `barangkeluar_ibfk_5` FOREIGN KEY (`id_user`) REFERENCES `pegawai` (`id_user`),
  CONSTRAINT `barangkeluar_ibfk_6` FOREIGN KEY (`kode_jabatan`) REFERENCES `jabatan` (`kode_jabatan`),
  CONSTRAINT `barangkeluar_ibfk_7` FOREIGN KEY (`id_permintaan`) REFERENCES `permintaan` (`id_permintaan`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4;

/*Data for the table `barangkeluar` */

insert  into `barangkeluar`(`id`,`id_stok`,`id_barang`,`id_user`,`kode_jabatan`,`jumlah`,`tgl_keluar`,`id_permintaan`) values 
(21,'ST35233',18,3,3,'1','2022-12-02',31),
(22,'ST35233',18,3,3,'1','2022-12-02',31),
(23,'ST35233',18,3,3,'1','2022-12-02',31);

/*Table structure for table `employee` */

DROP TABLE IF EXISTS `employee`;

CREATE TABLE `employee` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `employee` */

insert  into `employee`(`id`,`name`,`email`,`phone`) values 
(0,'Ilham','ilhamlagiaja@gmail.com',''),
(2,'dwada','dawdsa','dawdaw'),
(3,'wadsfd','','');

/*Table structure for table `historypesanan` */

DROP TABLE IF EXISTS `historypesanan`;

CREATE TABLE `historypesanan` (
  `namabarang` varchar(255) DEFAULT NULL,
  `jumlahpesan` varchar(255) DEFAULT NULL,
  `tanggalpesan` varchar(255) DEFAULT NULL,
  `tanggalperubahan` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `historypesanan` */

insert  into `historypesanan`(`namabarang`,`jumlahpesan`,`tanggalpesan`,`tanggalperubahan`) values 
('BR240','1','2022-09-10','2022-09-18'),
('BR240','1','2022-09-10','2022-09-18'),
('BR240','1','2022-09-10','2022-09-18'),
('BR240','1','2022-09-10','2022-09-18'),
('BR240','1','2022-09-10','2022-09-18'),
('BR240','1','2022-09-10','2022-09-18'),
('BR240','1','2022-09-10','2022-09-18'),
('BR200','2','2022-08-20','2022-09-19'),
('BR200','2','2022-08-20','2022-09-19'),
(NULL,NULL,NULL,'2022-09-25'),
(NULL,NULL,NULL,'2022-09-25'),
('BR210',NULL,NULL,'2022-09-25'),
('BR210','3',NULL,'2022-09-25'),
('BR210','3','2022-09-25','2022-09-25'),
('BR230','24','2022-09-25','2022-09-25'),
('BR230','21','2022-09-27','2022-09-27'),
('BR200','2','2022-08-20','2022-09-27'),
('BR200','2','2022-08-20','2022-09-27'),
('BR240','1','2022-09-10','2022-10-03'),
('BR200','2','2022-08-20','2022-10-03'),
('BR210','1','2022-08-21','2022-10-03'),
('BR230','11','2022-09-27','2022-10-07'),
('BR230','11','2022-09-27','2022-10-07'),
('BR230','11','2022-09-27','2022-10-07'),
('BR230','11','2022-09-27','2022-10-07'),
('BR230','11','2022-09-27','2022-10-07'),
('BR200','2','2022-08-20','2022-10-07'),
('BR210','1','2022-08-21','2022-10-07'),
('BR230','24','2022-09-25','2022-10-07'),
('BR240','1','2022-09-10','2022-10-07'),
('BR230','11','2022-09-27','2022-10-07'),
('BR210','3','2022-09-25','2022-10-07'),
('BR230','21','2022-09-27','2022-10-07'),
('1','25','2022-10-14','2022-10-14'),
('3','100','2022-10-14','2022-10-14'),
('3','100','2022-10-14','2022-10-14'),
('3','100','2022-10-14','2022-10-14'),
('1','10','2022-10-25','2022-10-25'),
('1','25','2022-10-14','2022-10-31'),
('1','10','2022-10-25','2022-10-31'),
('3','10','2022-10-31','2022-11-09'),
('14','22','2022-11-09','2022-11-09'),
('3','2','2022-11-07','2022-11-14'),
('3','2','2022-11-07','2022-11-14'),
('18','1','2022-11-27','2022-11-27'),
('19','3','2022-11-27','2022-11-27'),
('19','3','2022-11-27','2022-11-27'),
('18','1','2022-11-27','2022-11-27'),
('18','1','2022-11-27','2022-11-27'),
('18','3','2022-11-27','2022-11-27'),
('18','1','2022-11-27','2022-11-27'),
('18','3','2022-11-27','2022-11-27'),
('18','3','2022-11-27','2022-11-27'),
('18','3','2022-11-27','2022-11-27'),
('19','3','2022-11-27','2022-11-27'),
('18','3','2022-11-27','2022-11-27'),
('18','3','2022-11-27','2022-11-27'),
('18','3','2022-11-27','2022-11-27'),
('19','3','2022-11-27','2022-11-27'),
('18','3','2022-11-27','2022-11-27'),
('19','1','2022-11-28','2022-11-28'),
('19','1','2022-11-28','2022-11-28'),
('19','1','2022-11-28','2022-11-28'),
('18','1','2022-12-13','2022-11-30'),
('18','1','2022-12-13','2022-11-30'),
('18','1','2022-12-02','2022-12-02'),
('18','1','2022-12-02','2022-12-02'),
('18','1','2022-12-02','2022-12-02');

/*Table structure for table `jabatan` */

DROP TABLE IF EXISTS `jabatan`;

CREATE TABLE `jabatan` (
  `kode_jabatan` int(11) NOT NULL AUTO_INCREMENT,
  `nama_jabatan` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`kode_jabatan`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

/*Data for the table `jabatan` */

insert  into `jabatan`(`kode_jabatan`,`nama_jabatan`) values 
(1,'Kepala Jurusan BDP'),
(2,'Kepala Jurusan MM'),
(3,'Kepala Jurusan RPL'),
(4,'Kepala Sekolah'),
(5,'Kepala Gudang'),
(7,'Kepala Jurusan TJKT');

/*Table structure for table `kartubarang` */

DROP TABLE IF EXISTS `kartubarang`;

CREATE TABLE `kartubarang` (
  `idkartubaran` varchar(255) NOT NULL,
  `id_barang` varchar(50) DEFAULT NULL,
  `id_stok` varchar(50) DEFAULT NULL,
  `id_satuan` varchar(50) DEFAULT NULL,
  `namabarang` varchar(255) DEFAULT NULL,
  `jumlahmasuk` char(20) DEFAULT NULL,
  `jumlahkeluar` char(20) DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idkartubaran`),
  KEY `id_barang` (`id_barang`),
  KEY `id_stok` (`id_stok`),
  KEY `id_satuan` (`id_satuan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `kartubarang` */

/*Table structure for table `kategoribarang` */

DROP TABLE IF EXISTS `kategoribarang`;

CREATE TABLE `kategoribarang` (
  `id_kategori` int(11) NOT NULL AUTO_INCREMENT,
  `namakategori` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id_kategori`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4;

/*Data for the table `kategoribarang` */

insert  into `kategoribarang`(`id_kategori`,`namakategori`) values 
(32,'ATK'),
(33,'Elektronik'),
(34,'Percetakan'),
(35,'Perabot Kantor'),
(37,'Dapur');

/*Table structure for table `masterbarang` */

DROP TABLE IF EXISTS `masterbarang`;

CREATE TABLE `masterbarang` (
  `id_barang` int(11) NOT NULL AUTO_INCREMENT,
  `id_stok` varchar(255) DEFAULT NULL,
  `id_kategori` int(11) DEFAULT NULL,
  `id_satuan` int(11) DEFAULT NULL,
  `namabarang` varchar(235) DEFAULT NULL,
  `merk` varchar(235) DEFAULT NULL,
  `idsumberdana` int(11) DEFAULT NULL,
  `files` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_barang`),
  KEY `id_kategori` (`id_kategori`),
  KEY `id_satuan` (`id_satuan`),
  KEY `id_stok` (`id_stok`),
  KEY `idsumberdana` (`idsumberdana`),
  CONSTRAINT `masterbarang_ibfk_2` FOREIGN KEY (`id_kategori`) REFERENCES `kategoribarang` (`id_kategori`),
  CONSTRAINT `masterbarang_ibfk_3` FOREIGN KEY (`id_satuan`) REFERENCES `satuanbarang` (`id_satuan`),
  CONSTRAINT `masterbarang_ibfk_4` FOREIGN KEY (`idsumberdana`) REFERENCES `sumberdana` (`idsumberdana`),
  CONSTRAINT `masterbarang_ibfk_5` FOREIGN KEY (`id_stok`) REFERENCES `stokbarang` (`id_stok`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;

/*Data for the table `masterbarang` */

insert  into `masterbarang`(`id_barang`,`id_stok`,`id_kategori`,`id_satuan`,`namabarang`,`merk`,`idsumberdana`,`files`) values 
(17,'ST102525000',32,1,'Pensil','Joyko',5,'image.png'),
(18,'ST35233',33,4,'Projektor','Infocus',4,'png-transparent-mitsubishi-multimedia-projectors-lcd-projector-wide-xga-projector-electronics-electronic-device-mitsubishi.png'),
(19,'ST3244',34,3,'Kertas HVS A4','SIDU',5,'kertas-hvs-a4-7.1631439028.jpg'),
(20,'ST50230105',32,1,'Pulpen','Joyko',5,'UI2DdIYmAqmlB9t2D8oQvFJHHOGmjslHmj5VXMZM.png'),
(21,'ST3421222',37,6,'Minyak','Bunga Matahari',4,'png-transparent-sunflower-oil-cooking-oils-frying-greas-food-cooking-oil.png'),
(22,'ST5324332',33,1,'Kabel HDMI','Sony',4,'kabelhdmi.png'),
(23,'ST25011222',33,1,'Kabel VGA','Sony',5,'kabelvga.png'),
(24,'ST1021222',33,1,'Harddisk 500 Gb','Seagate',5,'gambarharddisk.png'),
(25,'ST3521222',32,2,'Iodin Povidon','Betadine',5,'betadine.png');

/*Table structure for table `pegawai` */

DROP TABLE IF EXISTS `pegawai`;

CREATE TABLE `pegawai` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `kode_jabatan` int(11) DEFAULT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `nip` varchar(30) DEFAULT NULL,
  `email` varchar(75) DEFAULT NULL,
  `id_status` varchar(50) DEFAULT NULL,
  `nomor_tlp` varchar(255) DEFAULT NULL,
  `id_unitkerja` int(11) DEFAULT NULL,
  `tingkat` enum('Kepala Gudang','Kepala Sekolah','Pegawai') DEFAULT NULL,
  PRIMARY KEY (`id_user`),
  KEY `kode_jurusan` (`kode_jabatan`),
  KEY `id_status` (`id_status`),
  KEY `id_unitkerja` (`id_unitkerja`),
  CONSTRAINT `pegawai_ibfk_2` FOREIGN KEY (`id_status`) REFERENCES `status` (`id_status`),
  CONSTRAINT `pegawai_ibfk_3` FOREIGN KEY (`kode_jabatan`) REFERENCES `jabatan` (`kode_jabatan`),
  CONSTRAINT `pegawai_ibfk_4` FOREIGN KEY (`id_unitkerja`) REFERENCES `unitkerja` (`id_unitkerja`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

/*Data for the table `pegawai` */

insert  into `pegawai`(`id_user`,`kode_jabatan`,`nama`,`nip`,`email`,`id_status`,`nomor_tlp`,`id_unitkerja`,`tingkat`) values 
(1,4,'Ino Soprano','19630708 198703 1 009','inosoprano@gmail.com','S1','089375882718',1,'Kepala Sekolah'),
(2,5,'Toni Kusmana','19800509 201408 1 001','tonikusmana@gmail.com','S1','0895374821745',1,'Kepala Gudang'),
(3,3,'Usep Suterjo','19730502 199702 2 003','usepsuterjo@gmail.com','S1','0895285728472',1,'Pegawai'),
(4,1,'Tati Sutarni','19630115 199203 2 002','tatisutarni@gmail.com','S2','089673992847',1,'Pegawai'),
(5,7,'Siti Nurhaeni','19830203 202103 3 010','sitinurhaeni@gmail.com','S2','080392842',1,'Pegawai'),
(11,2,'Ilham Faisal Ridhotulloh','ilhamaja','ilhamfaisalrr@gmail.com','S1','08965600502',1,'Pegawai');

/*Table structure for table `permintaan` */

DROP TABLE IF EXISTS `permintaan`;

CREATE TABLE `permintaan` (
  `id_permintaan` int(11) NOT NULL AUTO_INCREMENT,
  `id_unitkerja` int(11) DEFAULT NULL,
  `id_user` int(11) DEFAULT NULL,
  `kode_jabatan` int(11) DEFAULT NULL,
  `id_barang` int(11) DEFAULT NULL,
  `jumlahpesan` varchar(40) DEFAULT NULL,
  `tanggalpesan` date DEFAULT NULL,
  `idstatuspesanan` varchar(255) DEFAULT NULL,
  `alasan` varchar(255) DEFAULT NULL,
  `id_stok` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_permintaan`),
  KEY `id_unitkerja` (`id_unitkerja`),
  KEY `kode_jurusan` (`kode_jabatan`),
  KEY `id_barang` (`id_barang`),
  KEY `id_user` (`id_user`),
  KEY `idstatuspesanan` (`idstatuspesanan`),
  KEY `id_stok` (`id_stok`),
  CONSTRAINT `permintaan_ibfk_1` FOREIGN KEY (`id_unitkerja`) REFERENCES `unitkerja` (`id_unitkerja`),
  CONSTRAINT `permintaan_ibfk_2` FOREIGN KEY (`id_user`) REFERENCES `pegawai` (`id_user`),
  CONSTRAINT `permintaan_ibfk_3` FOREIGN KEY (`kode_jabatan`) REFERENCES `jabatan` (`kode_jabatan`),
  CONSTRAINT `permintaan_ibfk_4` FOREIGN KEY (`id_barang`) REFERENCES `masterbarang` (`id_barang`),
  CONSTRAINT `permintaan_ibfk_5` FOREIGN KEY (`idstatuspesanan`) REFERENCES `statuspesanan` (`idstatuspesanan`),
  CONSTRAINT `permintaan_ibfk_6` FOREIGN KEY (`id_stok`) REFERENCES `stokbarang` (`id_stok`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4;

/*Data for the table `permintaan` */

insert  into `permintaan`(`id_permintaan`,`id_unitkerja`,`id_user`,`kode_jabatan`,`id_barang`,`jumlahpesan`,`tanggalpesan`,`idstatuspesanan`,`alasan`,`id_stok`) values 
(30,1,3,3,22,'1','2022-12-02','1',NULL,'ST5324332'),
(31,1,3,3,18,'1','2022-12-02','3',NULL,'ST35233'),
(32,1,3,3,19,'2','2022-12-02','1',NULL,'ST3244');

/*Table structure for table `rak` */

DROP TABLE IF EXISTS `rak`;

CREATE TABLE `rak` (
  `id_rak` int(11) NOT NULL AUTO_INCREMENT,
  `nama_rak` varchar(255) DEFAULT NULL,
  `kapasitas_rak` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_rak`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

/*Data for the table `rak` */

insert  into `rak`(`id_rak`,`nama_rak`,`kapasitas_rak`) values 
(1,'A1','200'),
(2,'A2','100'),
(7,'Rak A5','70');

/*Table structure for table `satuanbarang` */

DROP TABLE IF EXISTS `satuanbarang`;

CREATE TABLE `satuanbarang` (
  `id_satuan` int(11) NOT NULL AUTO_INCREMENT,
  `nama_satuan` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_satuan`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;

/*Data for the table `satuanbarang` */

insert  into `satuanbarang`(`id_satuan`,`nama_satuan`) values 
(1,'Pcs'),
(2,'Buah'),
(3,'Rim'),
(4,'Unit'),
(5,'Pack'),
(6,'Liter');

/*Table structure for table `status` */

DROP TABLE IF EXISTS `status`;

CREATE TABLE `status` (
  `id_status` char(30) NOT NULL,
  `nama_status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `status` */

insert  into `status`(`id_status`,`nama_status`) values 
('S1','Aktif'),
('S2','Nonaktif');

/*Table structure for table `statuspesanan` */

DROP TABLE IF EXISTS `statuspesanan`;

CREATE TABLE `statuspesanan` (
  `idstatuspesanan` varchar(255) NOT NULL,
  `namastatuspesanan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idstatuspesanan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `statuspesanan` */

insert  into `statuspesanan`(`idstatuspesanan`,`namastatuspesanan`) values 
('1','Pending'),
('2','Siap Diambil'),
('3','Sudah Diambil'),
('4','Ditolak'),
('5','DiACC');

/*Table structure for table `stokbarang` */

DROP TABLE IF EXISTS `stokbarang`;

CREATE TABLE `stokbarang` (
  `id_stok` varchar(255) NOT NULL,
  `stok` int(11) DEFAULT NULL,
  `jml_barang_msk` int(11) DEFAULT NULL,
  `tgl_masuk` date DEFAULT NULL,
  `hrg_satuan` int(11) DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  `id_supplier` int(11) DEFAULT NULL,
  `id_rak` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_stok`),
  KEY `id_supplier` (`id_supplier`),
  KEY `id_rak` (`id_rak`),
  CONSTRAINT `stokbarang_ibfk_1` FOREIGN KEY (`id_supplier`) REFERENCES `supplier` (`id_supplier`),
  CONSTRAINT `stokbarang_ibfk_2` FOREIGN KEY (`id_rak`) REFERENCES `rak` (`id_rak`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `stokbarang` */

insert  into `stokbarang`(`id_stok`,`stok`,`jml_barang_msk`,`tgl_masuk`,`hrg_satuan`,`total`,`id_supplier`,`id_rak`) values 
('ST1021222',10,10,'2022-12-02',250000,2500000,5,2),
('ST102525000',25,10,'2022-11-27',25000,250000,1,2),
('ST25011222',25,25,'2022-12-02',25000,625000,5,2),
('ST3244',20,25,'2022-11-27',25000,500000,1,1),
('ST3421222',34,34,'2022-12-02',3500,119000,6,2),
('ST3521222',10,10,'2022-12-02',4500,45000,2,2),
('ST35233',29,35,'2022-11-27',30000,700000,5,1),
('ST50230105',50,50,'2022-12-02',3000,150000,1,2),
('ST5324332',52,53,'2022-12-02',15000,795000,5,1);

/*Table structure for table `sumberdana` */

DROP TABLE IF EXISTS `sumberdana`;

CREATE TABLE `sumberdana` (
  `idsumberdana` int(11) NOT NULL AUTO_INCREMENT,
  `namasumberdana` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`idsumberdana`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

/*Data for the table `sumberdana` */

insert  into `sumberdana`(`idsumberdana`,`namasumberdana`) values 
(4,'BOS'),
(5,'BOPD');

/*Table structure for table `supplier` */

DROP TABLE IF EXISTS `supplier`;

CREATE TABLE `supplier` (
  `id_supplier` int(11) NOT NULL AUTO_INCREMENT,
  `namasupplier` varchar(245) DEFAULT NULL,
  `nomortelepon` char(15) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `alamat` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id_supplier`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

/*Data for the table `supplier` */

insert  into `supplier`(`id_supplier`,`namasupplier`,`nomortelepon`,`email`,`alamat`) values 
(1,'Supplier ATK','232425345','supplieratk@gmail.com','Jalan ATK'),
(2,'Supplier Kesehatan','089656338283','supplierkesehatan@gmail.com','Jalan Kesehatan'),
(5,'Supplier Elektronik','0894782647','supplierelektronik@gmail.com','Jalan Sarimadu Barat'),
(6,'Supplier Dapur','08989278642','supplierdapur@gmail.com','Jalan Bojongsoang');

/*Table structure for table `unitkerja` */

DROP TABLE IF EXISTS `unitkerja`;

CREATE TABLE `unitkerja` (
  `id_unitkerja` int(11) NOT NULL AUTO_INCREMENT,
  `namaunitkerja` varchar(100) DEFAULT NULL,
  `alamat` varchar(100) DEFAULT NULL,
  `no_telp` varchar(15) DEFAULT NULL,
  `no_fax` varchar(20) DEFAULT NULL,
  `email` varchar(25) DEFAULT NULL,
  `web` varchar(50) DEFAULT NULL,
  `cabang` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_unitkerja`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

/*Data for the table `unitkerja` */

insert  into `unitkerja`(`id_unitkerja`,`namaunitkerja`,`alamat`,`no_telp`,`no_fax`,`email`,`web`,`cabang`) values 
(1,'SMKN 11 Bandung','Jl. Budi Jl. Raya Cilember, RT.01/RW.04, Sukaraja, Kec. Cicendo, Kota Bandung, Jawa Barat 40153','(022) 6652442','(022) 6652442','smk11@gmail.com','smkn11bdg.scola.id','Jawa Barat');

/* Trigger structure for table `permintaan` */

DELIMITER $$

/*!50003 DROP TRIGGER*//*!50032 IF EXISTS */ /*!50003 `barangkurang` */$$

/*!50003 CREATE */ /*!50017 DEFINER = 'root'@'localhost' */ /*!50003 TRIGGER `barangkurang` AFTER INSERT ON `permintaan` FOR EACH ROW BEGIN
	UPDATE stokbarang SET stok= stok - NEW.jumlahpesan
    WHERE id_stok = NEW.id_stok;
END */$$


DELIMITER ;

/* Trigger structure for table `permintaan` */

DELIMITER $$

/*!50003 DROP TRIGGER*//*!50032 IF EXISTS */ /*!50003 `gantistatus` */$$

/*!50003 CREATE */ /*!50017 DEFINER = 'root'@'localhost' */ /*!50003 TRIGGER `gantistatus` BEFORE UPDATE ON `permintaan` FOR EACH ROW BEGIN
    INSERT INTO historypesanan SELECT OLD.id_barang, OLD.jumlahpesan, OLD.tanggalpesan, NOW();
END */$$


DELIMITER ;

/* Trigger structure for table `permintaan` */

DELIMITER $$

/*!50003 DROP TRIGGER*//*!50032 IF EXISTS */ /*!50003 `barangtelahkeluar` */$$

/*!50003 CREATE */ /*!50017 DEFINER = 'root'@'localhost' */ /*!50003 TRIGGER `barangtelahkeluar` AFTER UPDATE ON `permintaan` FOR EACH ROW 
BEGIN
   IF OLD.id_barang = new.id_barang THEN
      INSERT INTO barangkeluar(id_stok,id_barang, id_user,kode_jabatan, jumlah,id_permintaan)
      VALUES(old.id_stok, old.id_barang, old.id_user,old.kode_jabatan,old.jumlahpesan,old.id_permintaan);
   END IF;
END */$$


DELIMITER ;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
