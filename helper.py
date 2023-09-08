# helper functions
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import pickle

import io

class CPU_Unpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'torch.storage' and name == '_load_from_bytes':
            return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
        else:
        return super().find_class(module, name)

#contents = pickle.load(f) becomes...
# contents = CPU_Unpickler(f).load()
with open("./data/embeddings_090823.pkl", "rb") as f:
    corpus_embeddings = CPU_Unpickler(f).load()
# corpus_embeddings=torch.load(embeddingspickle)

# load the dataset(knowledge base)
dataset = pd.read_csv("./data/formatted_corpus.csv")

# load a sentence-transformer model
bi_encoder = SentenceTransformer('paraphrase-distilroberta-base-v1')
bi_encoder.max_seq_length = 256     #Truncate long passages to 256 tokens
top_k = 32                          #Number of passages we want to retrieve with the bi-encoder

#The bi-encoder will retrieve 100 documents. We use a cross-encoder, to re-rank the results list to improve the quality
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# encode queries from knowledge base to create corpus embeddings
passages=dataset['Sentence'].tolist()
# corpus_embeddings = bi_encoder.encode(passages, convert_to_tensor=True, show_progress_bar=True)

# lets put it all together
def get_query_responses(query, top_k):
    '''find the closest `top_k` queries of the corpus for the user query based on cosine similarity'''
    
    ##### Sematic Search #####
    # Encode the query using the bi-encoder and find potentially relevant passages
    query_embedding = bi_encoder.encode(query, convert_to_tensor=True)
    # query_embedding = question_embedding.cuda()
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)
    hits = hits[0]  # Get the hits for the first query

    ##### Re-Ranking #####
    # Now, score all retrieved passages with the cross_encoder
    cross_inp = [[query, passages[hit['corpus_id']]] for hit in hits]
    cross_scores = cross_encoder.predict(cross_inp)

    # Sort results by the cross-encoder scores
    for idx in range(len(cross_scores)):
        hits[idx]['cross-score'] = cross_scores[idx]

    # Output of top-5 hits from bi-encoder
    print("\n-------------------------\n")
    print("Top-3 Bi-Encoder Retrieval hits")
    hits = sorted(hits, key=lambda x: x['score'], reverse=True)
    for hit in hits[0:top_k]:
        print("\t{:.3f}\t{}\t{}".format(hit['score'], dataset.iloc[hit['corpus_id'],2],passages[hit['corpus_id']].replace("\n", " ")))

    # Output of top-5 hits from re-ranker
    print("\n-------------------------\n")
    print("Top-3 Cross-Encoder Re-ranker hits")
    hits = sorted(hits, key=lambda x: x['cross-score'], reverse=True)
    results_dict = {}
    n=1
    for hit in hits[0:top_k]:
        # print("\t{:.3f}\t{}\t{}".format(, ,passages[hit['corpus_id']].replace("\n", " ")))
        entry={n:{'score':hit['cross-score'],'true_id':dataset.iloc[hit['corpus_id'],2],'sentence':passages[hit['corpus_id']]}}
        results_dict.update(entry)
        n+=1
    # use cosine-similarity and torch.topk to find the highest `top_k` scores
    # cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    # top_results = torch.topk(cos_scores, k=min(top_k, dataset.shape[0]))
    
    # filter dataframe by list of index
    # df = dataset.iloc[hits[1], :]
    
    # add matched score
    # df['Score'] = ["{:.4f}".format(value) for value in top_results[0]]
    
    # select top_k responses
    # responses = df.to_dict('records')
    
    return results_dict
