'''You can input a query or a question. The script then uses semantic search to find relevant passages in Simple English Wikipedia (as it is smaller and fits better in RAM).

For semantic search, we use SentenceTransformer('multi-qa-MiniLM-L6-cos-v1') and retrieve 32 potentially passages that answer the input query.

Next, we use a more powerful CrossEncoder (cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')) that scores the query and all retrieved passages for their relevancy. The cross-encoder further boost the performance, especially when you search over a corpus for which the bi-encoder was not trained for.'''

import os
import pandas as pd
import csv

def readcsvData(input):
  data_d = {}
  # data_d
  with open(input) as f:
    reader = csv.DictReader(f)
    for row in reader:
      # print(row)
      # clean_row = [(k, preProcess(v)) for (k, v) in row.items()]
      # print(list(row.keys())[0])
      id_name = list(row.keys())[0]
      row_id = int(row[id_name])
      data_d[row_id] = dict(row.items())
    return data_d
    
def get_data():
  inputf = ''
  if inputf != '':
    inputfile = readData(inputf)
    st.write('Importing Data...')
    inputfile = readcsvData(inputf)