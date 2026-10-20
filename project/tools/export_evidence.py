"""Export allowlisted real usage and measured budget arithmetic, never inputs."""

import json
import statistics
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from project.backend.app.config import EMBEDDING_MODEL
from project.backend.app.index import load

events = [json.loads(line) for line in (REPO / 'logs/runtime/events.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
real_generation = [event for event in events if event.get('model', '').startswith('dots-studio/')]
if not real_generation:
    raise SystemExit('No real provider evidence is available; refusing to invent usage.')
first = min(event['timestamp'] for event in real_generation)
real = [event for event in events if event.get('model') == EMBEDDING_MODEL or
        (event['timestamp'] >= first and
         (event.get('model') in {item['model'] for item in real_generation}
          or event.get('operation') == 'guidance'))]
folder = REPO / 'logs'
folder.mkdir(exist_ok=True)
(folder / 'verified-usage.jsonl').write_text(''.join(json.dumps(event) + '\n' for event in real), encoding='utf-8')

golden_path = REPO / 'evals/results/20261020T193257001485Z.json'
golden = json.loads(golden_path.read_text())
end = datetime.fromisoformat(golden['timestamp'])
start = end - timedelta(milliseconds=sum(case['elapsed_ms'] for case in golden['cases']))
selected_guidance = [event for event in real_generation if event['operation'] == 'guidance_generation'
                     and start <= datetime.fromisoformat(event['timestamp']) <= end]
last_feedback = [event for event in real_generation if event['operation'] == 'feedback'][-1:]
images = [event for event in real_generation if event['operation'] == 'extraction' and event.get('finish_reason') == 'stop']


def summarize(rows):
    def average(key):
        values = [row[key] for row in rows if isinstance(row.get(key), (int, float))]
        return round(statistics.mean(values), 2) if values else None
    return {'samples': len(rows), 'tokens_in_mean': average('tokens_in'), 'tokens_out_mean': average('tokens_out'),
            'elapsed_ms_mean': average('elapsed_ms'), 'cost_usd_mean': average('cost_usd'),
            'failures': sum(row.get('outcome') != 'success' for row in rows)}


summary = {'source': 'verified-usage.jsonl', 'generation_model': real_generation[-1]['model'],
           'feedback': summarize(last_feedback), 'guidance_latest_golden': summarize(selected_guidance),
           'extraction_completed': summarize(images),
           'all_real_generation': summarize(real_generation),
           'local_index_build': summarize([event for event in real if event['operation'] == 'embedding_index']),
           'monthly_workload': {'users': 20, 'feedback_per_user': 10, 'guidance_per_user': 10, 'imports_per_user': 1, 'total_requests': 420},
           'limits': ['Provider-reported costs only; hardware/hosting excluded.', 'Free capacity/quota is not guaranteed.',
                      'Guidance generation rows include the answerable case refused by citation checks.',
                      'Local embeddings use no provider tokens.', 'Not a ten-trial feedback latency study.']}
means = [summary[key]['cost_usd_mean'] for key in ('feedback', 'guidance_latest_golden', 'extraction_completed')]
summary['monthly_provider_cost_usd'] = round(20 * (10 * means[0] + 10 * means[1] + means[2]), 8) if all(value is not None for value in means) else None
(folder / 'budget-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
data = load()
manifest = {key: data[key] for key in ('model', 'dimension', 'corpus_hash')}
manifest['chunks'] = [{key: chunk[key] for key in ('id', 'document')} for chunk in data['chunks']]
(REPO / 'docs/evidence/index-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
