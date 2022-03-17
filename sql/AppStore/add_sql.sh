psql $DATABASE_URL -f sql/AppStore/AppStoreClean.sql
psql $DATABASE_URL -f sql/AppStore/AppStoreSchema.sql
psql $DATABASE_URL -f sql/AppStore/AppStoreCustomers.sql
psql $DATABASE_URL -f sql/AppStore/AppStoreGames.sql
psql $DATABASE_URL -f sql/AppStore/AppStoreDownloads.sql