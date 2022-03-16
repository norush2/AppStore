# Construct the URI from the .env
DB_HOST=ec2-3-212-45-192.compute-1.amazonaws.com
DB_NAME=d4m91rllesgpia
DB_USER=jtskawfvzioxdv
DB_PORT=5432
DB_PASSWORD=ef7611b099d9734171641665e3363d0f20fe2fa802a1f6d73f3f51713a9dd316

while IFS= read -r line
do
  if [[ $line == DB_HOST* ]]
  then
    DB_HOST=$(cut -d "=" -f2- <<< $line | tr -d \')
  elif [[ $line == DB_NAME* ]]
  then
    DB_NAME=$(cut -d "=" -f2- <<< $line | tr -d \' )
  elif [[ $line == DB_USER* ]]
  then
    DB_USER=$(cut -d "=" -f2- <<< $line | tr -d \' )
  elif [[ $line == DB_PORT* ]]
  then
    DB_PORT=$(cut -d "=" -f2- <<< $line | tr -d \')
  elif [[ $line == DB_PASSWORD* ]]
  then
    DB_PASSWORD=$(cut -d "=" -f2- <<< $line | tr -d \')
  fi
done < ".env"

URI="postgres://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"

# Run the scripts to insert data.
psql ${URI} -f sql/AppStoreClean.sql
psql ${URI} -f sql/AppStoreSchema.sql
psql ${URI} -f sql/AppStoreCustomers.sql
psql ${URI} -f sql/AppStoreGames.sql
psql ${URI} -f sql/AppStoreDownloads.sql
