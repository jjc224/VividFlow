/*
Vivid DB
Version: 1
Author: Thomas Nixon
Last update: 02/06/2016
*/

DROP DATABASE IF EXISTS vivid;

CREATE DATABASE vivid;
USE vivid;

CREATE TABLE `user` (
	`id` int(11) AUTO_INCREMENT PRIMARY KEY,
	`username` varchar(255),
	`password` varchar(255),
	`logged_in` boolean,
	`disabled` boolean,
	`jsonstr` mediumtext,
    UNIQUE (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `algorithm` (
	`id` int(11) AUTO_INCREMENT PRIMARY KEY,
	`name` varchar(255),
	`version` int(11),
	`userid` int(11),
	`jsonstr` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `module` (
	`modversionid` int(11) AUTO_INCREMENT PRIMARY KEY,
	`moduleversionstate` varchar(255),
	`name` varchar(255),
	`version` int(11),
	`userid` int(11),
	`moduleid` int(11),
	`jsonstr` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `scheduled_tasks`;
CREATE TABLE IF NOT EXISTS `scheduled_tasks` (
    `scheduledtaskid` int(11) NOT NULL AUTO_INCREMENT,
    `algorithmid` int(11) DEFAULT '0',
    `taskstatus` varchar(50) DEFAULT NULL,
    `jsonstr` mediumtext,
    PRIMARY KEY (`scheduledtaskid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `resource` (
    `id` int(11) AUTO_INCREMENT PRIMARY KEY,
    `filename` varchar(255) DEFAULT NULL,
    `resource_name` varchar(255) DEFAULT NULL,
    `file_type` varchar(255) DEFAULT NULL,
    `user_id` int(11) DEFAULT NULL,
    `deleted` boolean DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
