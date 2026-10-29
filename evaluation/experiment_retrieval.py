"""Compare similarity k=3, similarity k=8, and MMR k=5 on labeled questions."""
import json, os
from pathlib import Path
from src.config import settings
from src.retrieval.vector_store import load_vector_store

def main():
    key=os.getenv('OPENAI_API_KEY')
    if not key: raise SystemExit('Set OPENAI_API_KEY before retrieval experiments.')
    store=load_vector_store(key,settings.vector_store_path,settings.embedding_model)
    cases=json.loads(Path('evaluation/test_questions.json').read_text(encoding='utf-8'))
    cases=[c for c in cases if c.get('ground_truth_source')!='none' and c.get('expected_key_fact')]
    strategies=[('similarity_k3',lambda q:store.similarity_search(q,k=3)),('similarity_k8',lambda q:store.similarity_search(q,k=8)),('mmr_k5',lambda q:store.max_marginal_relevance_search(q,k=5,fetch_k=15))]
    rows=[]
    for name,fn in strategies:
        hit=0; judged=0
        for c in cases:
            docs=fn(c['question']); fact=c['expected_key_fact'].lower(); expected=[x.strip() for x in c.get('ground_truth_source','').split(';')]
            found=any(fact in d.page_content.lower() and (not expected or Path(str(d.metadata.get('source',''))).name in expected) for d in docs)
            hit+=int(found); judged+=1
        rows.append({'strategy':name,'questions':judged,'hits':hit,'hit_rate':round(hit/judged,4) if judged else None})
    out=Path('evaluation/results');out.mkdir(parents=True,exist_ok=True)
    (out/'retrieval_experiment.json').write_text(json.dumps({'method':'A question is a hit only when top-k includes the expected key fact and one expected source file.','results':rows},indent=2),encoding='utf-8')
    md=['| Strategy | Questions | Hits | Hit rate |','|---|---:|---:|---:|']+[f"| {r['strategy']} | {r['questions']} | {r['hits']} | {r['hit_rate']} |" for r in rows]
    (out/'retrieval_experiment.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print('\n'.join(md))
if __name__=='__main__':main()
