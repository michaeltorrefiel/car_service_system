-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: car_service
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `mechanic_id` int NOT NULL,
  `customer_id` int NOT NULL,
  `plate_number` varchar(9) NOT NULL,
  `date_time_of_service` datetime NOT NULL,
  `payment` decimal(10,0) NOT NULL,
  PRIMARY KEY (`booking_id`,`mechanic_id`,`customer_id`),
  KEY `fk_Bookings_Customers1_idx` (`customer_id`),
  KEY `fk_Bookings_Mechanics1_idx` (`mechanic_id`),
  KEY `fk_Bookings_Cars1_idx` (`plate_number`),
  CONSTRAINT `fk_Bookings_Cars1` FOREIGN KEY (`plate_number`) REFERENCES `cars` (`plate_number`),
  CONSTRAINT `fk_Bookings_Customers1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  CONSTRAINT `fk_Bookings_Mechanics1` FOREIGN KEY (`mechanic_id`) REFERENCES `mechanics` (`mechanic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (1,1,1,'ABC1234','2024-12-01 09:00:00',5000),(2,2,2,'DEF5678','2024-12-01 10:00:00',4500),(3,3,3,'GHI9012','2024-12-02 11:00:00',5200),(4,4,4,'JKL3456','2024-12-02 13:00:00',4800),(5,5,5,'MNO7890','2024-12-03 14:00:00',5500),(6,6,6,'PQR1235','2024-12-03 15:00:00',4600),(7,7,7,'STU6789','2024-12-04 09:30:00',4700),(8,8,8,'VWX9013','2024-12-04 11:30:00',4200),(9,9,9,'YZA3457','2024-12-05 13:00:00',4800),(10,10,10,'BCD7891','2024-12-05 14:30:00',5000),(11,11,11,'EFG1236','2024-12-06 09:00:00',6000),(12,12,12,'HIJ5670','2024-12-06 10:30:00',7000),(13,13,13,'KLM9014','2024-12-07 12:00:00',5300),(14,14,14,'NOP3458','2024-12-07 13:30:00',5600),(15,15,15,'QRS7892','2024-12-08 10:00:00',8000),(16,16,16,'TUV1237','2024-12-08 11:00:00',4000),(17,17,17,'WXY5671','2024-12-09 12:00:00',3800),(18,18,18,'ZAB9015','2024-12-09 14:00:00',7500),(19,19,19,'CDE3459','2024-12-10 09:00:00',6500),(20,20,20,'FGH7893','2024-12-10 11:00:00',4300),(21,21,21,'IJK1238','2024-12-11 10:30:00',3900),(22,22,22,'LMN5672','2024-12-11 12:30:00',4700),(23,23,23,'OPQ9016','2024-12-12 13:00:00',5200),(24,24,24,'RST3460','2024-12-12 14:00:00',4800),(25,25,25,'UVW7894','2024-12-13 09:30:00',5400);
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cars`
--

DROP TABLE IF EXISTS `cars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cars` (
  `plate_number` varchar(9) NOT NULL,
  `customer_id` int NOT NULL,
  `manufacturer` varchar(50) NOT NULL,
  `model` varchar(50) NOT NULL,
  `known_issue` mediumtext,
  `other_details` tinytext,
  PRIMARY KEY (`plate_number`,`customer_id`),
  KEY `fk_Cars_Customers1_idx` (`customer_id`),
  CONSTRAINT `fk_Cars_Customers1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cars`
--

LOCK TABLES `cars` WRITE;
/*!40000 ALTER TABLE `cars` DISABLE KEYS */;
INSERT INTO `cars` VALUES ('ABC1234',1,'Toyota','Corolla','Brake failure','Red color'),('BCD7891',10,'Volkswagen','Golf','Engine stalling','Silver color'),('CDE3459',19,'Land Rover','Discovery','Fuel injector failure','Gray color'),('DEF5678',2,'Honda','Civic','Battery issues','Blue color'),('EFG1236',11,'BMW','3 Series','Coolant leak','Black color'),('FGH7893',20,'Mitsubishi','Lancer','Air filter clogging','Red color'),('GHI9012',3,'Ford','Focus','Overheating engine','Silver color'),('HIJ5670',12,'Mercedes-Benz','C-Class','Oil consumption','White color'),('IJK1238',21,'Suzuki','Swift','Ignition issues','Blue color'),('JKL3456',4,'Nissan','Altima','Suspension noise','Black color'),('KLM9014',13,'Audi','A4','Electrical issues','Gray color'),('LMN5672',22,'Peugeot','308','Brake light failure','Green color'),('MNO7890',5,'Mazda','3','Air conditioning malfunction','White color'),('NOP3458',14,'Lexus','IS','Brake noise','Red color'),('OPQ9016',23,'Fiat','500','Cooling fan failure','Silver color'),('PQR1235',6,'Hyundai','Elantra','Transmission issues','Gray color'),('QRS7892',15,'Tesla','Model 3','Software malfunction','Blue color'),('RST3460',24,'Jeep','Wrangler','Starter motor issues','Black color'),('STU6789',7,'Chevrolet','Malibu','Steering problems','Red color'),('TUV1237',16,'Volvo','S60','Transmission fluid leak','Silver color'),('UVW7894',25,'Chrysler','300','Exhaust leak','White color'),('VWX9013',8,'Kia','Forte','Tire wear','Blue color'),('WXY5671',17,'Jaguar','XE','Tire pressure problems','Black color'),('YZA3457',9,'Subaru','Impreza','Fuel pump failure','Green color'),('ZAB9015',18,'Porsche','Cayman','Suspension alignment','White color');
/*!40000 ALTER TABLE `cars` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `contact_number` varchar(11) NOT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'John','Smith','09171234568'),(2,'Jane','Doe','09181234568'),(3,'Michael','Johnson','09192234568'),(4,'Emily','Davis','09173214568'),(5,'Chris','Brown','09184214568'),(6,'Anna','Wilson','09195214568'),(7,'Paul','Taylor','09176234568'),(8,'Sofia','Anderson','09187234568'),(9,'David','Thomas','09198234568'),(10,'Ella','Jackson','09179234568'),(11,'Mark','White','09181324568'),(12,'Grace','Harris','09192324568'),(13,'Luke','Martin','09173324568'),(14,'Zoe','Thompson','09184324568'),(15,'Liam','Moore','09195324568'),(16,'Mia','Young','09176324568'),(17,'Noah','Lee','09187324568'),(18,'Chloe','Walker','09198324568'),(19,'James','Hall','09179324568'),(20,'Ruby','Allen','09181424568'),(21,'Oscar','King','09192424568'),(22,'Lily','Scott','09173424568'),(23,'Jack','Green','09184424568'),(24,'Ava','Adams','09195424568'),(25,'Ethan','Baker','09176424568');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mechanics`
--

DROP TABLE IF EXISTS `mechanics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mechanics` (
  `mechanic_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `contact_number` varchar(11) NOT NULL,
  `other_mechanic_details` tinytext,
  PRIMARY KEY (`mechanic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mechanics`
--

LOCK TABLES `mechanics` WRITE;
/*!40000 ALTER TABLE `mechanics` DISABLE KEYS */;
INSERT INTO `mechanics` VALUES (1,'Juan','Dela Cruz','09171234567','Experienced with SUVs'),(2,'Pedro','Santos','09181234567','Specializes in engine repair'),(3,'Maria','Reyes','09192234567','Expert in luxury cars'),(4,'Jose','Garcia','09173214567','Electrical systems specialist'),(5,'Ana','Lopez','09184214567','Certified for hybrid vehicles'),(6,'Carlos','Martinez','09195214567','Brake systems expert'),(7,'Miguel','Torres','09176234567','Suspension specialist'),(8,'Sophia','Gomez','09187234567','Bodywork and painting'),(9,'Luis','Hernandez','09198234567','Expert in Japanese cars'),(10,'Elena','Perez','09179234567','Experienced with manual transmissions'),(11,'Fernando','Castro','09181324567','Air conditioning repair'),(12,'Carmen','Flores','09192324567','Engine diagnostics specialist'),(13,'Jorge','Morales','09173324567','Certified diesel mechanic'),(14,'Isabella','Ramos','09184324567','Oil and fluid systems'),(15,'Ricardo','Diaz','09195324567','Transmission systems'),(16,'Teresa','Ortiz','09176324567','General repairs'),(17,'Adrian','Vargas','09187324567','Welding and fabrication'),(18,'Lucia','Ramirez','09198324567','Inspection specialist'),(19,'Pablo','Chavez','09179324567','European car expert'),(20,'Diana','Jimenez','09181424567','Interior systems'),(21,'Victor','Silva','09192424567','Battery and charging systems'),(22,'Clara','Ruiz','09173424567','Off-road vehicle expert'),(23,'Gabriel','Mendoza','09184424567','Tire and alignment expert'),(24,'Daniel','Vega','09195424567','Hydraulics specialist'),(25,'Laura','Gutierrez','09176424567','Vintage car restoration');
/*!40000 ALTER TABLE `mechanics` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-14 20:35:39
