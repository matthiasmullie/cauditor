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
  `hash` binary(40) NOT NULL, -- commit sha
  `author` varchar(255) NOT NULL, -- author email
  `author_date` datetime NOT NULL, -- date authored
  `committer` varchar(255) NOT NULL, -- committer email
  `commit_date` datetime NOT NULL, -- date of commit
  `metrics` blob DEFAULT NULL, -- metrics for this specific commit
  PRIMARY KEY (`project`,`hash`),
  -- @todo below UNIQUE will fail to insert commits in forks - fix this DB to allow that some day (but not store stats more than once)
  UNIQUE KEY `idx_unique` (`project`,`hash`,`author`), -- ensure commits only get in once (don't care about same commit in forks)
  KEY `idx_project` (`project`,`commit_date`), -- fetching last x commits per project
  KEY `idx_author` (`author`,`author_date`) -- fetching last x commits per author
) DEFAULT CHARSET=utf8;

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
) DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
