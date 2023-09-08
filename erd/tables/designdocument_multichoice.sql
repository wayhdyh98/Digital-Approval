CREATE TABLE MPMDS.dbo.designdocument_multichoice (
	designdocumentmultichoiceid uniqueidentifier DEFAULT newid() NOT NULL,
    designdocumentquestionid  uniqueidentifier NOT NULL,
	masterdocid uniqueidentifier NOT NULL,
	code varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[value] varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	createdby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	createddate datetime NULL,
	CONSTRAINT PK_designdocument_multichoice_id PRIMARY KEY (designdocumentmultichoiceid)
);

ALTER TABLE MPMDS.dbo.designdocument_multichoice 
    ADD CONSTRAINT FK_questionmultichoice_question 
    FOREIGN KEY (designdocumentquestionid) 
    REFERENCES MPMDS.dbo.designdocument_question(designdocumentquestionid);

ALTER TABLE MPMDS.dbo.designdocument_multichoice 
    ADD CONSTRAINT FK_questionmultichoice_document 
    FOREIGN KEY (masterdocid) 
    REFERENCES MPMDS.dbo.masterdocument(masterdocid);