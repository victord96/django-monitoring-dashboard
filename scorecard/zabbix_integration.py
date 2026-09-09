import json
import requests
import re
from datetime import datetime, timedelta
import pytz


class ZabbixIntegration:
    def __init__(self, url, api_token):
        self.url = url
        self.headers = {"content-type": "application/json"}
        self.api_token = api_token

    def _make_request(self, method, params):
        data = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1,
            "auth": self.api_token,
        }

        response = requests.post(
            self.url, data=json.dumps(data), headers=self.headers, verify=False
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def _get_host_ids_by_tag(self, tags):
        params = {
            "output": ["hostid"],
            "tags": tags,
        }
        json_response = self._make_request("host.get", params)

        if json_response["result"]:
            hostids = [host["hostid"] for host in json_response["result"]]
            return hostids
        else:
            return []

    def _get_items_by_host_ids(
        self,
        host_ids,
        items,
        port,
        vlans,
        tags=None,
        history_type="3",
        time_from=None,
        time_till=None,
    ):
        params = {
            "output": [
                "name",
                "lastvalue",
                "lastclock",
                "itemid",
                "hostid",
            ],
            "hostids": host_ids,
            "search": {"name": items},
            "searchByAny": True,
        }

        if tags is not None:
            params["tags"] = tags

        json_response = self._make_request("item.get", params).get("result", [])

        # Initialize a dictionary to store items by host_id
        items_by_host_id = {}

        for item_info in json_response:
            # Get the host_id of the item
            host_id = item_info["hostid"]

            # If the host_id is not in the dictionary, initialize an empty list
            if host_id not in items_by_host_id:
                items_by_host_id[host_id] = []

            items_by_host_id[host_id].append(item_info)

        items_by_host_name = {}
        for host_id, item in items_by_host_id.items():
            items_by_host_id[host_id] = self._obtain_required_items(
                item, port, vlans, history_type, time_from, time_till
            )

            # Request the name of the host using the host_id
            host_params = {
                "output": ["host"],  # This should return the name of the hos
                "hostids": host_id,
            }
            host_json_response = self._make_request("host.get", host_params).get(
                "result", []
            )

            if len(host_json_response) > 0:
                host_name = host_json_response[0]["host"]
                items_by_host_name[host_name] = items_by_host_id[host_id]

        # Create a list of itemids
        itemids = [item_info["itemid"] for item_info in json_response]

        # Now items_by_host_name is a dictionary where the keys are the names of the hosts and the values are lists of items
        return items_by_host_name, itemids

    def _obtain_required_items(
        self, item, port, vlans, history_type="3", time_from=None, time_till=None
    ):
        # Obtain required items through items name of the json response
        port_pattern = f"Interface {port}" if port else None
        vlan_patterns = [f"VLAN {vlan}" for vlan in vlans] if vlans else []

        matching_items = [
            item_info
            for item_info in item
            if (not port_pattern or re.search(port_pattern, item_info["name"]))
            and (
                not vlan_patterns
                or any(
                    re.search(pattern, item_info["name"]) for pattern in vlan_patterns
                )
            )
        ]

        items_ids = [item["itemid"] for item in matching_items]
        histories = self._get_history_by_item_ids(
            items_ids, history_type, time_from, time_till
        )

        # assign data history to its corresponding item
        for item in matching_items:
            item["histories"] = [
                history for history in histories if history["itemid"] == item["itemid"]
            ]

        return matching_items

    def _get_history_by_item_ids(
        self, item_ids, history_type="3", time_from=None, time_till=None
    ):
        current_time = datetime.now()

        if time_from is None or time_till is None:
            # time from which we are going to across
            past_time = current_time - timedelta(hours=1)

            past_time_timestamp = int(past_time.timestamp())
            current_time_timestamp = int(current_time.timestamp())

        else:
            madrid_tz = pytz.timezone("Europe/Madrid")
            time_from_utc = madrid_tz.localize(
                datetime.fromtimestamp(time_from)
            ).astimezone(pytz.utc)
            time_till_utc = madrid_tz.localize(
                datetime.fromtimestamp(time_till)
            ).astimezone(pytz.utc)

            past_time_timestamp = int(time_from_utc.timestamp())
            current_time_timestamp = int(time_till_utc.timestamp())

        history = []

        params = {
            "output": "extend",
            "history": history_type,
            "itemids": item_ids,
            "time_from": past_time_timestamp,
            "time_till": current_time_timestamp,
        }

        response = self._make_request("history.get", params).get("result", [])

        history.extend(response)

        return history
