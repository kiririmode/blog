drop table if exists parents;
create table parents (
    id int not null
    , name varchar(500) not null
    , constraint parents_PKC primary key (id)
);

insert into parents(id, name) values
(1, 'ウルトラの父'),
(2, 'ウルトラの母');

CREATE SEQUENCE id_seq;
