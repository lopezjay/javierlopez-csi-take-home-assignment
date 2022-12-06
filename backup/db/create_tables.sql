CREATE TABLE contentprerollpairs (
    id int NOT NULL,
    content varchar(255) NOT NULL,
    preroll varchar(255) NOT NULL,
    playorder int NOT NULL,
);

CREATE TABLE videos (
    name: varchar(255) NOT NULL,
    country: varchar(255) NOT NULL,
    language: varchar(255) NOT NULL,
    content varchar(255),
    preroll varchar(255),
    PRIMARY KEY (name)
);

CREATE TABLE playlistsvideopairs (
    ID int NOT NULL,
    country: varchar(255) NOT NULL,
    language: varchar(255) NOT NULL,
    video: varchar(255) NOT NULL,
    playorder int NOT NULL,
    content: varchat(255) NOT NULL,
    FOREIGN KEY (video) REFERENCES Videos(name)
)