CREATE TABLE MPMDS.dbo.masterapproval (
	masterapproveid uniqueidentifier DEFAULT newid() NOT NULL,
	masterdocid uniqueidentifier NOT NULL,
	pictype int NOT NULL default(0),
	picid varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	piclevel int not null default (1),
	picsublevel int not null default (1),
	mandatory int NOT NULL default(0),
	descriptionapprovaltitle varchar(max) not null default (''),
	createdby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	createddate datetime NOT NULL,
	modifby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	modifdate datetime NOT NULL,
	CONSTRAINT PK_masterapproval PRIMARY KEY (masterapproveid)
);

ALTER TABLE MPMDS.dbo.masterapproval ADD CONSTRAINT FK_masterapproval_document FOREIGN KEY (masterdocid) REFERENCES MPMDS.dbo.masterdocument(masterdocid);