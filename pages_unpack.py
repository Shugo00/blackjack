"""Reconstruct the verified Web candidate for GitHub Pages, without rebuilding."""
from pathlib import Path
import hashlib,json,shutil,zipfile

target=Path('_site').resolve()
target.mkdir(exist_ok=False)
for name in ('site.zip','third-party.zip'):
    with zipfile.ZipFile(name) as archive:
        for member in archive.namelist():
            if not (target/member).resolve().is_relative_to(target):
                raise ValueError('archive path outside site')
        archive.extractall(target)
shutil.copyfile('web-source.apk',target/'web-source.apk')
manifest=json.loads(Path('site-manifest.json').read_text(encoding='utf-8'))
files={p.relative_to(target).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
       for p in target.rglob('*') if p.is_file()}
assert files==manifest['files'],'site does not match the tested Web candidate'
print(f"Verified {len(files)} files for {manifest['version']}")
