#!/usr/bin/env python3
"""Draft-only Zenodo Sandbox client; deliberately has no action endpoints."""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, re, time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

BASE="https://sandbox.zenodo.org/api"
BUNDLE_NAME="fof-locomotor-capacity-cohort-0.1.0.zip"

class Stop(RuntimeError): pass
class Client:
    def __init__(self, token, opener=urlopen): self.token=token; self.opener=opener
    def request(self, method, url, body=None, content_type="application/json", retries=None):
        self.validate_operation(method, url, content_type)
        retries = 2 if retries is None and method == "GET" else (retries or 0)
        data = json.dumps(body).encode() if isinstance(body,(dict,list)) else body
        headers={"Authorization":f"Bearer {self.token}"}
        if data is not None: headers["Content-Type"]=content_type
        for attempt in range(retries+1):
            try:
                with self.opener(Request(url,data=data,headers=headers,method=method),timeout=60) as r:
                    final_url=r.geturl() if hasattr(r,"geturl") else url
                    self.validate_operation(method, final_url, content_type)
                    payload=r.read(); return json.loads(payload) if payload else None
            except HTTPError as e:
                if e.code==429 and attempt<retries: time.sleep(2**attempt); continue
                raise Stop(f"Sandbox request stopped with HTTP {e.code}") from None
            except (URLError,TimeoutError) as e: raise Stop("ambiguous Sandbox transport result; inspect state before retry") from None
    def validate_operation(self, method, url, content_type="application/json"):
        parsed=urlsplit(url)
        if parsed.scheme!="https" or parsed.hostname!="sandbox.zenodo.org" or parsed.username or parsed.password or parsed.port not in (None,443):
            raise Stop("request host/scheme is not approved Sandbox")
        path=parsed.path.rstrip("/") or "/"
        query=parsed.query
        draft=r"/api/deposit/depositions/[0-9]+"
        allowed=False
        if method=="GET":
            allowed=(path=="/api/licenses" and query=="q=MIT&size=10") or bool(re.fullmatch(draft+r"(?:/files)?",path))
        elif method=="POST": allowed=path=="/api/deposit/depositions" and not query
        elif method=="PUT":
            allowed=(bool(re.fullmatch(draft,path)) and content_type=="application/json") or (bool(re.fullmatch(r"/api/files/[A-Za-z0-9-]+/"+re.escape(BUNDLE_NAME),path)) and content_type=="application/octet-stream")
        elif method=="DELETE": allowed=bool(re.fullmatch(draft+r"/files/[A-Za-z0-9-]+",path)) and not query
        if not allowed: raise Stop("HTTP operation is outside the Sandbox draft-only allowlist")
    def license_preflight(self):
        result=self.request("GET",f"{BASE}/licenses/?q=MIT&size=10")
        hits=result.get("hits",{}).get("hits",[]) if result else []
        if not any(item.get("id")=="mit" and item.get("props",{}).get("scheme")=="spdx" for item in hits):
            raise Stop("MIT license preflight failed")
    def get_draft(self,did): return self.request("GET",f"{BASE}/deposit/depositions/{did}")
    def validate_draft(self,draft,did=None):
        if did is not None and str(draft.get("id"))!=str(did): raise Stop("draft id mismatch")
        if draft.get("state")!="unsubmitted" or draft.get("submitted") is not False: raise Stop("draft is not unpublished and editable")
    def validate_metadata(self,draft,intended):
        actual=draft.get("metadata",{})
        for key,value in intended.get("metadata",{}).items():
            if actual.get(key)!=value: raise Stop(f"draft metadata verification failed: {key}")
    def files(self,did): return self.request("GET",f"{BASE}/deposit/depositions/{did}/files")
    def delete_exact_bundle(self,draft):
        current=self.files(draft["id"])
        unexpected=[f for f in current if f.get("filename")!=BUNDLE_NAME]
        if unexpected: raise Stop("draft contains unexpected files; replacement stopped")
        matches=[f for f in current if f.get("filename")==BUNDLE_NAME]
        if len(matches)>1: raise Stop("expected prior bundle is not unique")
        if matches: self.request("DELETE",f'{BASE}/deposit/depositions/{draft["id"]}/files/{matches[0]["id"]}')
    def upload(self,draft,bundle):
        bucket=draft.get("links",{}).get("bucket","")
        if not bucket.startswith("https://sandbox.zenodo.org/api/files/"): raise Stop("invalid or non-Sandbox bucket link")
        return self.request("PUT",f"{bucket}/{quote(BUNDLE_NAME)}",bundle.read_bytes(),"application/octet-stream")

def expected_md5(path): return hashlib.md5(path.read_bytes(), usedforsecurity=False).hexdigest()
def matching_upload(files,bundle):
    expected=expected_md5(bundle)
    matches=[]
    for item in files:
        checksum=str(item.get("checksum","")); checksum=checksum.removeprefix("md5:")
        if item.get("filename")==BUNDLE_NAME and item.get("filesize")==bundle.stat().st_size and checksum==expected:
            matches.append(item)
    return matches

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def attestation(draft,mode,bundle,source_sha,run_id):
    return {"sandbox_deposition_id":str(draft["id"]),"sandbox_draft_reference":f'https://sandbox.zenodo.org/deposit/{draft["id"]}',"source_commit_sha":source_sha,"workflow_run_id":str(run_id),"operation":mode,"state":"UNPUBLISHED_SANDBOX_DRAFT","bundle_sha256":digest(bundle),"timestamp":dt.datetime.now(dt.timezone.utc).isoformat()}
def failure_attestation(mode,draft_id,bundle,source_sha,run_id):
    safe_id=str(draft_id) if str(draft_id).isdigit() else "UNAVAILABLE"
    return {"sandbox_deposition_id":safe_id,"sandbox_draft_reference":f"https://sandbox.zenodo.org/deposit/{safe_id}" if safe_id!="UNAVAILABLE" else "UNAVAILABLE","source_commit_sha":source_sha,"workflow_run_id":str(run_id),"operation":mode,"state":"FAILED_CLOSED_NEEDS_VERIFICATION","bundle_sha256":digest(bundle),"timestamp":dt.datetime.now(dt.timezone.utc).isoformat()}

def execute(client,mode,confirmation,draft_id,metadata,bundle,operation_state=None):
    operation_state = operation_state if operation_state is not None else {}
    if draft_id:
        operation_state["draft_id"] = str(draft_id)
    client.license_preflight()
    if mode=="CREATE":
        if confirmation!="CREATE_SANDBOX_DRAFT" or draft_id: raise Stop("CREATE requires exact confirmation and no draft_id")
        draft=client.request("POST",f"{BASE}/deposit/depositions",metadata)
        operation_state["draft_id"] = str(draft.get("id", "")) if isinstance(draft, dict) else ""
        client.validate_draft(draft); client.validate_metadata(draft,metadata)
    elif mode=="UPDATE":
        if not draft_id or confirmation: raise Stop("UPDATE requires draft_id and no create confirmation")
        draft=client.get_draft(draft_id); client.validate_draft(draft,draft_id)
        draft=client.request("PUT",f"{BASE}/deposit/depositions/{draft_id}",metadata)
        client.validate_draft(draft,draft_id); client.validate_metadata(draft,metadata); client.delete_exact_bundle(draft)
    else: raise Stop("mode must be CREATE or UPDATE")
    try:
        client.upload(draft,bundle)
    except Stop as error:
        found=matching_upload(client.files(draft["id"]),bundle)
        if len(found)!=1: raise Stop(f"{error}; read-after-write did not prove success") from None
    found=matching_upload(client.files(draft["id"]),bundle)
    if len(found)!=1: raise Stop("uploaded bundle checksum verification failed")
    return draft

def main():
    p=argparse.ArgumentParser(); p.add_argument("--mode",required=True); p.add_argument("--create-confirmation",default=""); p.add_argument("--draft-id",default=""); p.add_argument("--metadata",type=Path,required=True); p.add_argument("--bundle",type=Path,required=True); p.add_argument("--attestation",type=Path,required=True); p.add_argument("--source-sha",required=True); p.add_argument("--workflow-run-id",required=True); a=p.parse_args()
    token=os.environ.get("ZENODO_SANDBOX_TOKEN");
    if not token: raise Stop("ZENODO_SANDBOX_TOKEN is required")
    operation_state={"draft_id":a.draft_id}
    try:
        draft=execute(Client(token),a.mode,a.create_confirmation,a.draft_id,json.loads(a.metadata.read_text()),a.bundle,operation_state)
    except Stop:
        a.attestation.write_text(json.dumps(failure_attestation(a.mode,operation_state["draft_id"],a.bundle,a.source_sha,a.workflow_run_id),indent=2)+"\n")
        raise
    a.attestation.write_text(json.dumps(attestation(draft,a.mode,a.bundle,a.source_sha,a.workflow_run_id),indent=2)+"\n")
    print(f"SANDBOX_DRAFT_OPERATION=PASS mode={a.mode} state=UNPUBLISHED_SANDBOX_DRAFT")
if __name__=="__main__": main()
