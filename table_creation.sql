drop table buildings;
drop table user_msg;
drop table user_move;
drop table logs;
drop table users;

-- Admin users in the system (not implemented yet) TODO

create table users
	(user_id	varchar(20) not null unique,
	 user_latitude 	double not null,
	 user_longitude double not null,
	 primary key(user_id));

create table logs
	(log_id	 	int NOT NULL AUTO_INCREMENT,
	 content_id	int not null,
	 user_id	varchar(20) not null,
	 entry_type ENUM('Move', 'Msg') not null,
	 primary key(log_id),
	 foreign key(user_id) references users(user_id));

create table user_move
	(move_id 	int NOT NULL AUTO_INCREMENT,
	 user_id	varchar(20) not null,
	 move_time datetime,
	 old_latitude	double not null,
	 old_longitude	double not null,
	 new_latitude	double not null,
	 new_longitude	double not null,
	 primary key(move_id),
	 foreign key(user_id) references users(user_id));

create table user_msg
	(msg_id 	int NOT NULL AUTO_INCREMENT,
	 user_id	varchar(20) not null,
	 msg_time datetime,
	 msg_body varchar(200) not null,
	 latitude	double not null,
	 longitude	double not null,
	 radius float(2) not null check (radius>=0),
	 primary key(msg_id),
	 foreign key(user_id) references users(user_id));


create table buildings
	(building_id 	int NOT NULL AUTO_INCREMENT,
	 building_name varchar(200),
	 latitude	double not null,
	 longitude  double not null,
	 radius float(2) not null check (radius>=0),
	 primary key(building_id));

insert into buildings (building_name, latitude, longitude, radius) VALUES ('Biblioteca','38.811977','-9.094261','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('DPRSN Armazém','38.813276','-9.092613','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('DPRSN_dosimetria','38.813088','-9.094488','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Liq. Hélio / LETAL','38.811529','-9.094861','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('DPRSN - Proteção e Segurança Radiológica','38.812983','-9.094206','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Física','38.812174','-9.093365','20');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Administração','38.811731','-9.093865','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Edifício principal','38.73715','-9.302892','30');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Civil','38.737466','-9.140206','20');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Química','38.736246','-9.138529','5');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Infantário','38.735803','-9.139441','5');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Minas','38.735748','-9.138452','5');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Secção de Folhas','38.736328','-9.137812','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Electricidade','38.73783','-9.138693','5');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Torre Norte','38.737579','-9.138582','5');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Física','38.735524','-9.140224','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão da Associação dos  Estudantes','38.736331','-9.137089','20');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão do Jardim Sul','38.735561','-9.139211','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão do Jardim Norte','38.737887','-9.139453','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Complexo Interdisciplinar','38.736051','-9.140108','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Torre Sul','38.735993','-9.138438','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão Central','38.736747','-9.139328','20');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Matemática','38.735557','-9.139817','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Acção Social','38.735797','-9.137613','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Mecânica I','38.737316','-9.138618','5');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Mecânica II','38.737466','-9.137315','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Mecânica III','38.737419','-9.137042','5');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Mecânica IV','38.737621','-9.137872','5');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Informática I','38.737916','-9.137761','5');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Informática II','38.737257','-9.137843','10');
insert into buildings (building_name, latitude, longitude, radius) VALUES ('Pavilhão de Informática III','38.73763','-9.137587','5');