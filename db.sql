CREATE TABLE IF NOT EXISTS `projects` (
  `name` varchar(255) NOT NULL, -- vendor/project
  `git` blob NOT NULL, -- clone url
  `default_branch` varchar(255) NOT NULL,
  `github_id` INT UNSIGNED DEFAULT NULL, -- repo id
  `github_hook` INT UNSIGNED DEFAULT NULL, -- hook id
  `score` decimal(11, 2) NOT NULL, -- score, for comparison with other projects
  PRIMARY KEY (`name`),
  UNIQUE KEY `idx_git` (`github_id`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `commits` (
  `project` varchar(255) NOT NULL, -- vendor/project
  `branch` varchar(255) NOT NULL,
  `commit_id` INT UNSIGNED NOT NULL, -- FK, with commit_details.id
  PRIMARY KEY (`project`,`branch`,`commit_id`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `commit_details` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `hash` binary(40) NOT NULL, -- commit sha
  `previous` binary(40) DEFAULT NULL, -- previous commit sha
  `author` varchar(255) NOT NULL, -- author email
  `timestamp` datetime NOT NULL, -- commit date
  -- project-wide metrics as of this commit
  `loc` INT UNSIGNED NOT NULL,
  `noc` INT UNSIGNED NOT NULL,
  `nom` INT UNSIGNED NOT NULL,
  `nof` INT UNSIGNED NOT NULL,
  -- project-wide averages as of this commit
  `avg_ca` decimal(11, 2) NOT NULL,
  `avg_ce` decimal(11, 2) NOT NULL,
  `avg_i` decimal(11, 2) NOT NULL,
  `avg_dit` decimal(11, 2) NOT NULL,
  `avg_ccn` decimal(11, 2) NOT NULL,
  `avg_npath` decimal(11, 2) NOT NULL,
  `avg_he` decimal(11, 2) NOT NULL,
  `avg_hi` decimal(11, 2) NOT NULL,
  `avg_mi` decimal(11, 2) NOT NULL,
  -- project-wide worsts as of this commit
  `worst_ca` INT UNSIGNED NOT NULL,
  `worst_ce` INT UNSIGNED NOT NULL,
  `worst_i` decimal(11, 2) NOT NULL,
  `worst_dit` INT UNSIGNED NOT NULL,
  `worst_ccn` INT UNSIGNED NOT NULL,
  `worst_npath` BIGINT UNSIGNED NOT NULL,
  `worst_he` decimal(11, 2) NOT NULL,
  `worst_hi` decimal(11, 2) NOT NULL,
  `worst_mi` decimal(11, 2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_unique` (`author`,`timestamp`,`hash`)
) DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

CREATE TABLE IF NOT EXISTS `sessions` (
  `id` varchar(32) NOT NULL, -- session id
  `data` longblob NOT NULL, -- session data
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

CREATE TABLE IF NOT EXISTS `feedback` (
  `project` varchar(255) NOT NULL, -- vendor/project
  `author` varchar(255) NOT NULL, -- colleague email
  `question` varchar(255) NOT NULL,
  `score` TINYINT NOT NULL
) DEFAULT CHARSET=utf8;
