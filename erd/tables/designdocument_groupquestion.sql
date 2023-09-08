CREATE TABLE MPMDS.dbo.designdocument_groupquestion (
	designdocumentgroupquestionid uniqueidentifier DEFAULT newid() NOT NULL,
	masterdocid uniqueidentifier NOT NULL,
	grouptitle varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	createdby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	createddate datetime NULL,
	modifby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	modifdate datetime NULL,
	CONSTRAINT PK_designdocument_groupquestion PRIMARY KEY (designdocumentgroupquestionid)
);

ALTER TABLE MPMDS.dbo.designdocument_groupquestion ADD CONSTRAINT FK_groupquestion_document FOREIGN KEY (masterdocid) REFERENCES MPMDS.dbo.masterdocument(masterdocid);

ALTER TABLE designdocument_groupquestion
add sectiontype int NOT NULL DEFAULT (0); -- 0 single, 1 - multirow