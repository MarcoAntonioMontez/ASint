
drop table building;
drop table user_msg;
drop table user_move;
drop table logs;
drop table users;

-- Admin users in the system (not implemented yet) TODO

create table users
	(user_id	varchar(20) not null unique,
	 user_latitude 	float(15) not null,
	 user_longitude float(15) not null,
	 primary key(user_id));

create table logs
	(log_id	int not null,
	 content_id	int not null,
	 user_id	varchar(20) not null,
	 entry_type ENUM('Move', 'Msg') not null,
	 primary key(log_id),
	 foreign key(user_id) references users(user_id));

create table user_move
	(move_id	int not null unique,
	 user_id	varchar(20) not null unique,
	 move_time datetime,
	 old_latitude	float(15) not null,
	 old_longitude	float(15) not null,
	 new_latitude	float(15) not null,
	 new_longitude	float(15) not null,
	 primary key(move_id),
	 foreign key(user_id) references users(user_id));

create table user_msg
	(msg_id	int not null unique,
	 user_id	varchar(20) not null unique,
	 msg_time datetime,
	 msg_body varchar(200),
	 latitude	float(15) not null,
	 longitude	float(15) not null,
	 radius float(2) not null,
	 primary key(msg_id),
	 foreign key(user_id) references users(user_id));


create table building
	(building_id	int not null unique,
	 building_name varchar(200),
	 latitude	float(15) not null,
	 longitude	float(15) not null,
	 radius float(2) not null,
	 primary key(building_id));