CREATE TABLE IF NOT EXISTS `karma` (
    id      INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    word    TEXT NOT NULL,
    karma   INT DEFAULT 0,
    is_user BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS `events` (
    id          INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    date_event  DATE NOT NULL,
    time_event  TIME NOT NULL DEFAULT '19:00',
    link        TEXT NOT NULL,
    place       TEXT NOT NULL,
    maps        TEXT NOT NULL,
    attendance  INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS `quotes` (
    id          INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    quote        TEXT NOT NULL,
    user       TEXT
);