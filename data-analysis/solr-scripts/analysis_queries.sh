#!/usr/bin/env bash

curl http://localhost:8983/solr/trainingset/query -d 'q=*:*&rows=0&
 json.facet={
    mean_search_count : "avg(search_count)",
    max_search_count : "max(search_count)",
    min_search_count : "min(search_count)",

    mean_clicks : "avg(clicked)",
    max_clicks : "max(clicked)",
    min_clicks : "min(clicked)",

    mean_add_to_bag : "avg(add_to_bag)",
    max_add_to_bag : "max(add_to_bag)",
    min_add_to_bag : "min(add_to_bag)",

    mean_checked_out : "avg(checked_out)",
    max_checked_out : "max(checked_out)",
    min_checked_out : "min(checked_out)"
 }'


curl http://localhost:8983/solr/trainingset/query -d 'q=*:*&rows=0&
 json.facet={
 view_count_1_to_10 : {
    type : query,
    q : "productViewCount:[0 TO 10]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  },
  view_count_10_to_100 : {
    type : query,
    q : "productViewCount:{10 TO 100]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  },
  view_count_100_to_500 : {
    type : query,
    q : "productViewCount:{100 TO 500]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  },
  view_count_500_to_1000 : {
    type : query,
    q : "productViewCount:{500 TO 1000]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  },
  view_count_1000_to_5000 : {
    type : query,
    q : "productViewCount:{1000 TO 5000]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  },
  view_count_5000_to_10000 : {
    type : query,
    q : "productViewCount:{5000 TO 10000]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  },
  view_count_10000_to_50000 : {
    type : query,
    q : "productViewCount:{10000 TO 50000]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  }
}'


curl http://localhost:8983/solr/trainingset/query -d 'q=*:*&rows=0&
 json.facet={
 view_count_1_to_10 : {
    type : query,
    q : "productViewCount:[0 TO 10]",
    facet : {
        type: term,
        field: clicked
    }
  },
  view_count_10_to_100 : {
    type : query,
    q : "productViewCount:{10 TO 100]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  },
  view_count_100_to_500 : {
    type : query,
    q : "productViewCount:{100 TO 500]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  },
  view_count_500_to_1000 : {
    type : query,
    q : "productViewCount:{500 TO 1000]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  },
  view_count_1000_to_5000 : {
    type : query,
    q : "productViewCount:{1000 TO 5000]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  },
  view_count_5000_to_10000 : {
    type : query,
    q : "productViewCount:{5000 TO 10000]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  },
  view_count_10000_to_50000 : {
    type : query,
    q : "productViewCount:{10000 TO 50000]",
    facet : {
        avg_clicks : "avg(clicked)",
        max_clicks : "max(clicked)",
        min_clicks : "min(clicked)",
        mean_clicks: "percentile(clicked, 50)"
    }
  }
}'


curl http://localhost:8983/solr/trainingset/query -d 'q=*:*&rows=0&
 json.facet={
 view_count__0_to_10 : {
    type : query,
    q : "productViewCount:[0 TO 10]",
    facet : {
        clicks: {
            type: terms,
            field: clicked,
            limit: -1
        }
    }
  }
 }'