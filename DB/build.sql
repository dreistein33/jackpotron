CREATE TYPE enum_status AS ENUM ('started', 'ended');

DROP TABLE IF EXISTS loteria;
CREATE TABLE loteria (
    id INTEGER PRIMARY KEY NOT NULL,
    start_time REAL NOT NULL CHECK (start_time > 0),
    end_time REAL NOT NULL CHECK (end_time > start_time),
    _status enum_status NOT NULL,
    wallet VARCHAR(40) NOT NULL,
    winner VARCHAR(40)
);


DROP TABLE IF EXISTS ticket;
CREATE TABLE ticket (
    id INTEGER PRIMARY KEY NOT NULL,
    sender VARCHAR(40) NOT NULL,
    amount REAL NOT NULL CHECK (amount > 0),
    _timestamp REAL NOT NULL CHECK (_timestamp > 0),
    memo VARCHAR(255),
    loteria_id INTEGER NOT NULL,
    FOREIGN KEY (loteria_id) REFERENCES loteria (id)
);