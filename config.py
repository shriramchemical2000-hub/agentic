"""Configuration loading with inheritance and dotted-key overrides."""
import copy
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "default.yaml"


def _deep_merge(base: dict, new: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in new.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load_config(path=None, overrides=None) -> dict:
    """Load YAML config. A file may contain ``extends: default.yaml`` to inherit and override.

    ``overrides`` is a dict like {"data.source": "m5"}.
    """
    path = Path(path) if path else DEFAULT_CONFIG_PATH
    with open(path) as f:
        cfg = yaml.safe_load(f)
    parent = cfg.pop("extends", None)
    if parent:
        base = load_config(path.parent / parent)
        cfg = _deep_merge(base, cfg)
    for dotted, value in (overrides or {}).items():
        node = cfg
        keys = dotted.split(".")
        for key in keys[:-1]:
            node = node.setdefault(key, {})
        node[keys[-1]] = value
    return cfg


def periods_per_year(cfg: dict) -> int:
    return 52 if cfg["data"].get("frequency", "D") == "W" else 365
