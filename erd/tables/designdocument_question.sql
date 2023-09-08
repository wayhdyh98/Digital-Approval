CREATE TABLE MPMDS.dbo.designdocument_question (
	designdocumentquestionid uniqueidentifier DEFAULT newid() NOT NULL,
    designdocumentgroupquestionid  uniqueidentifier NOT NULL,
	masterdocid uniqueidentifier NOT NULL,
	question varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	questiontype int NOT NULL default(0),
	questioncondition int NOT NULL default(0),
	mandatory int NOT NULL default(0),
	questiontypecomponent int NOT NULL default(0),
	createdby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	createddate datetime NULL,
	modifby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	modifdate datetime NULL,
	note varchar(MAX) NULL,
	CONSTRAINT PK_designdocument_question_id PRIMARY KEY (designdocumentquestionid)
);

ALTER TABLE MPMDS.dbo.designdocument_question ADD CONSTRAINT FK_question_groupquestion FOREIGN KEY (designdocumentgroupquestionid) REFERENCES MPMDS.dbo.designdocument_groupquestion(designdocumentgroupquestionid);
ALTER TABLE MPMDS.dbo.designdocument_question ADD CONSTRAINT FK_question_document FOREIGN KEY (masterdocid) REFERENCES MPMDS.dbo.masterdocument(masterdocid);