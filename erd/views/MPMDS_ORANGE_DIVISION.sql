ALTER VIEW MPMDS_ORANGE_DIVISION AS
SELECT COMPANY_ID COMPANYID, IDDIVISION CODE, DIVISION VALUE FROM MPMDS_ORANGE_DATA 
WHERE IDDIVISION <> ''
GROUP BY COMPANY_ID, IDDIVISION, DIVISION