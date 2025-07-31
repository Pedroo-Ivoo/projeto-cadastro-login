drop table if exists usuarios;

create table usuarios(
    id serial primary key,
    nome varchar(150) not null,
    email varchar(50) not null UNIQUE,
    cep  varchar(9) not null,
    rua varchar(50) not null,
    numero varchar(5) not null,
    complemento varchar(50),
    bairro varchar(50) not null,
    cidade varchar(50) not null,
    estado varchar(2) not null,
    usuario varchar(12) not null UNIQUE,
    senha BYTEA not null
);
