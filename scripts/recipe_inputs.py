import json
from pathlib import Path
LIMITS=json.loads((Path(__file__).resolve().parents[1]/"data/flyne-input-limits.json").read_text())
"""Reviewed reference counts shared by recipe pages and input index."""
MULTI_REFERENCE_COUNTS={'P015':2,'P023':2,'P058':3,'P082':2,'P085':2}
TRANSPARENT_OUTPUT_IDS={'P024','P083'}
def reference_count(recipe):
    return MULTI_REFERENCE_COUNTS.get(recipe['id'],1 if recipe.get('mode')=='edit' else 0)
