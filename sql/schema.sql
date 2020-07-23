PRAGMA foreign_keys = ON;

CREATE TABLE businesses(
  bid INTEGER PRIMARY KEY AUTOINCREMENT,
  uid VARCHAR(40) NOT NULL,
  name VARCHAR(40) NOT NULL,
  description VARCHAR(140) NOT NULL,
  email VARCHAR(40),
  UNIQUE(bid),
  UNIQUE(uid)
);

/*
CREATE TABLE businesses(
  bid INTEGER PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  password VARCHAR(40) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
  address_street VARCHAR(40) NOT NULL,
  address_city VARCHAR(40) NOT NULL,
  address_state VARCHAR(40) NOT NULL,
  zipcode NUMBER NOT NULL,
  UNIQUE(bid),
  UNIQUE(email)
);
*/

/*
CREATE TABLE opening_hours(
  bid NUMBER NOT NULL,
  weekday NUMBER NOT NULL,
  open_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP NOT NULL,
  PRIMARY KEY (bid, weekday),
  FOREIGN KEY (bid) REFERENCES businesses(bid)
);

CREATE TABLE contact(
  bid NUMBER NOT NULL,
  pid NUMBER NOT NULL AUTOINCREMENT,
  phone_number NUMBER NOT NULL,
  PRIMARY KEY (bid, pid),
  FOREIGN KEY (bid) REFERENCES businesses(bid)
);*/

CREATE TABLE queues(
  qid INTEGER PRIMARY KEY AUTOINCREMENT,
  bid INTEGER NOT NULL,
  qname VARCHAR(20) NOT NULL,
  code VARCHAR(10) NOT NULL,
  description VARCHAR(200) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
  FOREIGN KEY (bid) REFERENCES businesses(bid),
  UNIQUE(code)
);

CREATE TABLE users(
  phone VARCHAR(20) PRIMARY KEY NOT NULL,
  qid INTEGER NOT NULL,
  status INTEGER DEFAULT 0 NOT NULL,
  FOREIGN KEY (qid) REFERENCES queues(qid)
);

/* this is a sample queue */
CREATE TABLE queue_qid0(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(20) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  note VARCHAR(100) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE queue_qid1(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(20) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  note VARCHAR(100) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE queue_qid2(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(20) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  note VARCHAR(100) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE queue_qid3(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(20) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  note VARCHAR(100) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE queue_qid4(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(20) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  note VARCHAR(100) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- the below would be nicer but isn't working for some reason
-- doesn't preserve the primary key structure
--CREATE TABLE queue_qid1 AS SELECT * FROM queue_qid0 WHERE 0;
--CREATE TABLE queue_qid2 AS SELECT * FROM queue_qid0;
--CREATE TABLE queue_qid3 AS SELECT * FROM queue_qid0;
--CREATE TABLE queue_qid4 AS SELECT * FROM queue_qid0;
