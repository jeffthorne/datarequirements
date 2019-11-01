from aqua.aqua import Aqua
import json


registry = 'Docker Hub' #friendly name for added registry in Aqua CSP
repo = 'ubuntu'
tag = '14.04'

aqua_username = 'username'
aqua_password = 'password'
aqua_host = 'mylo.uw.edu' # or '192.0.2.8'
port = '443'
using_tls = True # set to false if hitting http endpoint


aqua = Aqua(id=aqua_username, password=aqua_password, host=aqua_host, port=port, using_tls=using_tls)

registered_image = aqua.get_registered_image(registry=registry, repo=repo, tag=tag)
image_details = aqua.export_images([registered_image])['images'][0]

base_image = registered_image['parent']['name'] if 'parent' in registered_image else None
tag = registered_image['tag']
digest = registered_image['digest']
scanner = 'Aqua'

resources = image_details['imported_scan']['analysis']['resources']

scan_results = aqua.scan_results(registry_name=registry, image_name=repo, image_tag=tag)
cves_count = scan_results['cves_counts']
cves = scan_results['cves'] #contains all info: name, severity, solution, etc

#similar object to requirements outlined in DataRequirment.txt
data_object = dict(base_image=base_image, tag=tag, hash=digest, scanner='Aqua', components=resources, cves_count=cves_count, cves=cves)
print(json.dumps(data_object))