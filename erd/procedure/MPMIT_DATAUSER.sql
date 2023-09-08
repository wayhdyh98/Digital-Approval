-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
ALTER PROCEDURE [dbo].[MPMIT_DATAUSER] @NPK varchar(10)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	--SELECT * FROM MPMIT.DBO.MPMIT_PIC A JOIN mpmds.dbo.mpmitpic_wposition B on A.NPK=B.NPK 
	--WHERE A.NPK=@NPK

	SELECT TP.*, A.EMAIL, B.EMAIL, A.JABATAN, B.ttd FROM mpmitpic_wposition A
	JOIN (SELECT  RIGHT('00000'+CAST(ISNULL([EMPLOYEE_ID],0) AS VARCHAR(5)),5) NPK
		,[DISPLAY_NAME] NAME
		,[division] DIVISION_NAME
		,[COMPANY_ID] COMPANY_ID
		,[department] DEPARTMENTNAME
		,[iddivision] DIVISIONID
		,[iddepartment] DEPARTMENT_ID
	FROM [MPMDS].[dbo].[MPMDS_ORANGE_DATA]) TP
	ON TP.NPK = A.NPK
	JOIN MPMIT.DBO.MPMIT_PIC (NOLOCK) B ON TP.NPK = B.NPK
	WHERE A.NPK=@NPK
	
END
