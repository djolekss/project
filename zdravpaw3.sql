-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 30, 2025 at 07:02 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `zdravpaw3`
--

-- --------------------------------------------------------

--
-- Table structure for table `istorija_bolesti`
--

CREATE TABLE `istorija_bolesti` (
  `id` int(11) NOT NULL,
  `termin_id` int(11) DEFAULT NULL,
  `zivotinja_id` int(11) DEFAULT NULL,
  `vreme_pregleda` datetime DEFAULT current_timestamp(),
  `dijagnoza` varchar(255) DEFAULT NULL,
  `terapija` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `istorija_bolesti`
--

INSERT INTO `istorija_bolesti` (`id`, `termin_id`, `zivotinja_id`, `vreme_pregleda`, `dijagnoza`, `terapija`) VALUES
(1, 26, NULL, '2025-06-28 21:37:01', 'F191', 'Brufen po potrebi'),
(2, 26, NULL, '2025-06-28 21:39:16', 'F191', 'Brufen po potrebi'),
(3, 28, NULL, '2025-06-28 21:39:43', 'F191', 'Pentraksil 15 dana ujutru uvece '),
(4, 26, NULL, '2025-06-28 21:45:59', 'prelom', 'mirovanje'),
(5, 27, NULL, '2025-06-28 21:47:48', 'prelom', 'Brufen po potrebi'),
(6, 26, NULL, '2025-06-28 21:52:40', 'adwdad', 'dawd'),
(7, 29, NULL, '2025-06-28 22:57:32', 'F191', 'Remirta 121mg'),
(8, 30, NULL, '2025-06-28 23:20:39', 'F191', 'Xanax'),
(9, 26, NULL, '2025-06-28 23:32:11', 'F191', 'Xanax'),
(10, 31, 3, '2025-06-30 15:18:32', 'Povišena temperatura', 'Pronison 3 x dnevno '),
(11, 32, 3, '2025-06-30 16:08:37', 'prelom', 'miro'),
(12, 28, 2, '2025-06-30 18:31:48', 'glavobolja', 'brufen'),
(13, 36, 1, '2025-06-30 18:45:34', 'Glvobolja', 'Brufen');

-- --------------------------------------------------------

--
-- Table structure for table `korisnici`
--

CREATE TABLE `korisnici` (
  `korisnik_id` int(11) NOT NULL,
  `ime` varchar(30) NOT NULL,
  `prezime` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` char(32) NOT NULL,
  `is_admin` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `korisnici`
--

INSERT INTO `korisnici` (`korisnik_id`, `ime`, `prezime`, `email`, `password`, `is_admin`) VALUES
(1, 'Admin', 'Admin', 'admin@gmail.com', '2e33a9b0b06aa0a01ede70995674ee23', 1),
(5, 'Dragan', 'Davidović', 'davidovicdragan1@gmail.com', '86bc43e556b1df283839f053eb02e2bb', 0),
(6, 'Nevena', 'Davidovic', 'nd@gmail.com', '86bc43e556b1df283839f053eb02e2bb', 0),
(8, 'Nikola', 'Davidović', 'nikola.davidovic92@gmail.com', 'fcc317126c5c482954bd9dbd0111dd4e', 0),
(9, 'Nevena', 'Davidović', 'wpvezba@gmail.com', 'fcc317126c5c482954bd9dbd0111dd4e', 0),
(10, 'Milica ', 'Krstic', 'milica@gmail.com', 'fcc317126c5c482954bd9dbd0111dd4e', 0),
(11, 'Nemanja', 'Krstic', 'nkrstic@gmail.com', '86bc43e556b1df283839f053eb02e2bb', 0),
(12, 'Milos', 'Knezevic', 'm@gmail.com', '86bc43e556b1df283839f053eb02e2bb', 0),
(13, 'Vladan', 'Savic', 'v@gmail.com', '86bc43e556b1df283839f053eb02e2bb', 0),
(14, 'Verica', 'Milic', 'vm@gmail.com', '9ce70f5b0f0d601f21cf6a6261875515', 0),
(15, 'Jasmina', 'Davidovic', 'j@gmail.com', '86bc43e556b1df283839f053eb02e2bb', 0),
(16, 'Tanja', 'Danilovic', 'tdanilovic@gmail.com', '86bc43e556b1df283839f053eb02e2bb', 0),
(17, 'Marko ', 'Markovic', 'mm@gmail.com', 'f31e1eef20f64733a18c538073e78396', 0),
(18, 'Đorđe', 'Davidović', 'djdavidovic@gmail.com', 'fcc317126c5c482954bd9dbd0111dd4e', 0);

-- --------------------------------------------------------

--
-- Table structure for table `poruke`
--

CREATE TABLE `poruke` (
  `poruka_id` int(11) NOT NULL,
  `email` varchar(30) NOT NULL,
  `broj_telefona` varchar(30) DEFAULT NULL,
  `poruka` varchar(1000) NOT NULL,
  `poslato` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` enum('pročitano','nepročitano') DEFAULT 'nepročitano'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `poruke`
--

INSERT INTO `poruke` (`poruka_id`, `email`, `broj_telefona`, `poruka`, `poslato`, `status`) VALUES
(1, 'petar@gmail.com', '0604202641', 'Test', '2025-06-21 11:45:07', 'pročitano'),
(2, 'djole@gmail.com', '0651234657', 'AMWDLKNALWJKDNJLAKWNDJAWNDJKMANDANWD<MANWD<MANWD<MANWDM<NAW<MDNA<MWND<AMWND<ANWDM<ANWDM<ANWDM<NAWM<DNAWNDAWNDMAWNDM<ANWD<MAWNDM<ANWDM<ANWD<NAWD<', '2025-06-21 12:09:07', 'pročitano'),
(3, 'test@gmail.com', '0651234657', 'h5 class=\"card-title\">{{ p[1] }} <small class=\"text-muted\">({{ p[2] }})</small></h5>\r\n                        <h6 class=\"card-subtitle mb-2 text-muted\">{{ p[4] }}</h6>\r\n                        <p class=\"card-text\">{{ p[3][:200] }}{% if p[3]|length > 200 %}...{% endif %}</p>\r\n                        <div class=\"d-flex justify-content-end mt-3\">\r\n                            <a href=\"\" class=\"btn btn-sm btn-prim', '2025-06-21 12:09:49', 'pročitano'),
(4, 'kosta@gmail.com', '0659020777', 'Test test ', '2025-06-30 15:02:03', 'pročitano'),
(5, 'mm@gmail.com', '0651234657', 'Test\r\n', '2025-06-30 15:57:33', 'pročitano'),
(6, 'test@gmail.com', '0659020777', 'test\r\n', '2025-06-30 15:59:24', 'pročitano'),
(7, 'a@gmail.com', '034023020', 'Test', '2025-06-30 16:01:43', 'pročitano'),
(8, 'test@gmail.com', '0651234657', 'test', '2025-06-30 16:39:31', 'pročitano');

-- --------------------------------------------------------

--
-- Table structure for table `termini`
--

CREATE TABLE `termini` (
  `termin_id` int(11) NOT NULL,
  `korisnik_id` int(11) NOT NULL,
  `veterinar_id` int(11) NOT NULL,
  `datum` date NOT NULL,
  `vreme` time NOT NULL,
  `opis` varchar(255) NOT NULL,
  `status` enum('na čekanju','zakazano','odbijeno','izvršeno') NOT NULL DEFAULT 'na čekanju'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `termini`
--

INSERT INTO `termini` (`termin_id`, `korisnik_id`, `veterinar_id`, `datum`, `vreme`, `opis`, `status`) VALUES
(26, 9, 1, '2025-06-25', '19:30:00', 'Test', 'izvršeno'),
(27, 9, 4, '2025-06-25', '11:00:00', 'Test', 'zakazano'),
(28, 17, 14, '2025-06-30', '15:00:00', 'Vakcina', 'izvršeno'),
(29, 17, 1, '2025-07-02', '08:30:00', 'Pregled', 'zakazano'),
(30, 17, 1, '2025-07-03', '19:00:00', 'Test', 'zakazano'),
(31, 18, 1, '2025-07-01', '08:00:00', 'Test', 'izvršeno'),
(32, 18, 3, '2025-07-03', '08:00:00', '', 'izvršeno'),
(33, 18, 2, '2025-06-30', '08:00:00', '', 'odbijeno'),
(34, 18, 1, '2025-06-30', '08:00:00', '', 'odbijeno'),
(35, 18, 3, '2025-06-30', '08:00:00', '', 'odbijeno'),
(36, 17, 14, '2025-07-05', '10:00:00', 'Test', 'izvršeno');

-- --------------------------------------------------------

--
-- Table structure for table `veterinari`
--

CREATE TABLE `veterinari` (
  `veterinar_id` int(11) NOT NULL,
  `ime` varchar(30) NOT NULL,
  `prezime` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `specijalizacija` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `veterinari`
--

INSERT INTO `veterinari` (`veterinar_id`, `ime`, `prezime`, `email`, `specijalizacija`) VALUES
(1, 'Ana', 'Petrović', 'apetrović@gmail.com', 'hirurg'),
(2, 'Marko', 'Jovanović', 'mjovanovic@gmail.com', 'interne bolesti'),
(3, 'Milica', 'Kovač', 'mkovac@gmail.com', 'tehničar'),
(4, 'Lazar', 'Dončić', 'ldoncic@gmail.com', 'psihijatar'),
(14, 'Lazar', 'Pešić', 'lpesic@gmail.com', 'hirurg');

-- --------------------------------------------------------

--
-- Table structure for table `zivotinje`
--

CREATE TABLE `zivotinje` (
  `zivotinja_id` int(11) NOT NULL,
  `korisnik_id` int(11) DEFAULT NULL,
  `vrsta` varchar(30) NOT NULL,
  `rasa` varchar(30) NOT NULL,
  `ime` varchar(30) NOT NULL,
  `datum_rodjenja` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `zivotinje`
--

INSERT INTO `zivotinje` (`zivotinja_id`, `korisnik_id`, `vrsta`, `rasa`, `ime`, `datum_rodjenja`) VALUES
(1, 17, 'pas', 'Malinoa', 'Sloba', '2022-07-11'),
(2, 17, 'Svinja', 'Pijatren', 'Radoje', '2021-06-11'),
(3, 18, 'pas', 'Staford', 'Nora', '2020-09-11');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `istorija_bolesti`
--
ALTER TABLE `istorija_bolesti`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_termin` (`termin_id`),
  ADD KEY `fk_zivotinja` (`zivotinja_id`);

--
-- Indexes for table `korisnici`
--
ALTER TABLE `korisnici`
  ADD PRIMARY KEY (`korisnik_id`);

--
-- Indexes for table `poruke`
--
ALTER TABLE `poruke`
  ADD PRIMARY KEY (`poruka_id`);

--
-- Indexes for table `termini`
--
ALTER TABLE `termini`
  ADD PRIMARY KEY (`termin_id`),
  ADD KEY `korisnik_id` (`korisnik_id`),
  ADD KEY `veterinar_id` (`veterinar_id`);

--
-- Indexes for table `veterinari`
--
ALTER TABLE `veterinari`
  ADD PRIMARY KEY (`veterinar_id`);

--
-- Indexes for table `zivotinje`
--
ALTER TABLE `zivotinje`
  ADD PRIMARY KEY (`zivotinja_id`),
  ADD KEY `korisnik_id` (`korisnik_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `istorija_bolesti`
--
ALTER TABLE `istorija_bolesti`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `korisnici`
--
ALTER TABLE `korisnici`
  MODIFY `korisnik_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `poruke`
--
ALTER TABLE `poruke`
  MODIFY `poruka_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `termini`
--
ALTER TABLE `termini`
  MODIFY `termin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `veterinari`
--
ALTER TABLE `veterinari`
  MODIFY `veterinar_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `zivotinje`
--
ALTER TABLE `zivotinje`
  MODIFY `zivotinja_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `istorija_bolesti`
--
ALTER TABLE `istorija_bolesti`
  ADD CONSTRAINT `fk_termin` FOREIGN KEY (`termin_id`) REFERENCES `termini` (`termin_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_zivotinja` FOREIGN KEY (`zivotinja_id`) REFERENCES `zivotinje` (`zivotinja_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `termini`
--
ALTER TABLE `termini`
  ADD CONSTRAINT `termini_ibfk_1` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnici` (`korisnik_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `termini_ibfk_2` FOREIGN KEY (`veterinar_id`) REFERENCES `veterinari` (`veterinar_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `zivotinje`
--
ALTER TABLE `zivotinje`
  ADD CONSTRAINT `zivotinje_ibfk_1` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnici` (`korisnik_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
