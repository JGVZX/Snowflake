truncate table companies;
truncate table founders;

copy into companies from @startups/Startups.csv
file_format = 'basic_csv';

copy into founders from @startups/Founders.csv
file_format = 'basic_csv';