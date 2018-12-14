#!/usr/bin/env bash

#calculate statistic on full tree
curl http://localhost:8983/solr/trainingset/query -d 'q=*:*&rows=0&
 json.facet={
    ranks: {
        type: terms,
        field: rank,
        sort: {index: asc}
    }
}'

#calculate statistic on feature threshold split
curl http://localhost:8983/solr/trainingset/query -d 'q=*:*&rows=0&
 json.facet={
    left_split : {
        type: query,
        q: "queryScore_feature:[* TO 0.53703195]",
        facet: {
            ranks: {
                type: terms,
                field: rank,
                sort: {index: asc}
            }
        }
    },
    right_split : {
        type: query,
        q: "queryScore_feature:{0.53703195 TO *]",
        facet: {
            ranks: {
                type: terms,
                field: rank,
                sort: {index: asc}
            }
        }
    }
}'