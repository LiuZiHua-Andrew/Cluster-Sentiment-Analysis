{
  "views": {
    "all": {
      "map": "function(doc) { emit(doc.suburb, doc.polarity);}",
      "reduce": "function(keys, values) { return sum(values)/values.length }",
    }
  }
}
