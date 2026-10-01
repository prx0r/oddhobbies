#!/usr/bin/env python3
import os, sqlite3, subprocess, sys
from pathlib import Path
ROOT = Path("/root/oddhobbies"); DB = ROOT/"db"/"oddhobbies.db"; ASSETS = ROOT/"assets"
def vault(key):
    return subprocess.check_output(["agent-vault","vault","credential","get",key,"--vault","oracle"], text=True).strip()
def main():
    env=os.environ.copy()
    env["AWS_ACCESS_KEY_ID"]=vault("R2_S3_ACCESS_KEY")
    env["AWS_SECRET_ACCESS_KEY"]=vault("R2_S3_SECRET_KEY")
    env["AWS_DEFAULT_REGION"]="auto"
    endpoint=vault("CLOUDFLARE_R2_ENDPOINT"); bucket=vault("R2_BUCKET"); prefix=vault("R2_REMOTE_PREFIX") or ""
    print("bucket", bucket, "prefix", prefix)
    for sub in ("etsy","local"):
        src=ASSETS/sub
        if not src.is_dir(): continue
        dest=f"s3://{bucket}/{prefix}/oddhobbies/assets/{sub}/"
        subprocess.check_call(["aws","s3","sync",str(src),dest,"--endpoint-url",endpoint,"--only-show-errors"], env=env)
    conn=sqlite3.connect(DB); conn.row_factory=sqlite3.Row; n=0
    for r in conn.execute("SELECT id, path_or_url FROM assets WHERE path_or_url LIKE '/%'"):
        p=Path(r["path_or_url"]); rel=str(p)
        key=f"{prefix}/oddhobbies/assets/{rel[len(str(ASSETS))+1:]}" if rel.startswith(str(ASSETS)+"/") else f"{prefix}/oddhobbies/assets/{p.name}"
        conn.execute("UPDATE assets SET storage='r2', path_or_url=? WHERE id=?", (f"r2://{bucket}/{key}", r["id"])); n+=1
    conn.commit(); print("updated", n); conn.close(); return 0
if __name__=="__main__":
    sys.exit(main())
