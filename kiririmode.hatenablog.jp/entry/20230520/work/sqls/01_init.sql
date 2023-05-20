drop table if exists parents;
create table parents (
    id int not null
    , name varchar(500) not null
    , constraint parents_PKC primary key (id)
);

drop table if exists children;
create table children (
    id int not null
    , father_id int
    , mother_id int
    , name varchar(500) not null
);

alter table children
    add constraint father_FK foreign key(father_id) references parents(id)
    on delete no action
    on update no action;

alter table children
    add constraint mother_FK foreign key (mother_id) references parents(id)
    on delete no action
    on update no action;

insert into parents(id, name) values
(1, 'ウルトラの父'),
(2, 'ウルトラの母');

insert into children(id, father_id, mother_id, name) values
(1, 1, 2, 'ウルトラマンタロウ');
