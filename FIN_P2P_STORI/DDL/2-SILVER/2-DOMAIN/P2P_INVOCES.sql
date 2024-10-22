CREATE OR REPLACE TABLE STORI_SILVER_DB_PROD.PROCUREMENT_TO_PAY.DOMAIN_INVOICE (
  ID INT PRIMARY KEY COMMENT 'UNIQUE IDENTIFIER OF THE INVOICE'
  , SUPPLIER_ID VARCHAR (200) COMMENT 'ID OF THE SUPPLIER'
  , NETSUITE_ID VARCHAR (200) COMMENT 'NETSUITE ID ASSOCIATED WITH THE INVOICE'
  , AMOUNT_DUE FLOAT COMMENT 'AMOUNT DUE FOR THE INVOICE'
  , CANCELED BOOLEAN COMMENT 'INDICATOR OF WHETHER THE INVOICE IS CANCELED'
  , COMPLIANT BOOLEAN COMMENT 'INDICATOR OF WHETHER THE INVOICE IS COMPLIANT'
  , CONFIRMATION VARCHAR(200) COMMENT 'CONFIRMATION STATUS OF THE INVOICE'
  , CREATED_AT DATE COMMENT 'DATE WHEN THE RECORD WAS CREATED'
  , EXPORTED BOOLEAN COMMENT 'INDICATOR OF WHETHER THE INVOICE IS EXPORTED'
  , INVOICE_DATE DATE COMMENT 'DATE OF THE INVOICE'
  , INVOICE_NUMBER VARCHAR(500) COMMENT 'INVOICE NUMBER'
  , PAID BOOLEAN COMMENT 'INDICATOR OF WHETHER THE INVOICE IS PAID'
  , TAX_AMOUNT FLOAT COMMENT 'TAX AMOUNT'
  , TOTAL_WITH_TAXES FLOAT COMMENT 'TOTAL AMOUNT WITH TAXES'
  , UPDATED_AT DATE COMMENT 'DATE OF THE LAST UPDATE'
  , LOADED_AT TIMESTAMP_TZ(9) COMMENT 'TIMESTAMP OF WHEN THE RECORD WAS LOADED INTO THE DATABASE'
)
COMMENT = 'THIS SILVER TABLE STORES INFORMATION ABOUT LOW-LEVEL INVOICES IN OUR FINANCES SYSTEM. 
INCLUDES DETAILS SUCH AS INVOICE DATE, AMOUNT DUE, PAYMENT STATUS, AND TAX INFORMATION. FIELDS 
RELATED TO NETSUITE INTEGRATION ARE ALSO PRESENT.'
CLUSTER BY (SUPPLIER_ID, CREATED_AT)
;
