CREATE TABLE MPMDS.dbo.requestapproval_answer (
	requestapprovalanswerid uniqueidentifier DEFAULT newid() NOT NULL,
    requestapprovalid uniqueidentifier NOT NULL,
    designdocumentquestionid uniqueidentifier NOT NULL,
    answer varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    deleteflag int NOT NULL DEFAULT(0),
    createdby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	createddate datetime NULL,
	modifby varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	modifdate datetime NULL,
    answergroupid uniqueidentifier NULL,
	CONSTRAINT PK_requestapproval_answer_requestapprovalanswerid PRIMARY KEY (requestapprovalanswerid)
);

ALTER TABLE MPMDS.dbo.requestapproval_answer 
    ADD CONSTRAINT FK_requestapproval_answer_requestapproval 
    FOREIGN KEY (requestapprovalid) 
    REFERENCES MPMDS.dbo.requestapproval(requestapprovalid);



ALTER TABLE MPMDS.dbo.requestapproval_answer 
    ADD CONSTRAINT FK_requestapproval_answer_designdocument_question
    FOREIGN KEY (designdocumentquestionid) 
    REFERENCES MPMDS.dbo.designdocument_question(designdocumentquestionid);
