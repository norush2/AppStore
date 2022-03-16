psql $DATABASE_URL -f sql/AppStoreClean.sql
psql $DATABASE_URL -f sql/AppStoreSchema.sql
psql $DATABASE_URL -f sql/AppStoreCustomers.sql
psql $DATABASE_URL -f sql/AppStoreGames.sql
psql $DATABASE_URL -f sql/AppStoreDownloads.sql