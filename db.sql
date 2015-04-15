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
  `loc` int(11) NOT NULL, -- amount of added lines in this commit
  `ca` float NOT NULL, -- average ca in this commits: (this commit total - prev commit total) / lines
  `ce` float NOT NULL, -- average ce in this commits: (this commit total - prev commit total) / lines
  `i` float NOT NULL, -- average i in this commits: (this commit total - prev commit total) / lines
  `dit` float NOT NULL, -- average dit in this commits: (this commit total - prev commit total) / lines
  `ccn` float NOT NULL, -- average ccn in this commits: (this commit total - prev commit total) / lines
  `npath` float NOT NULL, -- average npath in this commits: (this commit total - prev commit total) / lines
  `he` float NOT NULL, -- average he in this commits: (this commit total - prev commit total) / lines
  `hi` float NOT NULL, -- average hi in this commits: (this commit total - prev commit total) / lines
  `mi` float NOT NULL, -- average mi in this commits: (this commit total - prev commit total) / lines
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
