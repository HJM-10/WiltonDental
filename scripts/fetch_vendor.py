"""Pinned, locally hosted Three.js modules and a development-only audit library."""
from urllib.request import urlopen
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]
FILES={
 'dist/assets/vendor/three.module.min.js':'https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.min.js',
 'dist/assets/vendor/three.core.min.js':'https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.core.min.js',
 'dist/assets/vendor/GLTFLoader.js':'https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/loaders/GLTFLoader.js',
 'dist/assets/utils/BufferGeometryUtils.js':'https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/utils/BufferGeometryUtils.js',
 'dist/assets/vendor/THREE-LICENSE.txt':'https://cdn.jsdelivr.net/npm/three@0.180.0/LICENSE',
 'tmp/axe.min.js':'https://cdn.jsdelivr.net/npm/axe-core@4.10.3/axe.min.js',
}
def get(item):
    name,url=item;dest=ROOT/name;dest.parent.mkdir(parents=True,exist_ok=True)
    with urlopen(url,timeout=45) as r: dest.write_bytes(r.read())
    print(name,dest.stat().st_size)
list(ThreadPoolExecutor(6).map(get,FILES.items()))
