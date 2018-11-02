-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 12, 2018 at 09:57 PM
-- Server version: 10.1.35-MariaDB
-- PHP Version: 7.2.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `iot`
--

-- --------------------------------------------------------

--
-- Table structure for table `auto`
--

CREATE TABLE `auto` (
  `id` int(11) NOT NULL,
  `lowh` int(11) NOT NULL DEFAULT '65',
  `mediumh` int(11) NOT NULL DEFAULT '75',
  `highh` int(11) NOT NULL DEFAULT '85',
  `lowt` int(11) NOT NULL,
  `mediumt` int(11) NOT NULL,
  `hight` int(11) NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auto`
--

INSERT INTO `auto` (`id`, `lowh`, `mediumh`, `highh`, `lowt`, `mediumt`, `hight`, `date`) VALUES
(1, 65, 75, 85, 24, 25, 26, '2018-10-02 14:59:00'),
(2, 60, 70, 80, 32, 33, 34, '2018-10-02 16:15:00');

-- --------------------------------------------------------

--
-- Table structure for table `data`
--

CREATE TABLE `data` (
  `id` int(11) NOT NULL,
  `humidity` int(11) NOT NULL,
  `temperature` int(11) NOT NULL,
  `auto_id` int(11) DEFAULT NULL,
  `manual_id` int(11) DEFAULT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `data`
--

INSERT INTO `data` (`id`, `humidity`, `temperature`, `auto_id`, `manual_id`, `date`) VALUES
(1, 70, 33, 1, NULL, '2018-10-02 15:30:00'),
(2, 65, 31, 1, NULL, '2018-10-02 16:00:00'),
(3, 72, 32, 2, NULL, '2018-10-02 16:30:00'),
(4, 69, 33, 2, NULL, '2018-10-02 17:00:00'),
(5, 58, 34, NULL, 1, '2018-10-02 17:30:00'),
(6, 52, 35, NULL, 3, '2018-10-02 18:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `manual`
--

CREATE TABLE `manual` (
  `id` int(11) NOT NULL,
  `speed` varchar(6) DEFAULT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `manual`
--

INSERT INTO `manual` (`id`, `speed`, `date`) VALUES
(1, 'Low', '2018-10-02 17:30:00'),
(2, 'Medium', '2018-10-02 18:00:00'),
(3, 'High', '2018-10-02 18:30:00'),
(4, NULL, '2018-10-02 19:00:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auto`
--
ALTER TABLE `auto`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `data`
--
ALTER TABLE `data`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `information_ibfk_1` (`auto_id`),
  ADD KEY `data_ibfk_2` (`manual_id`);

--
-- Indexes for table `manual`
--
ALTER TABLE `manual`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auto`
--
ALTER TABLE `auto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `data`
--
ALTER TABLE `data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `manual`
--
ALTER TABLE `manual`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `data`
--
ALTER TABLE `data`
  ADD CONSTRAINT `data_ibfk_1` FOREIGN KEY (`auto_id`) REFERENCES `auto` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `data_ibfk_2` FOREIGN KEY (`manual_id`) REFERENCES `manual` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
