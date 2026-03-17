-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: banque
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `compte_bancaire`
--

DROP TABLE IF EXISTS `compte_bancaire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compte_bancaire` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login_id` int NOT NULL,
  `numero_compte` varchar(50) NOT NULL,
  `solde` decimal(10,2) NOT NULL DEFAULT '0.00',
  `date_creation` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `login_id` (`login_id`),
  CONSTRAINT `compte_bancaire_ibfk_1` FOREIGN KEY (`login_id`) REFERENCES `login` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compte_bancaire`
--

LOCK TABLES `compte_bancaire` WRITE;
/*!40000 ALTER TABLE `compte_bancaire` DISABLE KEYS */;
INSERT INTO `compte_bancaire` VALUES (1,1,'FR4962003789962637',9600.00,'2026-03-17 08:45:17'),(2,3,'FR5480164051298386',200.00,'2026-03-17 14:19:53');
/*!40000 ALTER TABLE `compte_bancaire` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Nom` varchar(250) NOT NULL,
  `Prenom` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `MDP` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (1,'John','Doe','john.doe@example.com','$2b$12$1pPyoHm6EQ1fQuESs6Xtp.CxJHlT6T0IBHKbEBdUHjVGJC0Ai3Qcy'),(3,'Test','TEST','Test.TEST@example.com','$2b$12$0VTbsG3RhLDj/K58jNtJ5.8OWRUCEOzj/uppct4OlxJydmORtO6Zi');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(20) DEFAULT NULL,
  `description` text,
  `expediteur_id` int DEFAULT NULL,
  `receveur_id` int DEFAULT NULL,
  `montant` decimal(10,0) DEFAULT NULL,
  `date` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
INSERT INTO `transaction` VALUES (3,'depot','',1,1,100,'17/03/2026'),(4,'retrait','',1,1,100,'0.002796972688055281'),(5,'retrait','',1,1,100,'17/03/2026'),(6,'retrait','',1,1,100,'17/03/2026'),(7,'retrait','',1,1,100,'17/03/2026'),(8,'retrait','',1,1,100,'17/03/2026'),(9,'retrait','',1,1,100,'17/03/2026'),(10,'retrait','',1,1,100,'17/03/2026'),(11,'retrait','',1,1,100,'17/03/2026'),(12,'retrait','',1,1,100,'17/03/2026'),(13,'depot','',1,1,10000,'17/03/2026'),(14,'transfert','',1,2,200,'17/03/2026');
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-17 15:05:20
