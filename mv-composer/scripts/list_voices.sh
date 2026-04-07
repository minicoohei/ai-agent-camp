#!/bin/bash
set -euo pipefail
source "$(dirname "$0")/../../.env"
curl -s "https://api.elevenlabs.io/v1/voices" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for v in data.get('voices', []):
    labels = v.get('labels', {})
    name = v.get('name','')
    vid = v.get('voice_id','')
    lang = labels.get('language','')
    accent = labels.get('accent','')
    desc = labels.get('description','')
    age = labels.get('age','')
    gender = labels.get('gender','')
    use = labels.get('use_case','')
    print(f'{vid} | {name} | {gender} | {age} | {desc} | {use} | {lang}/{accent}')
"
