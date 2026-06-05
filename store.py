"""申し込み済み抽選の永続化（ローカルJSON）。

Mac常駐Botが読み書きする。個人管理用なのでグローバル（誰が押しても共有）。
構造: { "<uid>": {"label": 店舗, "product": 商品, "end": 締切, "at": 申込日時} }
"""
from __future__ import annotations

import json
import os
from pathlib import Path

APPLIED_PATH = Path(os.environ.get("APPLIED_PATH", "applied.json"))


def _load() -> dict:
    if APPLIED_PATH.exists():
        try:
            return json.loads(APPLIED_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def _save(d: dict) -> None:
    APPLIED_PATH.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def is_applied(uid: str) -> bool:
    return uid in _load()


def toggle(uid: str, label: str, product: str, end: str, at: str) -> bool:
    """申込済み⇔未申込をトグル。トグル後に「申込済みか」を返す。"""
    d = _load()
    if uid in d:
        del d[uid]
        applied = False
    else:
        d[uid] = {"label": label, "product": product, "end": end, "at": at}
        applied = True
    _save(d)
    return applied


def list_applied() -> dict:
    return _load()
