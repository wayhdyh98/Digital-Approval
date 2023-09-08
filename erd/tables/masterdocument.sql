CREATE TABLE MPMDS.dbo.masterdocument (
	masterdocid uniqueidentifier DEFAULT newid() NOT NULL,
	documentnumber bigint IDENTITY(1,1) NOT NULL,
	companyid varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	divisionid varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	departmentid varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	isprint int NOT NULL, -- 0 NO, 1 YES
	name varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[desc] TEXT NOT NULL,
	version varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT('1'),
	status int NOT NULL DEFAULT(0), -- 0 NOT ACTIVE, 1 ACTIVE
	entryauth varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	layout int NULL DEFAULT(0), -- 0 PORTRAIT, 1 LANDSCAPE
	nosig int DEFAULT 0 NOT NULL, -- 0 NO SIGNATURE, 1 SIGNATURE
	deleteflag int NOT NULL DEFAULT(0),
	createdby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT(GETDATE()),
	createddate datetime NULL,
	modifby varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	modifdate datetime NULL,
	CONSTRAINT PK_masterdocument_masterdocid PRIMARY KEY (masterdocid)
);