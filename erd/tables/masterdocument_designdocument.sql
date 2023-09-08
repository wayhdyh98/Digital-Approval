CREATE TABLE MPMDS.dbo.masterdocument_designdocument (
    designdocumentid uniqueidentifier DEFAULT newid() NOT NULL,
	documentid uniqueidentifier NOT NULL,
	contentdocument varchar(MAX) NULL,
	contentorigin varchar(MAX) NULL,
	version int IDENTITY(1,1) NOT NULL,
	createby varchar(10) NULL,
	createddate datetime NULL,
	modifby varchar(20) NULL,
	modifdate datetime NULL,
    CONSTRAINT PK_masterdocument_designdocument PRIMARY KEY (designdocumentid) 
);