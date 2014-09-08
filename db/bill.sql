CREATE TABLE IF NOT EXISTS 'bills' (
  'agency' text COLLATE utf8_bin NOT NULL,
  'sha' varchar(255) COLLATE utf8_bin NOT NULL,
  'sn' text COLLATE utf8_bin NOT NULL,
  'description' text COLLATE utf8_bin NOT NULL,
  'account_no' text COLLATE utf8_bin NOT NULL,
  'expense_heading' text COLLATE utf8_bin NOT NULL,
  'procurement_method' text COLLATE utf8_bin NOT NULL,
  'pan_no' text COLLATE utf8_bin NOT NULL,
  'vendor' text COLLATE utf8_bin NOT NULL,
  'application_date' text COLLATE utf8_bin NOT NULL,
  'amount' text COLLATE utf8_bin NOT NULL,
  'remarks' text COLLATE utf8_bin NOT NULL,
  'upload_datetime' text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;