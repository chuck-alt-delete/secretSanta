#!/bin/bash

DATABASE="data/santa.db"
MIGRATIONS_FOLDER="data/migrations"

# Iterate over sorted .sql files in the folder
for file in $(ls $MIGRATIONS_FOLDER/*.sql | sort); do
    echo "Running migration: $file"
    sqlite3 $DATABASE < $file
    if [ $? -ne 0 ]; then
        echo "Error running migration: $file"
        exit 1
    fi
done

echo "All migrations executed successfully."
