import os

from learning.pipeline import LearningPipeline, LearningProposal
from memory.store import PersonalMemory
from security.consent import Consent, ConsentManager, Purpose
from security.vault import EncryptedVault


def consent(mgr,purpose,category="conversation"):
    c=Consent("c1",purpose,True,frozenset({category})); mgr.record(c); return c

def test_vault_roundtrip_and_delete(tmp_path):
    key=os.urandom(32); v=EncryptedVault(tmp_path/"vault.json",key)
    v.put("r1",{"note":"private"},"c1")
    assert v.get("r1")=={"note":"private"}
    raw=(tmp_path/"vault.json").read_text()
    assert "private" not in raw
    assert v.delete("r1") and v.list_ids()==[]

def test_memory_requires_consent(tmp_path):
    mgr=ConsentManager(); mem=PersonalMemory(EncryptedVault(tmp_path/"v",os.urandom(32)),mgr)
    try: mem.save("r",{"x":1},"missing")
    except PermissionError: pass
    else: raise AssertionError("missing consent was accepted")

def test_learning_requires_sanitization():
    mgr=ConsentManager(); consent(mgr,Purpose.LEARNING_CONTRIBUTION,"task_history")
    p=LearningProposal("p","c1","task_history","generic example",True,True,True)
    assert LearningPipeline(mgr).propose(p)==p
