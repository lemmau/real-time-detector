
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
    ("Barbijo", "Barbijo"),
    ("Proteccion ocular", "gafas, lentes u otro element que proteja ojos"),
    ("Barbijo y Proteccion ocular", "Barbijo y gafas, lentes u otro element que proteja ojos"),
    ("Mascara Facial", "mascaras que cumbre todo el rostro"),
    ("Infraccion", "Cara Limpia, la persona no usa elementos en su rostro");


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
    date varchar(20) NOT NULL,
    day_of_week varchar(10) NOT NULL,
    day varchar(10) NOT NULL,
    hour varchar(2) NOT NULL,
    isDeleted bool NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Email`(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    email varchar(200) NOT NULL,
    isDeleted bool NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `DailyReport`(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    day DATETIME NOT NULL,
    events INT UNSIGNED NOT NULL,
    detectedClassId INT UNSIGNED NOT NULL,
    isDeleted bool NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
    -- CONSTRAINT `DailyReport_DetectedClass_fk`
    --     FOREIGN KEY (`detectedClassId`) REFERENCES DetectedClass(id)
    --     ON DELETE CASCADE ON UPDATE CASCADE
);
