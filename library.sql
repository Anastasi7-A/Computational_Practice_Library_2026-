DROP DATABASE library;

CREATE DATABASE library 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
use library;
show databases;

create table genres(
genre_id int auto_increment,
genre_name varchar(100) not null unique,
primary key(genre_id));

create table book (
book_id int auto_increment ,
title varchar(255) not null,
author varchar(255) not null,
book_year int not null,
edition varchar(255),
genre_id int,
total_copies bigint,
available_copies int,
book_description text,
cover_path varchar(255),
created_at timestamp,
primary key(book_id),
foreign key(genre_id) references genres(genre_id)
);

 alter table book 
 add constraint chk_available_cop
 check(available_copies >=0 and available_copies <= total_copies);

create index idx_book_title on book(title);
create index idx_book_author on book(author);
create index idx_book_genre on book(genre_id);

create table users (
user_id int auto_increment,
full_name varchar(100) not null,
email varchar(100) unique not null,
user_role enum('admin', 'techer', 'student'),
faculty varchar(100),
phone varchar(20),
reg_date date,
is_active bool,
primary key(user_id)
);

create table loans(
loan_id int auto_increment,
book_id int not null,
user_id int not null,
loan_date date not null,
due_date date not null,
return_date date,
status_loan enum('active', 'returned', 'overdue', 'lost'),
primary key(loan_id),
foreign key(book_id) references book(book_id) on delete restrict,
foreign key(user_id) references users(user_id) on delete restrict
);

create index idx_loans_user on loans(user_id);
create index idx_loans_status on loans(status_loan);

create table fines (
fine_id int auto_increment,
loan_id int not null,
user_id int not null,
amount decimal(8,2) not null,
per_date_rate decimal(6,2) not null,
days_overdue int not null,
created_at datetime not null,
paid_at datetime,
is_paid boolean not null default false,
primary key (fine_id),
foreign key(loan_id) references loans(loan_id) on delete cascade,
foreign key(user_id) references users(user_id) on delete restrict
);

create table reservation(
reservation_id int auto_increment,
book_id int not null,
user_id int not null,
reservation_date datetime not null,
expiry_date datetime,
status_res enum('reserved', 'waiting', 'fulfilled','cancelled', 'expired'),
primary key(reservation_id),
foreign key(book_id) references book(book_id) on delete cascade,
foreign key(user_id) references users(user_id) on delete cascade
);

