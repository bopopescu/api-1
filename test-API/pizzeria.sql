-- MySQL dump 10.16  Distrib 10.3.8-MariaDB, for osx10.13 (x86_64)
--
-- Host: localhost    Database: pizzeria
-- ------------------------------------------------------
-- Server version	10.3.8-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ingredient`
--

DROP TABLE IF EXISTS `ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ingredient` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredient`
--

LOCK TABLES `ingredient` WRITE;
/*!40000 ALTER TABLE `ingredient` DISABLE KEYS */;
INSERT INTO `ingredient` VALUES (1,'carotte'),(3,'brocoli'),(4,'petit pois'),(5,'epinards'),(6,'fromage'),(7,'tomate'),(8,'viande hache'),(9,'oignon'),(10,'poivron rouge'),(11,'poivron vert'),(12,'poivron jaune'),(13,'radis'),(14,'oeuf'),(15,'jambon'),(16,'lardon'),(17,'pomme'),(18,'banane'),(19,'ananas'),(20,'menthe'),(21,'persil'),(22,'basilic'),(23,'ciboulette'),(24,'sel'),(25,'poivre'),(26,'salade'),(27,'Mash'),(28,'laitue'),(29,'curcuma'),(30,'patate'),(31,'creme'),(32,'reblochon'),(33,'patate douce'),(34,'celeri'),(35,'salsifi'),(36,'cafard'),(37,'blate'),(38,'termite');
/*!40000 ALTER TABLE `ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pizza`
--

DROP TABLE IF EXISTS `pizza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pizza` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `sexe` char(1) DEFAULT NULL,
  `address` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `comments` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizza`
--

LOCK TABLES `pizza` WRITE;
/*!40000 ALTER TABLE `pizza` DISABLE KEYS */;
INSERT INTO `pizza` VALUES (1,'Adrien','M','10 rue paradis','00.00.00.00.00','j\'adore la pizza'),(2,'Adrien','M','10 rue paradis','00.00.00.00.00','j\'adore la pizza'),(3,'Adrien','M','10 rue paradis','00.00.00.00.00','j\'adore la pizza'),(4,'Adrien','M','10 rue paradis','00.00.00.00.00','j\'adore la pizza'),(5,'Adrien','M','10 rue paradis','00.00.00.00.00','j\'adore la pizza'),(6,'Batman','M','55 rue du chauve qui sourit','top secret','une pizza aux insectes');
/*!40000 ALTER TABLE `pizza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pizza_ingredient`
--

DROP TABLE IF EXISTS `pizza_ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pizza_ingredient` (
  `pizza` smallint(5) unsigned NOT NULL,
  `ingredient` smallint(5) unsigned NOT NULL,
  KEY `fk_pizza_id` (`pizza`),
  KEY `fk_ingreident_id` (`ingredient`),
  CONSTRAINT `fk_ingreident_id` FOREIGN KEY (`ingredient`) REFERENCES `ingredient` (`id`),
  CONSTRAINT `fk_pizza_id` FOREIGN KEY (`pizza`) REFERENCES `pizza` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pizza_ingredient`
--

LOCK TABLES `pizza_ingredient` WRITE;
/*!40000 ALTER TABLE `pizza_ingredient` DISABLE KEYS */;
INSERT INTO `pizza_ingredient` VALUES (3,29),(3,30),(3,31),(3,32),(4,29),(4,30),(4,31),(4,32),(5,33),(5,34),(5,35),(5,1),(5,24),(5,25),(5,7),(6,36),(6,37),(6,38);
/*!40000 ALTER TABLE `pizza_ingredient` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-18 15:16:14
