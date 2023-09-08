CREATE TABLE MPMDS.dbo.requestapproval_authentication (
	requestapprovalauthenticationid uniqueidentifier DEFAULT newid() NOT NULL,
    requestapprovalid uniqueidentifier NOT NULL,
    masterapproveid uniqueidentifier NOT NULL, -- relation to table masterapproval
    pictype int NOT NULL default(0), -- get data from masterapproval
    picid varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL DEFAULT(''), -- get data from masterapproval or input from user
    piclevel int not null default (1), -- get data from masterapproval
	picsublevel int not null default (1), -- get data from masterapproval
    picname varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL DEFAULT(''), -- get data from masterapproval or input from user
    mandatory int NOT NULL default(0),  -- get data from masterapproval
    statusapprove int NOT NULL default(0), -- 0: default, 1: approved, 2: declined
    commentapprove varchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL DEFAULT(''),
    publickey varchar(MAX) NOT NULL, -- fill with public key at table pic (if public key at pic is None then generate with the new one - secret key and public key)
    deleteflag int NOT NULL DEFAULT(0),
    createdby varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	createddate datetime NULL,
	modifby varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	modifdate datetime NULL,
	CONSTRAINT PK_requestapproval_authentication_requestapprovalauthenticationid PRIMARY KEY (requestapprovalauthenticationid)
);

ALTER TABLE MPMDS.dbo.requestapproval_authentication 
    ADD CONSTRAINT FK_requestapproval_authentication_requestapproval 
    FOREIGN KEY (requestapprovalid) 
    REFERENCES MPMDS.dbo.requestapproval(requestapprovalid);


ALTER TABLE MPMDS.dbo.requestapproval_authentication
    ADD CONSTRAINT FK_requestapproval_authentication_masterapproval
    FOREIGN KEY (masterapproveid) 
    REFERENCES MPMDS.dbo.masterapproval(masterapproveid);
