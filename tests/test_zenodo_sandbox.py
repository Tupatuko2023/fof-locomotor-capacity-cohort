import importlib.util, io, json, tempfile, unittest, zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError

ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
b=load("bundle","scripts/zenodo/build_cohort_bundle.py"); m=load("mapper","scripts/zenodo/map_cff_to_zenodo.py"); z=load("zenodo","scripts/zenodo/zenodo_sandbox_draft.py")
XLSX=ROOT/b.XLSX_PATH

def mutate_xlsx(target, replacements=None, extra=None, remove=None):
    replacements=replacements or {}; extra=extra or {}; remove=set(remove or ())
    with zipfile.ZipFile(XLSX) as src, zipfile.ZipFile(target,"w") as dst:
        for info in src.infolist():
            if info.filename not in remove: dst.writestr(info,replacements.get(info.filename,src.read(info.filename)))
        for name,payload in extra.items(): dst.writestr(name,payload)

class BundleTests(unittest.TestCase):
    def test_exact_allowlist_real_build_and_hashes(self):
        self.assertEqual(len(b.ALLOWLIST),31); self.assertEqual(len(b.ALLOWLIST),len(set(b.ALLOWLIST)))
        with tempfile.TemporaryDirectory() as td:
            bundle,digest=b.build(ROOT,Path(td)); self.assertEqual(digest,b.sha256(bundle)); b.verify_archive(bundle)
            with zipfile.ZipFile(bundle) as a:
                self.assertEqual(set(a.namelist()),set(b.ALLOWLIST+b.GENERATED)); self.assertEqual(len(a.read("SHA256SUMS").decode().splitlines()),31)
    def test_source_path_suffix_secret_and_symlink_rejections(self):
        for bad in ("../x","/x","GPT/x","outputs/x","AGENTS.md","safe/data.rds","safe/key.pem"):
            with self.assertRaises(ValueError): b.safe_member(bad)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); target=root/"target"; target.write_text("safe")
            with self.assertRaises(FileNotFoundError): b.validate_source_file("missing.txt",root/"missing.txt")
            link=root/"link"; link.symlink_to(target)
            with self.assertRaisesRegex(ValueError,"non-symlink"): b.validate_source_file("link",link)
            credentials=("Authorization: Bearer abcdef", "GITHUB_TOKEN=abcdef", "ZENODO_TOKEN=abcdef", "AWS_ACCESS_KEY_ID=ABCDEF", "SECRET=abcdef", "PASSWORD=abcdef", "-----BEGIN PRIVATE KEY-----")
            for i,value in enumerate(credentials):
                p=root/f"s{i}"; p.write_text(value)
                with self.assertRaisesRegex(ValueError,"secret-like"): b.validate_source_file(f"s{i}",p)
    def test_archive_duplicate_manifest_checksum_and_member_tampering(self):
        with tempfile.TemporaryDirectory() as td:
            bundle,_=b.build(ROOT,Path(td)); original=Path(td)/"original.zip"; original.write_bytes(bundle.read_bytes())
            cases=[("duplicate",None,"README.md",b"x"),("manifest","manifest.txt",None,b"wrong\n"),("checksum","SHA256SUMS",None,b"0"*64+b"  README.md\n"),("member","README.md",None,b"tampered")]
            for label,replace,extra,payload in cases:
                out=Path(td)/(label+".zip")
                with zipfile.ZipFile(original) as src, zipfile.ZipFile(out,"w") as dst:
                    for info in src.infolist(): dst.writestr(info,payload if info.filename==replace else src.read(info.filename))
                    if extra: dst.writestr(extra,payload)
                with self.assertRaises(ValueError,msg=label): b.verify_archive(out)

class XlsxTests(unittest.TestCase):
    def test_approved_fixture(self): b.validate_xlsx(XLSX)
    def test_all_contract_mutations_fail(self):
        with zipfile.ZipFile(XLSX) as src:
            wb=src.read("xl/workbook.xml"); sheet=src.read("xl/worksheets/sheet1.xml"); rel=src.read("xl/_rels/workbook.xml.rels")
        mutations={
            "wrong_sheet":({"xl/workbook.xml":wb.replace(b'Taul1',b'Other')},{}),
            "extra_sheet":({"xl/workbook.xml":wb.replace(b'</sheets>',b'<sheet name="X" sheetId="2" r:id="rId2"/></sheets>')},{}),
            "hidden_sheet":({"xl/workbook.xml":wb.replace(b' r:id=',b' state="hidden" r:id=')},{}),
            "hidden_row":({"xl/worksheets/sheet1.xml":sheet.replace(b'<row r="2"',b'<row r="2" hidden="1"')},{}),
            "hidden_col":({"xl/worksheets/sheet1.xml":sheet.replace(b'<sheetData>',b'<cols><col min="1" max="1" hidden="1"/></cols><sheetData>')},{}),
            "formula":({"xl/worksheets/sheet1.xml":sheet.replace(b'</c>',b'<f>1+1</f></c>',1)},{}),
            "wrong_column":({"xl/worksheets/sheet1.xml":sheet.replace(b'>ssn<',b'>name<')},{}),
            "participant_id":({"xl/worksheets/sheet1.xml":sheet.replace(b'SYNLOOKUPKEY001',b'010101-123N')},{}),
            "external_rel":({"xl/_rels/workbook.xml.rels":rel.replace(b'</Relationships>',b'<Relationship Id="rId2" Type="externalLink" Target="https://example.test" TargetMode="External"/></Relationships>')},{}),
            "irrelevant_synth":({"xl/worksheets/sheet1.xml":sheet.replace(b'SYN-K50-001',b'REAL-001')},{"customXml/item.xml":b'<x>SYNTH</x>'}),
        }
        extras={"comment":"xl/comments1.xml","custom":"customXml/item.xml","unexpected":"xl/theme/theme1.xml","macro":"xl/vbaProject.bin","embedded":"xl/embeddings/object.bin","external":"xl/externalLinks/externalLink1.xml"}
        with tempfile.TemporaryDirectory() as td:
            for label,(repls,extra) in mutations.items():
                p=Path(td)/(label+".xlsx"); mutate_xlsx(p,repls,extra)
                with self.assertRaises(ValueError,msg=label): b.validate_xlsx(p)
            for label,name in extras.items():
                p=Path(td)/(label+".xlsx"); mutate_xlsx(p,extra={name:b'<x/>'})
                with self.assertRaises(ValueError,msg=label): b.validate_xlsx(p)

class MappingTests(unittest.TestCase):
    def test_mapping_and_normalization(self):
        import yaml
        data=yaml.safe_load((ROOT/"CITATION.cff").read_text()); out=m.map_cff(data,"2026-08-13")["metadata"]
        self.assertEqual((out["upload_type"],out["publication_date"],out["license"]),("software","2026-08-13","mit"))
        self.assertEqual(out["creators"][0]["orcid"],"0009-0003-0217-8291"); self.assertEqual(out["related_identifiers"][0]["identifier"],data["repository-code"])

class FakeClient:
    def __init__(self,files=None): self.calls=[]; self.current={"id":7,"state":"unsubmitted","submitted":False,"metadata":{},"links":{"bucket":"https://sandbox.zenodo.org/api/files/b"}}; self.file=list(files or [])
    def license_preflight(self): self.calls.append("license")
    def request(self,method,url,body=None,*args):
        self.calls.append(method)
        if method=="POST": self.current["metadata"]=body["metadata"]; return self.current
        if method=="PUT" and "/deposit/" in url: self.current["metadata"]=body["metadata"]; return self.current
        if method=="DELETE": return None
    def validate_draft(self,draft,did=None): z.Client.validate_draft(self,draft,did)
    def validate_metadata(self,draft,intended): z.Client.validate_metadata(self,draft,intended)
    def get_draft(self,did): self.calls.append("get"); return self.current
    def delete_exact_bundle(self,draft): return z.Client.delete_exact_bundle(self,draft)
    def upload(self,draft,bundle): self.calls.append("upload"); self.file=[{"filename":z.BUNDLE_NAME,"filesize":bundle.stat().st_size,"checksum":"md5:"+z.expected_md5(bundle)}]
    def files(self,did): self.calls.append("files"); return self.file

class FlowTests(unittest.TestCase):
    def setUp(self): self.t=tempfile.TemporaryDirectory(); self.bundle=Path(self.t.name)/z.BUNDLE_NAME; self.bundle.write_bytes(b"x"); self.payload={"metadata":{"title":"x"}}
    def tearDown(self): self.t.cleanup()
    def test_create_update_and_mode_guards(self):
        c=FakeClient(); z.execute(c,"CREATE","CREATE_SANDBOX_DRAFT","",self.payload,self.bundle); self.assertEqual(c.calls,["license","POST","upload","files"])
        c=FakeClient(); z.execute(c,"UPDATE","","7",self.payload,self.bundle); self.assertIn("get",c.calls); self.assertIn("PUT",c.calls)
        for args in (("CREATE","",""),("UPDATE","",""),("UPDATE","CREATE_SANDBOX_DRAFT","7")):
            with self.assertRaises(z.Stop): z.execute(FakeClient(),*args,self.payload,self.bundle)
    def test_draft_and_metadata_mismatches_stop_before_upload(self):
        for change in ({"id":8},{"state":"done"},{"submitted":True}):
            c=FakeClient(); c.current.update(change)
            with self.assertRaises(z.Stop): z.execute(c,"UPDATE","","7",self.payload,self.bundle)
            self.assertNotIn("upload",c.calls)
        c=FakeClient()
        def bad(method,url,body=None,*args): c.calls.append(method); return {**c.current,"metadata":{"title":"wrong"}}
        c.request=bad
        with self.assertRaisesRegex(z.Stop,"metadata"): z.execute(c,"UPDATE","","7",self.payload,self.bundle)
        self.assertNotIn("upload",c.calls)
    def test_replacement_zero_one_multiple_and_delete_failure(self):
        empty=FakeClient(); empty.delete_exact_bundle(empty.current); self.assertEqual(empty.calls,["files"])
        one=FakeClient([{"filename":z.BUNDLE_NAME,"id":"f1"}]); one.delete_exact_bundle(one.current); self.assertEqual(one.calls,["files","DELETE"])
        many=FakeClient([{"filename":z.BUNDLE_NAME,"id":"1"},{"filename":z.BUNDLE_NAME,"id":"2"}])
        with self.assertRaises(z.Stop): many.delete_exact_bundle(many.current)
        failing=FakeClient([{"filename":z.BUNDLE_NAME,"id":"1"}])
        failing.request=lambda *a,**k: (_ for _ in ()).throw(z.Stop("delete failed"))
        with self.assertRaises(z.Stop): failing.delete_exact_bundle(failing.current)
        unexpected=FakeClient([{"filename":"other.zip","id":"x"}])
        with self.assertRaisesRegex(z.Stop,"unexpected"): unexpected.delete_exact_bundle(unexpected.current)
    def test_upload_failure_and_read_after_write(self):
        c=FakeClient(); c.upload=lambda *a: (_ for _ in ()).throw(z.Stop("ambiguous"))
        with self.assertRaisesRegex(z.Stop,"did not prove"): z.execute(c,"CREATE","CREATE_SANDBOX_DRAFT","",self.payload,self.bundle)
        state={}; c=FakeClient()
        def ambiguous(draft,bundle): c.file=[{"filename":z.BUNDLE_NAME,"filesize":1,"checksum":z.expected_md5(bundle)}]; raise z.Stop("ambiguous")
        c.upload=ambiguous; z.execute(c,"CREATE","CREATE_SANDBOX_DRAFT","",self.payload,self.bundle,state)
        self.assertEqual(state["draft_id"],"7")
    def test_create_failure_state_preserves_id_after_post(self):
        state={}; before=FakeClient(); before.request=lambda *a,**k: (_ for _ in ()).throw(z.Stop("POST failed"))
        with self.assertRaises(z.Stop): z.execute(before,"CREATE","CREATE_SANDBOX_DRAFT","",self.payload,self.bundle,state)
        self.assertEqual(z.failure_attestation("CREATE",state.get("draft_id",""),self.bundle,"abc","1")["sandbox_deposition_id"],"UNAVAILABLE")
        state={}; metadata=FakeClient(); metadata.validate_metadata=lambda *a: (_ for _ in ()).throw(z.Stop("metadata failed"))
        with self.assertRaises(z.Stop): z.execute(metadata,"CREATE","CREATE_SANDBOX_DRAFT","",self.payload,self.bundle,state)
        self.assertEqual(z.failure_attestation("CREATE",state["draft_id"],self.bundle,"abc","1")["sandbox_deposition_id"],"7")
        state={}; upload=FakeClient(); upload.upload=lambda *a: (_ for _ in ()).throw(z.Stop("upload failed")); upload.files=lambda *a: []
        with self.assertRaises(z.Stop): z.execute(upload,"CREATE","CREATE_SANDBOX_DRAFT","",self.payload,self.bundle,state)
        self.assertEqual(state["draft_id"],"7")
        state={}; readback=FakeClient(); readback.files=lambda *a: (_ for _ in ()).throw(z.Stop("read-back failed"))
        with self.assertRaises(z.Stop): z.execute(readback,"CREATE","CREATE_SANDBOX_DRAFT","",self.payload,self.bundle,state)
        self.assertEqual(state["draft_id"],"7")
    def test_update_failure_state_preserves_existing_id(self):
        state={}; c=FakeClient(); c.get_draft=lambda *a: (_ for _ in ()).throw(z.Stop("GET failed"))
        with self.assertRaises(z.Stop): z.execute(c,"UPDATE","","7",self.payload,self.bundle,state)
        self.assertEqual(z.failure_attestation("UPDATE",state["draft_id"],self.bundle,"abc","1")["sandbox_deposition_id"],"7")
    def test_get_put_and_post_failures_never_fallback(self):
        for mode,method in (("UPDATE","get"),("UPDATE","PUT"),("CREATE","POST")):
            c=FakeClient()
            if method=="get": c.get_draft=lambda did: (_ for _ in ()).throw(z.Stop("GET failed"))
            else:
                original=c.request
                c.request=lambda verb,*args,**kwargs: (_ for _ in ()).throw(z.Stop(f"{method} failed")) if verb==method else original(verb,*args,**kwargs)
            args=(mode,"" if mode=="UPDATE" else "CREATE_SANDBOX_DRAFT","7" if mode=="UPDATE" else "")
            with self.assertRaises(z.Stop): z.execute(c,*args,self.payload,self.bundle)
            self.assertNotIn("upload",c.calls)
    def test_redacted_attestation(self):
        a=z.attestation(FakeClient().current,"UPDATE",self.bundle,"abc","1"); text=json.dumps(a).lower()
        self.assertEqual(set(a),{"sandbox_deposition_id","sandbox_draft_reference","source_commit_sha","workflow_run_id","operation","state","bundle_sha256","timestamp"})
        for forbidden in ("token","authorization","bucket","doi","owner"): self.assertNotIn(forbidden,text)
        failed=z.failure_attestation("CREATE","",self.bundle,"abc","1"); self.assertEqual(failed["state"],"FAILED_CLOSED_NEEDS_VERIFICATION"); self.assertEqual(failed["sandbox_deposition_id"],"UNAVAILABLE")
        failed_with_id=z.failure_attestation("CREATE","7",self.bundle,"abc","1")
        self.assertEqual(failed_with_id["sandbox_deposition_id"],"7")
        for forbidden in ("token","authorization","bucket","doi","owner"): self.assertNotIn(forbidden,json.dumps(failed_with_id).lower())

class Response:
    def __init__(self,payload=b'{}',url='https://sandbox.zenodo.org/api/deposit/depositions/7'): self.payload=payload; self.url=url
    def __enter__(self): return self
    def __exit__(self,*a): pass
    def read(self): return self.payload
    def geturl(self): return self.url

class HttpTests(unittest.TestCase):
    def test_endpoint_method_and_redirect_allowlist(self):
        c=z.Client("fake",lambda req,timeout: Response(url=req.full_url))
        allowed=[("GET",z.BASE+"/licenses/?q=MIT&size=10","application/json"),("GET",z.BASE+"/deposit/depositions/7","application/json"),("GET",z.BASE+"/deposit/depositions/7/files","application/json"),("POST",z.BASE+"/deposit/depositions","application/json"),("PUT",z.BASE+"/deposit/depositions/7","application/json"),("PUT",z.BASE+"/files/abc/"+z.BUNDLE_NAME,"application/octet-stream"),("DELETE",z.BASE+"/deposit/depositions/7/files/f1","application/json")]
        for args in allowed: c.validate_operation(*args)
        denied=[("GET","https://zenodo.org/api/deposit/depositions/7"),("GET","https://evil.test/api/deposit/depositions/7"),("GET","http://sandbox.zenodo.org/api/deposit/depositions/7"),("POST",z.BASE+"/deposit/depositions/7/actions/publish"),("POST",z.BASE+"/deposit/depositions/7/actions/discard"),("POST",z.BASE+"/deposit/depositions/7/actions/newversion"),("POST",z.BASE+"/unexpected"),("PUT",z.BASE+"/unexpected"),("DELETE",z.BASE+"/deposit/depositions/7"),("PATCH",z.BASE+"/deposit/depositions/7")]
        for method,url in denied:
            with self.assertRaises(z.Stop,msg=url): c.validate_operation(method,url)
        redirect=z.Client("fake",lambda req,timeout: Response(url="https://evil.test/x"))
        with self.assertRaises(z.Stop): redirect.request("GET",z.BASE+"/deposit/depositions/7")
    def test_http_failures_and_bounded_429(self):
        for code in (403,404,409):
            def opener(req,timeout,code=code): raise HTTPError(req.full_url,code,"x",{},io.BytesIO())
            with self.assertRaises(z.Stop): z.Client("fake",opener).request("GET",z.BASE+"/deposit/depositions/7")
        calls=[]
        def rate(req,timeout): calls.append(1); raise HTTPError(req.full_url,429,"x",{},io.BytesIO())
        with self.assertRaises(z.Stop): z.Client("fake",rate).request("GET",z.BASE+"/deposit/depositions/7",retries=2)
        self.assertEqual(len(calls),3)
        for error in (URLError("timeout"),TimeoutError()):
            with self.assertRaisesRegex(z.Stop,"ambiguous"): z.Client("fake",lambda req,timeout,e=error: (_ for _ in ()).throw(e)).request("GET",z.BASE+"/deposit/depositions/7")
    def test_static_boundaries(self):
        text="\n".join((ROOT/p).read_text().lower() for p in (".github/workflows/zenodo_sandbox_draft.yml","scripts/zenodo/zenodo_sandbox_draft.py"))
        self.assertNotIn("actions/publish",text); self.assertNotIn("deposit:actions",text); self.assertNotIn("https://zenodo.org/api",text.replace("https://sandbox.zenodo.org/api",""))

if __name__=="__main__": unittest.main()
