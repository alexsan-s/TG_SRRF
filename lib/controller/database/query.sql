-- PSQL -D SRRF
DROP TABLE CLIENT_PRODUCT;
DROP TABLE PURCHASES;
DROP TABLE PRODUCT_PICTURE;
DROP TABLE CATEGORIE;
DROP TABLE CLIENT_PICTURE;
DROP TABLE CLIENT;
DROP TABLE OPERATOR_CONTROLLER;
DROP TABLE CONTROLLER;
DROP TABLE PRODUCT;
DROP TABLE OPERATOR;

CREATE TABLE IF NOT EXISTS OPERATOR (
	PK_OPERATOR SERIAL,
	NAME TEXT,
	TELEFONE TEXT,
	CPF TEXT,
	EMAIL TEXT,
	LOGIN TEXT,
	PASSWORD TEXT,
	PASS_HASH TEXT,
	INACTIVE NUMERIC(9,2),
	PRIMARY KEY(PK_OPERATOR )
);

CREATE TABLE IF NOT EXISTS CONTROLLER (
	PK_CONTROLLER SERIAL,
	CONTROLLER TEXT,
	PATTERN TEXT,
	PRIMARY KEY(PK_CONTROLLER )
);

CREATE TABLE IF NOT EXISTS OPERATOR_CONTROLLER(
    PK_OPERATOR INTEGER,
    PK_CONTROLLER INTEGER,
    FOREIGN KEY (PK_OPERATOR) REFERENCES OPERATOR(PK_OPERATOR),
    FOREIGN KEY (PK_CONTROLLER) REFERENCES CONTROLLER(PK_CONTROLLER)
);
CREATE TABLE IF NOT EXISTS CLIENT(
	PK_CLIENT SERIAL,
	NAME TEXT,
	CPF TEXT,
    RG TEXT,
    BIRTH DATE,
    SEX CHARACTER(1),
	EMAIL TEXT,
    CEP TEXT,
    ADDRESS TEXT,
    NUMBER INTEGER,
    DISTRICT TEXT,
    CITY TEXT, 
    STATE TEXT,
	TELEFONE TEXT,
    CELL TEXT,
	PRIMARY KEY(PK_CLIENT)
);
CREATE TABLE IF NOT EXISTS CLIENT_PICTURE(
	PK_CLIENT_PICTURE SERIAL,
	PK_CLIENT INTEGER,
	PICTURE TEXT,
    PRIMARY KEY (PK_CLIENT_PICTURE),
    FOREIGN KEY (PK_CLIENT) REFERENCES CLIENT(PK_CLIENT)
);
CREATE TABLE IF NOT EXISTS CATEGORIE(
    PK_CATEGORIE SERIAL,
    CATEGORIE TEXT,
    PATTERN INTEGER,
    PRIMARY KEY(PK_CATEGORIE)
);
CREATE TABLE IF NOT EXISTS PRODUCT(
    PK_PRODUCT SERIAL,
    PRODUCT TEXT,
    DESCRIPTION TEXT,
    INACTIVE INTEGER,
    PRIMARY KEY(PK_PRODUCT)
);
CREATE TABLE IF NOT EXISTS PRODUCT_PICTURE(
    PK_PRODUCT_PICTURE SERIAL,
    PK_PRODUCT INTEGER,
    PICTURE TEXT,
    PRIMARY KEY (PK_PRODUCT_PICTURE),
    FOREIGN KEY (PK_PRODUCT) REFERENCES PRODUCT(PK_PRODUCT)
);
CREATE TABLE IF NOT EXISTS PURCHASES(
    PK_PURCHASES SERIAL,
    PURCHASES_DATE DATE NOT NULL DEFAULT CURRENT_DATE,
    PK_CLIENT INTEGER,
    FOREIGN KEY(PK_CLIENT) REFERENCES CLIENT(PK_CLIENT),
    PRIMARY KEY(PK_PURCHASES)
);
CREATE TABLE IF NOT EXISTS CLIENT_PRODUCT(
    PK_CLIENT_PRODUCT SERIAL,
    PK_PURCHASES INTEGER,
    PK_PRODUCT INTEGER,
    PRIMARY KEY (PK_CLIENT_PRODUCT),
    FOREIGN KEY(PK_PURCHASES) REFERENCES PURCHASES(PK_PURCHASES),
    FOREIGN KEY(PK_PRODUCT) REFERENCES PRODUCT(PK_PRODUCT)
);