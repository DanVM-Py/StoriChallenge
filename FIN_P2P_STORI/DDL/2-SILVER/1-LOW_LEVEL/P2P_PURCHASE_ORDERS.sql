CREATE OR REPLACE TABLE STORI_SILVER_DB_PROD.PROCUREMENT_TO_PAY.LOW_LEVEL_P2P_PURCHASE_ORDERS (
  ID INT PRIMARY KEY COMMENT 'UNIQUE IDENTIFIER OF THE PURCHASE ORDER'
  , SUPPLIER_ID VARCHAR(200) COMMENT 'ID OF THE SUPPLIER ASSOCIATED WITH THE PURCHASE ORDER'
  , PO_NUMBER VARCHAR(200) COMMENT 'PURCHASE ORDER NUMBER'
  , ORDER_STATE VARCHAR(200) COMMENT 'STATE OF THE PURCHASE ORDER'
  , NETSUITE_ID VARCHAR(200) COMMENT 'NETSUITE ID ASSOCIATED WITH THE PURCHASE ORDER'
  , NETSUITE_ORDER_NUMBER VARCHAR(200) COMMENT 'NETSUITE ORDER NUMBER'
  , BUDGET_AMOUNT FLOAT COMMENT 'AMOUNT DUE FOR THE PURCHASE ORDERS'
  , LOADED_AT TIMESTAMP_TZ(9) COMMENT 'TIMESTAMP OF WHEN THE RECORD WAS LOADED INTO THE DATABASE'
)
COMMENT = 'THIS SILVER TABLE STORES INFORMATION ABOUT LOW-LEVEL PURCHASE ORDERS IN THE FINANCES SYSTEM. 
EACH PURCHASE ORDER CONTAINS DETAILS SUCH AS THE SUPPLIER ID, PURCHASE ORDER NUMBER, AND ORDER STATE. 
NETSUITE INFORMATION IS ALSO STORED FOR TRACKING PURPOSES. TIMESTAMPS ARE RECORDED FOR WHEN THE RECORD WAS LOADED INTO THE DATABASE.'
;
