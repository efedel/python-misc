bash# createdb bgo_db
bash# psql bgo_db < database_modules/schema/bgo_schema.sql
# ignore all NOTICE, CREATE, and INSERT messages -- look for ERROR
bash# dropdb bgo_db
