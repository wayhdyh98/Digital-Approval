<<<<<<< HEAD
CREATE TABLE MPMDS.dbo.approvalonline_files (
	approvalonlinefileid uniqueidentifier DEFAULT newid() NOT NULL,
    filetype INT NOT NULL DEFAULT(1), -- 1 : main file
	filename varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT(''),
    aliasfilename varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT(''),
    size INT NOT NULL DEFAULT(0),
    comments varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT(''),
    referenceid uniqueidentifier NOT NULL,
    deleteflag int NOT NULL DEFAULT(0),
	createdby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT(GETDATE()),
	createddate datetime NULL,
	modifby varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	modifdate datetime NULL,
	CONSTRAINT PK_approvalonline_files_approvalonlinefileid PRIMARY KEY (approvalonlinefileid)
=======
CREATE TABLE MPMDS.dbo.approvalonline_files (
	approvalonlinefileid uniqueidentifier DEFAULT newid() NOT NULL,
    filetype INT NOT NULL DEFAULT(1), -- 1 : main file
	filename varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT(''),
    aliasfilename varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT(''),
    size INT NOT NULL DEFAULT(0),
    comments varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT(''),
    referenceid uniqueidentifier NOT NULL,
    deleteflag int NOT NULL DEFAULT(0),
	createdby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT(GETDATE()),
	createddate datetime NULL,
	modifby varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	modifdate datetime NULL,
	CONSTRAINT PK_approvalonline_files_approvalonlinefileid PRIMARY KEY (approvalonlinefileid)
>>>>>>> 6a2152d28bf46329e647de233fcb6e15f9038312
);