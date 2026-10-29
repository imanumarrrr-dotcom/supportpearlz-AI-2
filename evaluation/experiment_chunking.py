"""Measure six chunk configurations with real embedding retrieval.
Run from the project root after installing requirements and setting OPENAI_API_KEY.
Results are measurements from the configured embedding model, not synthetic estimates.
"""
import json, os, time
from pathlib import Path
import numpy as np
from langchain_openai import OpenAIEmbeddings
from src.config import settings
from src.ingestion.loaders import load_documents
from src.ingestion.chunking import split_documents

CONFIGS = [(400, 0), (400, 80), (800, 0), (800, 120), (1200, 0), (1200, 180)]

def main():
    key = os.getenv('OPENAI_API_KEY')
    if not key: raise SystemExit('Set OPENAI_API_KEY before running measured chunking experiments.')
    docs, ingestion = load_documents(settings.knowledge_base_path)
    cases = json.loads(Path('evaluation/test_questions.json').read_text(encoding='utf-8'))
    answerable = [c for c in cases if c.get('ground_truth_source') != 'none' and c.get('expected_key_fact')]
    embedder = OpenAIEmbeddings(api_key=key, model=settings.embedding_model)
    queries = embedder.embed_documents([c['question'] for c in answerable])
    results=[]
    for size, overlap in CONFIGS:
        started=time.perf_counter(); chunks=split_documents(docs, size, overlap)
        vectors=embedder.embed_documents([c.page_content for c in chunks])
        matrix=np.asarray(vectors, dtype=float); qmat=np.asarray(queries, dtype=float)
        matrix=matrix/(np.linalg.norm(matrix,axis=1,keepdims=True)+1e-12)
        qmat=qmat/(np.linalg.norm(qmat,axis=1,keepdims=True)+1e-12)
        hits=0; judged=0
        for case, qvec in zip(answerable, qmat):
            sims=matrix @ qvec; top=np.argsort(sims)[::-1][:4]
            fact=case['expected_key_fact'].lower()
            found=False
            for idx in top:
                text=chunks[int(idx)].page_content.lower()
                # Ground-truth source and key-fact presence are both checked, not similarity alone.
                src=Path(str(chunks[int(idx)].metadata.get('source',''))).name
                expected_sources=[x.strip() for x in case.get('ground_truth_source','').split(';')]
                if fact in text and (not expected_sources or src in expected_sources): found=True; break
            hits += int(found); judged += 1
        lengths=[len(c.page_content) for c in chunks]
        results.append({'chunk_size':size,'chunk_overlap':overlap,'chunks':len(chunks),'mean_chunk_chars':round(float(np.mean(lengths)),1),'max_chunk_chars':max(lengths,default=0),'answerable_cases_judged':judged,'answer_chunk_hit_at_4':hits,'hit_at_4':round(hits/judged,4) if judged else None,'elapsed_seconds':round(time.perf_counter()-started,2)})
        print(results[-1])
    out=Path('evaluation/results'); out.mkdir(parents=True,exist_ok=True)
    payload={'embedding_model':settings.embedding_model,'embedding_dimension':len(queries[0]) if queries else None,'method':'cosine similarity; top-4 chunks; hit requires expected key fact text and expected source filename','results':results}
    (out/'chunking_experiment.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    rows=['| Size | Overlap | Chunks | Mean chars | Max chars | Hit@4 | Seconds |','|---:|---:|---:|---:|---:|---:|---:|']
    rows += [f"| {r['chunk_size']} | {r['chunk_overlap']} | {r['chunks']} | {r['mean_chunk_chars']} | {r['max_chunk_chars']} | {r['hit_at_4']} | {r['elapsed_seconds']} |" for r in results]
    (out/'chunking_experiment.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
if __name__=='__main__': main()
