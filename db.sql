CREATE TABLE IF NOT EXISTS `projects` (
  `name` varchar(255) NOT NULL, -- vendor/project
  `git` blob NOT NULL, -- clone url
  `hook` int(11) DEFAULT NULL, -- hook id
  PRIMARY KEY (`name`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `commits` (
  `project` varchar(255) NOT NULL, -- vendor/project
  `hash` binary(40) NOT NULL, -- commit sha
  `author` varchar(255) NOT NULL, -- author email
  `date` datetime NOT NULL, -- date of commit
  PRIMARY KEY (`project`,`commit`),
  UNIQUE KEY `idx_author` (`project`,`commit`,`author`),
  UNIQUE KEY `idx_date` (`project`,`commit`,`date`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `sessions` (
  `id` varchar(32) NOT NULL, -- session id
  `data` blob NOT NULL, -- session data
  `touched` datetime NOT NULL, -- last read/written
  PRIMARY KEY (`id`),
  KEY `touched` (`touched`)
) DEFAULT CHARSET=utf8;
