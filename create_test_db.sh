#!/bin/bash
set -eu

sqlite3 db.sqlite < db-schema.sql
sqlite3 db.sqlite < db-test-data.sql
