
import hashlib
import requests as r
from tqdm import tqdm


res = r.get("http://www.w3schools.com/css/trolltunga.jpg", stream=True)
h = hashlib.md5()

pbar = tqdm(total=int(res.headers.get("Content-Length")), unit="B", unit_scale=True)
for chuck in res.iter_content(2048):
    h.update(chuck)
    pbar.update(len(chuck))

pbar.close()

print(h.hexdigest())

res = r.get("http://www.w3schools.com/css/trolltunga.jpg", stream=True)
h = hashlib.md5()
h.update(res.content)
print(h.hexdigest())

