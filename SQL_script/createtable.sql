create database if not exists DB_NAME;
use DB_NAME;
create table if not exists Administrator(
admin_id int auto_increment primary key,
Email varchar(100) not null unique,
u_name varchar(30) default 'administrator',
u_password varchar(100) not null,
pw_salt int,
u_status tinyint unsigned default '0',
addtime DATETIME,
modifytime DATETIME
);

create table if not exists Constructor(
u_id int auto_increment primary key,
Email varchar(100) not null unique,
u_name varchar(30) default 'user',
u_password varchar(100) not null,
pw_salt int,
u_status tinyint unsigned default '0',
addtime DATETIME,
modifytime DATETIME,
addr varchar(100)
);

create table if not exists Product(
p_id int auto_increment primary key,
p_name varchar(50) default 'virtual product',
p_status tinyint unsigned default '0',
addtime DATETIME,
modifytime DATETIME,
avatar varchar(100),
description text
);

create table if not exists Manufacturer(
m_id int auto_increment primary key,
contact varchar(100) not null,
addr varchar(100) not null,
loc varchar(100) not null,
m_status tinyint unsigned default '0',
addtime DATETIME,
modifytime DATETIME,
description text,
m_name varchar(100)
);

CREATE TABLE if not exists cpmapping (
  id int NOT NULL AUTO_INCREMENT,
  c_id int NOT NULL,
  c_email varchar(100) NOT NULL,
  p_id int NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE pmmapping (
  id int NOT NULL AUTO_INCREMENT,
  p_id int NOT NULL,
  m_id int NOT NULL,
  m_pnode int not null,
  m_Tlevel int not null,
  PRIMARY KEY (id)
);