#!/usr/bin/env bash

curl -X GET \
  'http://localhost:8983/solr/trainingset/update?commit=true&indent=on&q=*:*&stream.body=<delete><query>*:*</query></delete>&wt=json'
