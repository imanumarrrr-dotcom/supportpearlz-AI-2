"""Run live RAG evaluation and save machine outputs plus an honest human-scoring worksheet."""
import json, os
from pathlib import Path
from src.config import settings
from src.retrieval.vector_store import load_vector_store
from src.chains.rag_chain import answer_question

def main():
    key=os.getenv('OPENAI_API_KEY')
    if not key: raise SystemExit('Set OPENAI_API_KEY before running live evaluation.')
    cases=json.loads(Path('evaluation/test_questions.json').read_text(encoding='utf-8'))
    store=load_vector_store(key,settings.vector_store_path,settings.embedding_model)
    results=[]
    for case in cases:
        try:
            output=answer_question(case['question'],[],store,key,settings.model,settings.temperature,settings.retrieval_k,settings.score_threshold)
            results.append({'id':case['id'],'category':case['category'],'question':case['question'],'expected_behaviour':case['expected_behaviour'],'ground_truth_source':case.get('ground_truth_source'),'expected_key_fact':case.get('expected_key_fact'),'output':output,'manual_scores':{'correctness':None,'groundedness':None,'citation_accuracy':None},'reviewer_notes':''})
        except Exception as exc:
            results.append({'id':case['id'],'category':case.get('category'),'question':case['question'],'error':str(exc),'manual_scores':{'correctness':None,'groundedness':None,'citation_accuracy':None},'reviewer_notes':'Investigate the pipeline error before scoring.'})
    out=Path('evaluation/results');out.mkdir(parents=True,exist_ok=True)
    answered=[r for r in results if 'output' in r]
    unanswerable_ids={c['id'] for c in cases if c.get('category')=='unanswerable'}
    unanswerable=[r for r in answered if r['id'] in unanswerable_ids]
    aggregate={'total_cases':len(cases),'completed_cases':len(answered),'runtime_errors':len(results)-len(answered),'unanswerable_cases':len(unanswerable),'unanswerable_refusals':sum(bool(r['output'].get('refused')) for r in unanswerable),'unanswerable_refusal_rate':(sum(bool(r['output'].get('refused')) for r in unanswerable)/len(unanswerable) if unanswerable else None),'hallucination_count':'REQUIRES_MANUAL_REVIEW','mean_correctness':'REQUIRES_MANUAL_REVIEW','mean_groundedness':'REQUIRES_MANUAL_REVIEW','mean_citation_accuracy':'REQUIRES_MANUAL_REVIEW'}
    payload={'model':settings.model,'embedding_model':settings.embedding_model,'aggregate':aggregate,'results':results}
    (out/'eval_results.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding='utf-8')
    rows=['| ID | Category | Expected source | Refused | Confidence | Correctness (0–2) | Groundedness (0–2) | Citation accuracy (0–2) | Reviewer notes |','|---|---|---|---|---|---:|---:|---:|---|']
    for r in results:
        o=r.get('output',{});scores=r.get('manual_scores',{})
        rows.append(f"| {r['id']} | {r.get('category','-')} | {r.get('ground_truth_source','-')} | {o.get('refused','error')} | {o.get('confidence','-')} | {scores.get('correctness')} | {scores.get('groundedness')} | {scores.get('citation_accuracy')} | {r.get('reviewer_notes','').replace('|','/')} |")
    rows += ['', '## Aggregate metrics', '', f"- Cases: {aggregate['total_cases']}; completed: {aggregate['completed_cases']}; runtime errors: {aggregate['runtime_errors']}", f"- Unanswerable refusal rate: {aggregate['unanswerable_refusal_rate']} (live measured output; manually inspect each refusal)", '- Hallucination count and quality scores must be filled after reviewing the actual answer and citations.', '', '## Scoring rubric', '- Correctness: 0 = wrong/unsupported fact; 1 = partly correct or incomplete; 2 = correct and appropriately qualified.', '- Groundedness: 0 = material unsupported claim; 1 = mostly supported with a questionable claim; 2 = every material claim supported by supplied context.', '- Citation accuracy: 0 = fabricated/irrelevant citations; 1 = partially relevant or incomplete; 2 = each cited source supports the associated claim.', '', '## Failure analysis worksheet', 'For every failed case, classify the earliest failing stage: ingestion, chunking, retrieval, context assembly, prompt/generation, schema validation, or citation validation. Record the supporting evidence and a targeted change. Do not assign a model/prompt fault until confirming that the needed source text was present in the assembled context.']
    (out/'eval_results.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print(json.dumps(aggregate,indent=2));print(f'Wrote {len(results)} cases to {out}')
if __name__=='__main__':main()
