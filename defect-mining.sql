/*
 Navicat MySQL Data Transfer

 Source Server         : 192.168.0.103
 Source Server Type    : MySQL
 Source Server Version : 50555
 Source Host           : 192.168.0.103
 Source Database       : defect-mining

 Target Server Type    : MySQL
 Target Server Version : 50555
 File Encoding         : utf-8

 Date: 06/01/2017 05:01:17 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `binarys`
-- ----------------------------
DROP TABLE IF EXISTS `binarys`;
CREATE TABLE `binarys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `binary_name` varchar(255) DEFAULT NULL,
  `file_size` float DEFAULT NULL,
  `upload_datetime` datetime DEFAULT NULL,
  `status` int(255) DEFAULT NULL,
  `update_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

SET FOREIGN_KEY_CHECKS = 1;
