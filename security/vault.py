"""Encrypted local personal-data vault using authenticated AES-GCM.

The vault never stores the encryption key in the repository. Supply a 32-byte
key through the NIMO_VAULT_KEY environment variable as base64, or pass raw
bytes to EncryptedVault for embedding in a platform keychain adapter later.
"""
from __future__ import annotations

import base64, json, os, secrets
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY_ENV="NIMO_VAULT_KEY"

def generate_key() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("ascii")

def key_from_env() -> bytes:
    value=os.environ.get(KEY_ENV)
    if not value:
        raise RuntimeError(f"{KEY_ENV} is not set")
    try:
        key=base64.urlsafe_b64decode(value.encode("ascii"))
    except Exception as exc:
        raise ValueError("Invalid NIMO_VAULT_KEY encoding") from exc
    if len(key)!=32:
        raise ValueError("NIMO_VAULT_KEY must decode to 32 bytes")
    return key

class EncryptedVault:
    VERSION=1
    def __init__(self,path: str|Path,key: bytes|None=None):
        self.path=Path(path)
        self.key=key if key is not None else key_from_env()
        if len(self.key)!=32: raise ValueError("Vault key must be 32 bytes")

    def _load(self)->dict:
        if not self.path.exists(): return {"version":self.VERSION,"records":{}}
        raw=json.loads(self.path.read_text(encoding="utf-8"))
        if raw.get("version")!=self.VERSION: raise ValueError("Unsupported vault version")
        return raw

    def put(self, record_id:str, value:dict, consent_id:str)->None:
        if not record_id or not consent_id: raise ValueError("record_id and consent_id are required")
        plaintext=json.dumps({"consentId":consent_id,"value":value},separators=(",",":"),ensure_ascii=False).encode()
        nonce=secrets.token_bytes(12)
        aad=f"nimo-vault:v{self.VERSION}:{record_id}".encode()
        ciphertext=AESGCM(self.key).encrypt(nonce,plaintext,aad)
        data=self._load()
        data["records"][record_id]={"nonce":base64.b64encode(nonce).decode(),"ciphertext":base64.b64encode(ciphertext).decode(),"consentId":consent_id}
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.path.write_text(json.dumps(data,indent=2),encoding="utf-8")
        try: os.chmod(self.path,0o600)
        except OSError: pass

    def get(self, record_id:str)->dict:
        item=self._load()["records"].get(record_id)
        if not item: raise KeyError(record_id)
        aad=f"nimo-vault:v{self.VERSION}:{record_id}".encode()
        plain=AESGCM(self.key).decrypt(base64.b64decode(item["nonce"]),base64.b64decode(item["ciphertext"]),aad)
        return json.loads(plain)["value"]

    def delete(self,record_id:str)->bool:
        data=self._load()
        existed=record_id in data["records"]
        data["records"].pop(record_id,None)
        if existed: self.path.write_text(json.dumps(data,indent=2),encoding="utf-8")
        return existed

    def list_ids(self)->list[str]:
        return sorted(self._load()["records"])
