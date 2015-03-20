CREATE TABLE IF NOT EXISTS `projects` (
  `name` varchar(255) NOT NULL, -- vendor/project
  `git` blob NOT NULL, -- clone url
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
