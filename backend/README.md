# Backend Documentation

## Setup

Run `python3 init_db.py` to initialize the sqlite3 database. Note the format of each column.

After initializing the database, run `python3 main.py` to run the main database server. This should show up on localhost:5000.

## Structs

The following datatypes can be found in the database structure. Certain fields are restricted to just these string values.

trips : tripType -> 'hiking', 'climbing', 'social', 'skiing', 'boating', 'other'

leaders : position -> 'member', 'president', 'vicePresident', 'treasurer', 'secretary', 'outreach', 'gearManager'

##### Gio 11/5/25