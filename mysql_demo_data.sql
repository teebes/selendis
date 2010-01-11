-- MySQL dump 10.13  Distrib 5.1.37, for apple-darwin9.5.0 (i386)
--
-- Host: localhost    Database: stark
-- ------------------------------------------------------
-- Server version	5.1.37

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
-- Table structure for table `accounts_emailconfirmation`
--

DROP TABLE IF EXISTS `accounts_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `key` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_emailconfirmation_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_emailconfirmation`
--

LOCK TABLES `accounts_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `accounts_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anima_message`
--

DROP TABLE IF EXISTS `anima_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anima_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `type` varchar(20) NOT NULL,
  `content` text NOT NULL,
  `destination` varchar(40) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `anima_message_content_type_id` (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anima_message`
--

LOCK TABLES `anima_message` WRITE;
/*!40000 ALTER TABLE `anima_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `anima_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anima_mob`
--

DROP TABLE IF EXISTS `anima_mob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anima_mob` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `room_id` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  `experience` int(11) NOT NULL,
  `next_level` int(11) NOT NULL,
  `description` text NOT NULL,
  `hp` int(11) NOT NULL,
  `max_hp` int(11) NOT NULL,
  `mp` int(11) NOT NULL,
  `max_mp` int(11) NOT NULL,
  `sp` int(11) NOT NULL,
  `max_sp` int(11) NOT NULL,
  `strength` int(11) NOT NULL,
  `agility` int(11) NOT NULL,
  `constitution` int(11) NOT NULL,
  `main_hand_id` int(11) DEFAULT NULL,
  `head_id` int(11) DEFAULT NULL,
  `chest_id` int(11) DEFAULT NULL,
  `arms_id` int(11) DEFAULT NULL,
  `hands_id` int(11) DEFAULT NULL,
  `legs_id` int(11) DEFAULT NULL,
  `feet_id` int(11) DEFAULT NULL,
  `target_type_id` int(11) DEFAULT NULL,
  `target_id` int(10) unsigned DEFAULT NULL,
  `static` tinyint(1) NOT NULL,
  `template` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `anima_mob_room_id` (`room_id`),
  KEY `anima_mob_main_hand_id` (`main_hand_id`),
  KEY `anima_mob_head_id` (`head_id`),
  KEY `anima_mob_chest_id` (`chest_id`),
  KEY `anima_mob_arms_id` (`arms_id`),
  KEY `anima_mob_hands_id` (`hands_id`),
  KEY `anima_mob_legs_id` (`legs_id`),
  KEY `anima_mob_feet_id` (`feet_id`),
  KEY `anima_mob_target_type_id` (`target_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anima_mob`
--

LOCK TABLES `anima_mob` WRITE;
/*!40000 ALTER TABLE `anima_mob` DISABLE KEYS */;
INSERT INTO `anima_mob` VALUES (1,'a tired guard',1,1,10,1,'',10,10,10,10,10,10,10,10,10,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,1);
/*!40000 ALTER TABLE `anima_mob` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anima_mobloader`
--

DROP TABLE IF EXISTS `anima_mobloader`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anima_mobloader` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `batch_size` int(11) NOT NULL,
  `spawn_chance` int(11) NOT NULL,
  `zone_limit` int(11) NOT NULL,
  `template_mob_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `anima_mobloader_template_mob_id` (`template_mob_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anima_mobloader`
--

LOCK TABLES `anima_mobloader` WRITE;
/*!40000 ALTER TABLE `anima_mobloader` DISABLE KEYS */;
/*!40000 ALTER TABLE `anima_mobloader` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anima_mobloader_armor`
--

DROP TABLE IF EXISTS `anima_mobloader_armor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anima_mobloader_armor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mobloader_id` int(11) NOT NULL,
  `armor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobloader_id` (`mobloader_id`,`armor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anima_mobloader_armor`
--

LOCK TABLES `anima_mobloader_armor` WRITE;
/*!40000 ALTER TABLE `anima_mobloader_armor` DISABLE KEYS */;
/*!40000 ALTER TABLE `anima_mobloader_armor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anima_mobloader_misc`
--

DROP TABLE IF EXISTS `anima_mobloader_misc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anima_mobloader_misc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mobloader_id` int(11) NOT NULL,
  `misc_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobloader_id` (`mobloader_id`,`misc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anima_mobloader_misc`
--

LOCK TABLES `anima_mobloader_misc` WRITE;
/*!40000 ALTER TABLE `anima_mobloader_misc` DISABLE KEYS */;
/*!40000 ALTER TABLE `anima_mobloader_misc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anima_mobloader_spawn_in`
--

DROP TABLE IF EXISTS `anima_mobloader_spawn_in`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anima_mobloader_spawn_in` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mobloader_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobloader_id` (`mobloader_id`,`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anima_mobloader_spawn_in`
--

LOCK TABLES `anima_mobloader_spawn_in` WRITE;
/*!40000 ALTER TABLE `anima_mobloader_spawn_in` DISABLE KEYS */;
/*!40000 ALTER TABLE `anima_mobloader_spawn_in` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anima_mobloader_spawned_mobs`
--

DROP TABLE IF EXISTS `anima_mobloader_spawned_mobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anima_mobloader_spawned_mobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mobloader_id` int(11) NOT NULL,
  `mob_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobloader_id` (`mobloader_id`,`mob_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anima_mobloader_spawned_mobs`
--

LOCK TABLES `anima_mobloader_spawned_mobs` WRITE;
/*!40000 ALTER TABLE `anima_mobloader_spawned_mobs` DISABLE KEYS */;
/*!40000 ALTER TABLE `anima_mobloader_spawned_mobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anima_mobloader_sustenance`
--

DROP TABLE IF EXISTS `anima_mobloader_sustenance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anima_mobloader_sustenance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mobloader_id` int(11) NOT NULL,
  `sustenance_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobloader_id` (`mobloader_id`,`sustenance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anima_mobloader_sustenance`
--

LOCK TABLES `anima_mobloader_sustenance` WRITE;
/*!40000 ALTER TABLE `anima_mobloader_sustenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `anima_mobloader_sustenance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anima_mobloader_weapon`
--

DROP TABLE IF EXISTS `anima_mobloader_weapon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anima_mobloader_weapon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mobloader_id` int(11) NOT NULL,
  `weapon_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobloader_id` (`mobloader_id`,`weapon_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anima_mobloader_weapon`
--

LOCK TABLES `anima_mobloader_weapon` WRITE;
/*!40000 ALTER TABLE `anima_mobloader_weapon` DISABLE KEYS */;
/*!40000 ALTER TABLE `anima_mobloader_weapon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anima_player`
--

DROP TABLE IF EXISTS `anima_player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anima_player` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `room_id` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  `experience` int(11) NOT NULL,
  `next_level` int(11) NOT NULL,
  `description` text NOT NULL,
  `hp` int(11) NOT NULL,
  `max_hp` int(11) NOT NULL,
  `mp` int(11) NOT NULL,
  `max_mp` int(11) NOT NULL,
  `sp` int(11) NOT NULL,
  `max_sp` int(11) NOT NULL,
  `strength` int(11) NOT NULL,
  `agility` int(11) NOT NULL,
  `constitution` int(11) NOT NULL,
  `main_hand_id` int(11) DEFAULT NULL,
  `head_id` int(11) DEFAULT NULL,
  `chest_id` int(11) DEFAULT NULL,
  `arms_id` int(11) DEFAULT NULL,
  `hands_id` int(11) DEFAULT NULL,
  `legs_id` int(11) DEFAULT NULL,
  `feet_id` int(11) DEFAULT NULL,
  `target_type_id` int(11) DEFAULT NULL,
  `target_id` int(10) unsigned DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `builder_mode` tinyint(1) NOT NULL,
  `temporary` tinyint(1) NOT NULL,
  `status` varchar(20) NOT NULL,
  `last_activity` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `anima_player_room_id` (`room_id`),
  KEY `anima_player_main_hand_id` (`main_hand_id`),
  KEY `anima_player_head_id` (`head_id`),
  KEY `anima_player_chest_id` (`chest_id`),
  KEY `anima_player_arms_id` (`arms_id`),
  KEY `anima_player_hands_id` (`hands_id`),
  KEY `anima_player_legs_id` (`legs_id`),
  KEY `anima_player_feet_id` (`feet_id`),
  KEY `anima_player_target_type_id` (`target_type_id`),
  KEY `anima_player_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anima_player`
--

LOCK TABLES `anima_player` WRITE;
/*!40000 ALTER TABLE `anima_player` DISABLE KEYS */;
INSERT INTO `anima_player` VALUES (3,'teebes',2,1,1,1,'',10,10,30,30,10,10,10,10,10,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0,'logged_in','2010-01-10 19:06:11');
/*!40000 ALTER TABLE `anima_player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id` (`content_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add message',4,'add_message'),(11,'Can change message',4,'change_message'),(12,'Can delete message',4,'delete_message'),(13,'Can add log entry',5,'add_logentry'),(14,'Can change log entry',5,'change_logentry'),(15,'Can delete log entry',5,'delete_logentry'),(16,'Can add content type',6,'add_contenttype'),(17,'Can change content type',6,'change_contenttype'),(18,'Can delete content type',6,'delete_contenttype'),(19,'Can add session',7,'add_session'),(20,'Can change session',7,'change_session'),(21,'Can delete session',7,'delete_session'),(22,'Can add site',8,'add_site'),(23,'Can change site',8,'change_site'),(24,'Can delete site',8,'delete_site'),(25,'Can add email confirmation',9,'add_emailconfirmation'),(26,'Can change email confirmation',9,'change_emailconfirmation'),(27,'Can delete email confirmation',9,'delete_emailconfirmation'),(28,'Can add player',10,'add_player'),(29,'Can change player',10,'change_player'),(30,'Can delete player',10,'delete_player'),(31,'Can add mob',11,'add_mob'),(32,'Can change mob',11,'change_mob'),(33,'Can delete mob',11,'delete_mob'),(34,'Can add mob loader',12,'add_mobloader'),(35,'Can change mob loader',12,'change_mobloader'),(36,'Can delete mob loader',12,'delete_mobloader'),(37,'Can add message',13,'add_message'),(38,'Can change message',13,'change_message'),(39,'Can delete message',13,'delete_message'),(40,'Can add zone',14,'add_zone'),(41,'Can change zone',14,'change_zone'),(42,'Can delete zone',14,'delete_zone'),(43,'Can add room connector',15,'add_roomconnector'),(44,'Can change room connector',15,'change_roomconnector'),(45,'Can delete room connector',15,'delete_roomconnector'),(46,'Can add room',16,'add_room'),(47,'Can change room',16,'change_room'),(48,'Can delete room',16,'delete_room'),(49,'Can add weapon',17,'add_weapon'),(50,'Can change weapon',17,'change_weapon'),(51,'Can delete weapon',17,'delete_weapon'),(52,'Can add equipment',18,'add_equipment'),(53,'Can change equipment',18,'change_equipment'),(54,'Can delete equipment',18,'delete_equipment'),(55,'Can add armor',19,'add_armor'),(56,'Can change armor',19,'change_armor'),(57,'Can delete armor',19,'delete_armor'),(58,'Can add sustenance',20,'add_sustenance'),(59,'Can change sustenance',20,'change_sustenance'),(60,'Can delete sustenance',20,'delete_sustenance'),(61,'Can add misc',21,'add_misc'),(62,'Can change misc',21,'change_misc'),(63,'Can delete misc',21,'delete_misc'),(64,'Can add item instance',22,'add_iteminstance'),(65,'Can change item instance',22,'change_iteminstance'),(66,'Can delete item instance',22,'delete_iteminstance');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'teebes','','','teebes@gmail.com','sha1$363fe$72ba9f2101443ec38968b3f7174ee4feb044dc88',1,1,1,'2010-01-10 19:02:09','2010-01-10 18:12:52');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` text,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_user_id` (`user_id`),
  KEY `django_admin_log_content_type_id` (`content_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2010-01-10 19:06:45',1,3,'2','user_2',3,''),(2,'2010-01-10 19:06:45',1,3,'3','user_3',3,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'message','auth','message'),(5,'log entry','admin','logentry'),(6,'content type','contenttypes','contenttype'),(7,'session','sessions','session'),(8,'site','sites','site'),(9,'email confirmation','accounts','emailconfirmation'),(10,'player','anima','player'),(11,'mob','anima','mob'),(12,'mob loader','anima','mobloader'),(13,'message','anima','message'),(14,'zone','world','zone'),(15,'room connector','world','roomconnector'),(16,'room','world','room'),(17,'weapon','world','weapon'),(18,'equipment','world','equipment'),(19,'armor','world','armor'),(20,'sustenance','world','sustenance'),(21,'misc','world','misc'),(22,'item instance','world','iteminstance');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` text NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('36f51f2d68fb85970ca9ed266324c501','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwN1LjkwNzRmMDYwOTE3YjY0ODJiNWJl\nOTk1MDE3MzRlYzk3\n','2010-01-24 18:50:46'),('fcde9dfcaa653031199bef70566db12f','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LmMwMTFlNTBmZjhmZTNkZGU5MTI4\nYzgwNjJkMTdhM2Qw\n','2010-01-24 18:26:32'),('fd1dbc05ad3757c77386cb15a02e47e2','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LmMwMTFlNTBmZjhmZTNkZGU5MTI4\nYzgwNjJkMTdhM2Qw\n','2010-01-24 19:02:09');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `world_armor`
--

DROP TABLE IF EXISTS `world_armor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `world_armor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `capacity` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `weight` decimal(10,0) NOT NULL,
  `slot` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `world_armor`
--

LOCK TABLES `world_armor` WRITE;
/*!40000 ALTER TABLE `world_armor` DISABLE KEYS */;
INSERT INTO `world_armor` VALUES (1,0,'an old leather helmet','3','head'),(2,0,'an old leather breastplate','7','chest'),(3,0,'a pair of rugged leather boots','2','feet'),(4,0,'a pair of dark leather gloves','1','hands'),(5,0,'a pair of light leather pants','2','feet');
/*!40000 ALTER TABLE `world_armor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `world_equipment`
--

DROP TABLE IF EXISTS `world_equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `world_equipment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `capacity` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `weight` decimal(10,0) NOT NULL,
  `slot` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `world_equipment`
--

LOCK TABLES `world_equipment` WRITE;
/*!40000 ALTER TABLE `world_equipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `world_equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `world_iteminstance`
--

DROP TABLE IF EXISTS `world_iteminstance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `world_iteminstance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `owner_type_id` int(11) NOT NULL,
  `owner_id` int(10) unsigned NOT NULL,
  `base_type_id` int(11) NOT NULL,
  `base_id` int(10) unsigned NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `world_iteminstance_owner_type_id` (`owner_type_id`),
  KEY `world_iteminstance_base_type_id` (`base_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `world_iteminstance`
--

LOCK TABLES `world_iteminstance` WRITE;
/*!40000 ALTER TABLE `world_iteminstance` DISABLE KEYS */;
/*!40000 ALTER TABLE `world_iteminstance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `world_misc`
--

DROP TABLE IF EXISTS `world_misc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `world_misc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `capacity` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `weight` decimal(10,0) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `world_misc`
--

LOCK TABLES `world_misc` WRITE;
/*!40000 ALTER TABLE `world_misc` DISABLE KEYS */;
INSERT INTO `world_misc` VALUES (1,1000,'a corpse','100');
/*!40000 ALTER TABLE `world_misc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `world_room`
--

DROP TABLE IF EXISTS `world_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `world_room` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `zone_id` int(11) NOT NULL,
  `xpos` int(11) NOT NULL,
  `ypos` int(11) NOT NULL,
  `name` varchar(80) NOT NULL,
  `description` text NOT NULL,
  `type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `world_room_zone_id` (`zone_id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `world_room`
--

LOCK TABLES `world_room` WRITE;
/*!40000 ALTER TABLE `world_room` DISABLE KEYS */;
INSERT INTO `world_room` VALUES (1,1,0,0,'The Void','You barely exist.','hidden'),(2,1,0,-1,'Center of the World','The center of the world.','city'),(3,1,1,-1,'Eastern terrace','Just to the east of the center of the world.','city'),(4,1,0,-2,'The northern path','A small path that leaves the center of the world, going north.','city'),(5,1,-1,-1,'The inn','Just to the west of the center of the world','shop'),(7,1,2,-2,'The armory','','shop'),(12,1,0,-3,'Intersection','','city'),(13,1,1,-3,'Outside merchant row','','city'),(14,1,-1,-3,'A well-lit street','','city'),(15,1,-2,-3,'Bend in the road','','city'),(16,1,-2,-2,'Inside the western gate','This is outisde the western gate','city'),(17,1,-2,-1,'South of the western gate','','city'),(18,1,-2,0,'Along the western wall','','city'),(19,1,-2,1,'Outside the cheese shop','','city'),(20,1,-2,2,'Bend in the road','','city'),(21,1,-1,2,'Along the southern wall','','city'),(22,1,-1,1,'The cheese shop','','shop'),(23,1,2,-3,'Merchant row','','city'),(24,1,3,-3,'Merchant row','','city'),(25,1,4,-3,'North-East corner of the city','','city'),(26,1,4,-2,'A quiet street','','city'),(27,1,4,-1,'A dark, shady street','','city'),(28,1,4,0,'A dark, shady street','','city'),(29,1,4,1,'A deserted plaza','','city'),(30,1,4,2,'South-East corner of the city','','city'),(31,1,3,2,'A small street','','city'),(32,1,2,2,'East of the southern gate','','city'),(33,1,1,2,'The southern gate','','city'),(34,1,0,2,'West of the southern gate','','city'),(35,1,-3,-2,'Outisde the western gate','','road'),(36,1,-4,-2,'Intersection in the road','','road'),(37,1,-3,-3,'Green fields by the road','','field'),(38,1,-3,-4,'Entrance to a dense forest','','field'),(39,1,-4,-3,'Green fields by the road','','field'),(40,1,-5,-3,'A small farm','','field'),(41,1,-5,-2,'Road outside the farm','','road'),(42,1,-6,-2,'Northern bend in the road','','road'),(43,1,-6,-1,'Southern bend in the road','','road'),(44,1,-7,-1,'A dusty road','','road'),(45,1,-8,-1,'End of the world','','road'),(46,1,-4,-1,'Beginning of a small dirt road','','road'),(47,1,-4,0,'Along a small dirt road','','road'),(52,1,-2,3,'Bend before the river','','road'),(53,1,-1,3,'Outside the city walls','','road'),(54,1,0,3,'On a small path','','road'),(55,1,1,3,'Outside the southern gate','','road'),(56,1,1,4,'Before the river','','road'),(57,1,1,5,'On a bridge over the river','','road'),(58,1,2,5,'Untitled room','','water'),(59,1,3,5,'Untitled room','','water'),(60,1,4,5,'Untitled room','','water'),(61,1,5,5,'Untitled room','','water'),(62,1,0,5,'Untitled room','','water'),(63,1,-1,5,'Untitled room','','water'),(64,1,-2,5,'Untitled room','','water'),(65,1,-3,5,'Untitled room','','water'),(66,1,-4,5,'Untitled room','','water'),(67,1,-5,5,'Untitled room','','water'),(68,1,-6,5,'Untitled room','','water'),(69,1,-7,5,'Untitled room','','water'),(70,1,-8,5,'Untitled room','','water'),(71,1,1,6,'Down the dusty road','','road'),(72,1,1,7,'The end of the world','','road'),(73,1,-4,2,'Untitled room','','road'),(74,1,-4,3,'Untitled room','','road'),(75,1,-3,4,'On the river bank','','road'),(76,1,-4,4,'Bend by the river bank','','road'),(77,1,-2,4,'Bend by the river bank','','road'),(78,1,-4,1,'Untitled room','','road'),(79,1,0,-4,'Cul de sac','','city'),(80,1,2,4,'The Idle Room','If you are here it\'s because you\'ve been idle for a while. Go 1w to interact with the world again.','city'),(81,1,3,-2,'The tanner','','shop'),(83,1,2,-4,'The apothecary','','shop'),(84,1,-1,-2,'The Guard Room','','city');
/*!40000 ALTER TABLE `world_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `world_roomconnector`
--

DROP TABLE IF EXISTS `world_roomconnector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `world_roomconnector` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_room_id` int(11) NOT NULL,
  `to_room_id` int(11) NOT NULL,
  `type` varchar(40) NOT NULL,
  `direction` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `world_roomconnector_from_room_id` (`from_room_id`),
  KEY `world_roomconnector_to_room_id` (`to_room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=183 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `world_roomconnector`
--

LOCK TABLES `world_roomconnector` WRITE;
/*!40000 ALTER TABLE `world_roomconnector` DISABLE KEYS */;
INSERT INTO `world_roomconnector` VALUES (10,4,12,'Normal','north'),(11,12,4,'Normal','south'),(12,12,13,'Normal','east'),(13,13,12,'Normal','west'),(14,14,12,'Normal','east'),(15,15,14,'Normal','east'),(16,20,21,'Normal','east'),(17,20,19,'Normal','north'),(18,21,20,'Normal','west'),(19,22,21,'Normal','south'),(20,22,19,'Normal','west'),(21,19,22,'Normal','east'),(22,19,20,'Normal','south'),(23,19,18,'Normal','north'),(24,18,17,'Normal','north'),(25,18,19,'Normal','south'),(26,17,16,'Normal','north'),(27,17,18,'Normal','south'),(28,16,17,'Normal','south'),(29,16,15,'Normal','north'),(30,15,16,'Normal','south'),(31,14,15,'Normal','west'),(32,12,14,'Normal','west'),(33,23,13,'Normal','west'),(34,23,7,'Normal','south'),(36,25,24,'Normal','west'),(37,24,25,'Normal','east'),(38,24,23,'Normal','west'),(39,13,23,'Normal','east'),(40,23,24,'Normal','east'),(41,7,23,'Normal','north'),(42,34,33,'Normal','east'),(43,34,21,'Normal','west'),(44,21,22,'Normal','north'),(45,21,34,'Normal','east'),(46,33,34,'Normal','west'),(47,32,33,'Normal','west'),(48,32,31,'Normal','east'),(49,31,30,'Normal','east'),(50,31,32,'Normal','west'),(51,30,29,'Normal','north'),(52,30,31,'Normal','west'),(53,29,28,'Normal','north'),(54,29,30,'Normal','south'),(55,28,27,'Normal','north'),(56,28,29,'Normal','south'),(57,27,26,'Normal','north'),(58,27,28,'Normal','south'),(59,26,25,'Normal','north'),(60,26,27,'Normal','south'),(61,25,26,'Normal','south'),(62,33,32,'Normal','east'),(63,16,35,'Normal','west'),(64,35,16,'Normal','east'),(65,38,37,'Normal','south'),(66,37,38,'Normal','north'),(67,37,35,'Normal','south'),(68,35,37,'Normal','north'),(69,36,35,'Normal','east'),(70,39,37,'Normal','east'),(71,39,36,'Normal','south'),(72,40,39,'Normal','east'),(73,41,40,'Normal','north'),(74,41,36,'Normal','east'),(75,40,41,'Normal','south'),(76,39,40,'Normal','west'),(77,37,39,'Normal','west'),(78,35,36,'Normal','west'),(79,36,41,'Normal','west'),(80,36,39,'Normal','north'),(81,42,41,'Normal','east'),(82,41,42,'Normal','west'),(83,43,42,'Normal','north'),(84,45,44,'Normal','east'),(85,44,43,'Normal','east'),(86,44,45,'Normal','west'),(87,43,44,'Normal','west'),(88,42,43,'Normal','south'),(89,46,36,'Normal','north'),(90,61,60,'Normal','west'),(91,60,61,'Normal','east'),(92,60,59,'Normal','west'),(93,59,60,'Normal','east'),(94,59,58,'Normal','west'),(95,58,59,'Normal','east'),(96,67,66,'Normal','east'),(97,70,69,'Normal','east'),(98,69,68,'Normal','east'),(99,69,70,'Normal','west'),(100,68,67,'Normal','east'),(101,68,69,'Normal','west'),(102,67,68,'Normal','west'),(103,66,65,'Normal','east'),(104,66,67,'Normal','west'),(105,65,64,'Normal','east'),(106,65,66,'Normal','west'),(107,64,63,'Normal','east'),(108,64,65,'Normal','west'),(109,63,62,'Normal','east'),(110,63,64,'Normal','west'),(111,62,63,'Normal','west'),(112,72,71,'Normal','north'),(113,71,57,'Normal','north'),(114,71,72,'Normal','south'),(115,57,56,'Normal','north'),(116,57,71,'Normal','south'),(117,56,55,'Normal','north'),(118,56,57,'Normal','south'),(119,55,33,'Normal','north'),(120,55,56,'Normal','south'),(121,33,55,'Normal','south'),(122,55,54,'Normal','west'),(123,54,55,'Normal','east'),(124,53,54,'Normal','east'),(125,53,52,'Normal','west'),(126,52,53,'Normal','east'),(137,47,46,'Normal','north'),(138,46,47,'Normal','south'),(139,36,46,'Normal','south'),(140,54,53,'Normal','west'),(142,74,73,'Normal','north'),(146,73,74,'Normal','south'),(147,76,74,'Normal','north'),(148,76,75,'Normal','east'),(149,74,76,'Normal','south'),(150,77,75,'Normal','west'),(151,77,52,'Normal','north'),(152,75,77,'Normal','east'),(153,75,76,'Normal','west'),(154,52,77,'Normal','south'),(155,78,47,'Normal','north'),(156,78,73,'Normal','south'),(157,47,78,'Normal','south'),(158,73,78,'Normal','north'),(159,79,12,'Normal','south'),(160,12,79,'Normal','north'),(162,80,56,'Normal','west'),(163,81,24,'Normal','north'),(164,24,81,'Normal','south'),(165,23,83,'Normal','north'),(166,83,23,'Normal','south'),(173,84,4,'Normal','east'),(174,4,84,'Normal','west'),(176,2,5,'Normal','west'),(177,2,3,'Normal','east'),(178,2,4,'Normal','north'),(180,3,2,'Normal','west'),(181,5,2,'Normal','east'),(182,4,2,'Normal','south');
/*!40000 ALTER TABLE `world_roomconnector` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `world_sustenance`
--

DROP TABLE IF EXISTS `world_sustenance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `world_sustenance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `capacity` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `weight` decimal(10,0) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `world_sustenance`
--

LOCK TABLES `world_sustenance` WRITE;
/*!40000 ALTER TABLE `world_sustenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `world_sustenance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `world_weapon`
--

DROP TABLE IF EXISTS `world_weapon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `world_weapon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `capacity` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `weight` decimal(10,0) NOT NULL,
  `num_dice` int(11) NOT NULL,
  `num_faces` int(11) NOT NULL,
  `weapon_class` varchar(20) NOT NULL,
  `two_handed` tinyint(1) NOT NULL,
  `slot` varchar(40) NOT NULL,
  `hit_first` varchar(20) NOT NULL,
  `hit_third` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `world_weapon`
--

LOCK TABLES `world_weapon` WRITE;
/*!40000 ALTER TABLE `world_weapon` DISABLE KEYS */;
INSERT INTO `world_weapon` VALUES (1,0,'a short dagger','0',2,2,'short_blade',0,'','',''),(2,0,'a wooden stick','0',1,1,'blunt',0,'','',''),(3,0,'a rusty blade','5',2,3,'long_blade',0,'main_hand','',''),(4,0,'a flaming crystal sword','15',20,30,'long_blade',0,'main_hand','','');
/*!40000 ALTER TABLE `world_weapon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `world_zone`
--

DROP TABLE IF EXISTS `world_zone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `world_zone` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `world_zone`
--

LOCK TABLES `world_zone` WRITE;
/*!40000 ALTER TABLE `world_zone` DISABLE KEYS */;
INSERT INTO `world_zone` VALUES (1,'Capital');
/*!40000 ALTER TABLE `world_zone` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-01-10 20:11:25
