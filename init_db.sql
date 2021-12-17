use alikadk_db;

drop table if exists Users;
drop table if exists Events;


create table Users(
    stuid int not null auto_increment,
    username varchar(50) not null,
    email  varchar(50) not null,
    hash_pwd varchar(100) not null,
    primary key(stuid)
);

create table Events(
    eid int not null auto_increment,
    title varchar(100) not null,
    descrip varchar (250) not null,
    time datetime not null,
    location varchar(50),
    sid int not null,
    primary key(eid),
    foreign key (sid) references Users(stuid)
        on update cascade
        on delete cascade
);

