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

CREATE TABLE IF NOT EXISTS `users` ( -- data from GitHub
  `id` int(11) NOT NULL AUTO_INCREMENT, -- user.id
  `email` varchar(255) NOT NULL, -- user.email
  `name` varchar(255) NOT NULL, -- user.name
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `users_repos` ( -- data from GitHub
  `id` int(11) NOT NULL AUTO_INCREMENT, -- repo.id
  `user_id` int(11) NOT NULL, -- user.id
  `project` varchar(255) NOT NULL, -- repo.full_name
  `url` blob NOT NULL, -- repo.clone_url
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `sessions` (
  `id` varchar(32) NOT NULL, -- session id
  `data` blob NOT NULL, -- session data
  `touched` datetime NOT NULL, -- last read/written
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;
