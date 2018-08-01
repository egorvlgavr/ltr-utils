#!/usr/bin/env bash

curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"rank",
     "type":"int"
  },
  "add-field":{
     "name":"qid",
     "type":"int"
   },
   "add-field":{
     "name":"query",
     "type":"string"
   },
   "add-copy-field":{
     "source":"query",
     "dest":[ "query_txt_en"]
   },
   "add-field":{
     "name":"product_id",
     "type":"string"
   },
   "add-field":{
     "name":"on_sale",
     "type":"float"
   },
   "add-field":{
     "name":"bm25_score",
     "type":"float"
   }
}' http://localhost:8983/solr/trainingset/schema