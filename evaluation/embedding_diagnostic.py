"""Check model dimensions and pairwise cosine similarity of paraphrases vs unrelated queries."""
import json, os
from pathlib import Path
import numpy as np
from langchain_openai import OpenAIEmbeddings
from src.config import settings
TEXTS=[
 'The purifier makes three beeps and its red indicator flashes.',
 'My water purifier gives three audible alerts and a blinking red light.',
 'How can I update the delivery address for my order?',
]
def main():
 key=os.getenv('OPENAI_API_KEY')
 if not key: raise SystemExit('Set OPENAI_API_KEY before embedding diagnostic.')
 model=OpenAIEmbeddings(api_key=key,model=settings.embedding_model)
 vec=np.asarray(model.embed_documents(TEXTS),dtype=float); norm=vec/(np.linalg.norm(vec,axis=1,keepdims=True)+1e-12); sim=norm@norm.T
 result={'model':settings.embedding_model,'dimension':int(vec.shape[1]),'texts':TEXTS,'cosine_similarity':sim.round(4).tolist(),'interpretation':'The two paraphrases should be more similar to each other than either is to the unrelated order-address question; inspect actual values rather than assuming this outcome.'}
 out=Path('evaluation/results');out.mkdir(parents=True,exist_ok=True);(out/'embedding_diagnostic.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
