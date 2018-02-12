create table IF NOT EXISTS data (
    id integer primary key autoincrement,
    name text not null,
    load_date text not null,
    content text not null
);