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
  `commit_id` int(11) NOT NULL, -- FK, with commit_details.id
  PRIMARY KEY (`project`,`commit_id`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `commit_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash` binary(40) NOT NULL, -- commit sha
  `author` varchar(255) NOT NULL, -- author email
  `author_date` datetime NOT NULL, -- date authored
  `committer` varchar(255) NOT NULL, -- committer email
  `commit_date` datetime NOT NULL, -- date of commit
  `metrics` blob, -- metrics for this specific commit
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_unique` (`commit_date``,`hash`,`author`), -- assumes there are no hash collisions per user/date
  KEY `idx_author` (`author`,`author_date`) -- fetching last x commits per author
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

CREATE TABLE IF NOT EXISTS `jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job` blob NOT NULL,
  `type` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;
