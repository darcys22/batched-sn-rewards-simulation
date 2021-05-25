#!/usr/bin/python3

import requests
import argparse
import json


def instruct_daemon(method, params):
    payload = json.dumps({"method": method, "params": params}, skipkeys=False)
    print(payload)
    headers = {'content-type': "application/json"}
    try:
        response = requests.request("POST", "http://public.loki.foundation:22023/json_rpc", data=payload, headers=headers)
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print(e)
    except:
        print('No response from daemon, check daemon is running on this machine')


# curl -X POST http://127.0.0.1:38157/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_service_nodes", “params”: {“service_node_pubkeys”: []}}' -H 'Content-Type: application/json'
params = {"service_node_pubkeys": []}
answer = instruct_daemon('get_service_nodes', params)

service_nodes = []
for node in answer['result']['service_node_states']:
    service_node = []
    for contributor in node['contributors']:
        service_node.append(contributor['address'])
    service_nodes.append(service_node)

contributors_save_file = open('contributors-dump.json', 'w+')
json.dump(service_nodes, contributors_save_file)


