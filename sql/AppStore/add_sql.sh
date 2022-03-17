psql $DATABASE_URL -f AppStoreClean.sql
psql $DATABASE_URL -f AppStoreSchema.sql
psql $DATABASE_URL -f AppStoreCustomers.sql
psql $DATABASE_URL -f AppStoreGames.sql
psql $DATABASE_URL -f AppStoreDownloads.sql