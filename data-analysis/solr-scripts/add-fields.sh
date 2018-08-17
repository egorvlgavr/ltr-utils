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
   "add-field":{
     "name":"search_count",
     "type":"int"
   },
   "add-field":{
     "name":"clicked",
     "type":"int"
   },
   "add-field":{
     "name":"add_to_bag",
     "type":"int"
   },
     "add-field":{
     "name":"checked_out",
     "type":"int"
   }
}' http://localhost:8983/solr/trainingset/schema