
CREATE DATABASE IF NOT EXISTS `real-time-detector`;

USE `real-time-detector`;

CREATE TABLE IF NOT EXISTS `DetectedClass`(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar(50) NOT NULL,
    description varchar(200),
    isDeleted BOOL NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
);

INSERT INTO `DetectedClass` (`name`, `description`) VALUES
    ("Limpio", "Cara Limpia, la persona no usa elementos en su rostro"),
    ("Barbijo", "Barbijo"),
    ("Protección ocular", "gafas, lentes u otro element que proteja ojos"),
    ("Mascara Facial", "mascaras que cumbre todo el rostro"),
    ("Barbijo y Protección ocular", "Barbijo y gafas, lentes u otro element que proteja ojos");


CREATE TABLE IF NOT EXISTS `Event`(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    timestamp INT UNSIGNED NOT NULL,
    detectedClassId INT UNSIGNED NOT NULL,
    isInfraction BOOL NOT NULL,
    isDeleted BOOL NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
    -- CONSTRAINT `Event_DetectedClass_fk`
    --     FOREIGN KEY (`detectedClassId`) REFERENCES DetectedClass(id)
    --     ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `Cron`(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    date DATETIME NOT NULL,
    frecuency varchar(10) NOT NULL,
    isDeleted bool NOT NULL DEFAULT 0,
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
    detectedClassId INT UNSIGNED NOT NULL,
    isDeleted bool NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    CONSTRAINT `DailyReport_DetectedClass_fk`
        FOREIGN KEY (`detectedClassId`) REFERENCES DetectedClass(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
