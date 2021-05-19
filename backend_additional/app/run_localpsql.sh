#!/usr/bin/fish

docker run --rm --name localpsql_add -d -p 5433:5432 --env-file=localpsql.env -v data_add:/var/lib/postgresql/data postgres:12