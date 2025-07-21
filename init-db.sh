#!/bin/bash
set -e

# Kiểm tra database 'data' đã tồn tại chưa, nếu chưa thì tạo
db_exists=$(psql -U "$POSTGRES_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='data'")
if [ "$db_exists" != "1" ]; then
  psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE data;"
fi