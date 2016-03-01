CREATE TABLE IF NOT EXISTS `projects` (
  `name` varchar(255) NOT NULL, -- vendor/project
  `git` blob NOT NULL, -- clone url
  `github_id` int(11) DEFAULT NULL, -- repo id
  `github_hook` int(11) DEFAULT NULL, -- hook id
  PRIMARY KEY (`name`),
  UNIQUE KEY `idx_git` (`github_id`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `commits` (
  `project` varchar(255) NOT NULL, -- vendor/project
  `branch` varchar(255) NOT NULL,
  `commit_id` int(11) NOT NULL, -- FK, with commit_details.id
  PRIMARY KEY (`project`,`branch`,`commit_id`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `commit_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash` binary(40) NOT NULL, -- commit sha
  `previous` binary(40) DEFAULT NULL, -- previous commit sha
  `author` varchar(255) NOT NULL, -- author email
  `timestamp` datetime NOT NULL, -- commit date
  -- project-wide metrics as of this commit
  `loc` int(11) NOT NULL,
  `noc` int(11) NOT NULL,
  `nom` int(11) NOT NULL,
  `ca` int(11) NOT NULL,
  `ce` int(11) NOT NULL,
  `i` decimal(11, 2) NOT NULL,
  `dit` int(11) NOT NULL,
  `ccn` int(11) NOT NULL,
  `npath` int(11) NOT NULL,
  `he` decimal(11, 2) NOT NULL,
  `hi` decimal(11, 2) NOT NULL,
  `mi` decimal(11, 2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_unique` (`author`,`timestamp`,`hash`)
) DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

CREATE TABLE IF NOT EXISTS `sessions` (
  `id` varchar(32) NOT NULL, -- session id
  `data` blob NOT NULL, -- session data
  `touched` datetime NOT NULL, -- last read/written
  PRIMARY KEY (`id`),
  KEY `touched` (`touched`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `settings` (
  `user` int(10) NOT NULL,
  `key` varchar(255) NOT NULL,
  `value` blob DEFAULT NULL,
  PRIMARY KEY (`user`,`key`)
) DEFAULT CHARSET=utf8;
