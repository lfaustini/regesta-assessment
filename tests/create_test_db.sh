#!/bin/bash
set -eu

db_file="$(dirname "$0")/test-db.sqlite"

sqlite3 "$db_file" < db-schema.sql
sqlite3 "$db_file" < db-test-data.sql
