create table if not exists users (
id integer primary key AUTOINCREMENT,
username text not null,
password text not null,
email text not null,
role text not null
);