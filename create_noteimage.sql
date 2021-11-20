CREATE TABLE "CORE".noteimage(
    noteId          SERIAL PRIMARY KEY,
    modifiedOn      date NOT NULL,
    storedOn        date NOT NULL,
    noteType        varchar(5) NOT NULL,
    filePath        varchar() NOT NULL,
);