
CREATE DATABASE IF NOT EXISTS `real-time-detector`;

USE `real-time-detector`;

CREATE TABLE IF NOT EXISTS `Event`(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    timestamp INT UNSIGNED NOT NULL,
    objectId INT UNSIGNED NOT NULL,
    isInfraction BOOL NOT NULL,
    isDeleted BOOL NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Object`(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar(50) NOT NULL,
    description varchar(200),
    isDeleted BOOL NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `EventObject`(
    eventId INT UNSIGNED NOT NULL,
    objectId INT UNSIGNED NOT NULL,
    isDeleted BOOL NOT NULL DEFAULT 0,
    PRIMARY KEY (`eventId`, `objectId`),
    CONSTRAINT `Constr_EventObject_Event_fk`
        FOREIGN KEY `eventObject_event_fk` (`eventId`) REFERENCES `Event` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `Constr_EventObject_Object_fk`
        FOREIGN KEY `eventObject_object_fk` (`objectId`) REFERENCES `Object` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `Cron`(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    date DATETIME NOT NULL,
    frecuency varchar(10) NOT NULL,
    isDeleted bool NOT NULL DEFAULT 0,
    operationType INT NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Email`(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    cronId INT UNSIGNED NOT NULL,
    email varchar(200) NOT NULL,
    isDeleted bool NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    CONSTRAINT `Constr_Cron_fk`
        FOREIGN KEY `Cron_fk` (`cronId`) REFERENCES `Cron` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `DailyReport`(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    day DATETIME NOT NULL,
    infractions INT UNSIGNED NOT NULL,
    events INT UNSIGNED NOT NULL,
    isDeleted bool NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `DailyObject` (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    dailyReportId INT UNSIGNED NOT NULL,
    objectId INT UNSIGNED NOT NULL,
    count INT UNSIGNED NOT NULL,
    isDeleted bool NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    CONSTRAINT `Constr_DailyObject_DailyReport_fk`
        FOREIGN KEY `DailyReport_fk` (`dailyReportId`) REFERENCES `DailyReport` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `Constr_DailyObject_Object_fk`
        FOREIGN KEY `dailyObject_Object_fk` (`objectId`) REFERENCES `Object` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);
