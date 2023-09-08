CREATE TABLE MPMDS.dbo.requestapproval (
	requestapprovalid uniqueidentifier DEFAULT newid() NOT NULL,
    requestapprovalnumber bigint IDENTITY(1,1) NOT NULL,
    masterdocid uniqueidentifier NOT NULL,
    name varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[desc] varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	statusrequest int NOT NULL DEFAULT(0), -- 0 DRAFT, 1 SUBMIT, 2 CANCEL
    picrequester varchar(10) NOT NULL, -- BASED ON NPK
    deleteflag int NOT NULL DEFAULT(0),
    createdby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	createddate datetime NULL,
	modifby varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	modifdate datetime NULL,
	CONSTRAINT PK_requestapproval_requestapprovalid PRIMARY KEY (requestapprovalid)
);

ALTER TABLE MPMDS.dbo.requestapproval 
    ADD CONSTRAINT FK_requestapproval_document 
    FOREIGN KEY (masterdocid) 
    REFERENCES MPMDS.dbo.masterdocument(masterdocid);
