import json
from django.conf import settings
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import csv

# from .zabbix_integration import ZabbixIntegration
import datetime, pytz
from .constants import LOCAL_TZ

from .mock_zabbix_integration import MockZabbixIntegration as ZabbixIntegration


class ScorecardView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_api_key()
        self.zabbix = ZabbixIntegration(settings.ZABBIX_HOST, settings.ZABBIX_API_KEY)
        self.config_data = self.load_config_data()

    def check_api_key(self):
        if not settings.ZABBIX_API_KEY:
            raise ValueError("The 'ZABBIX_API_KEY' has not been defined")

    def load_config_data(self):
        config_data = [
            {
                "tags_list": [{"tag": "SYSTEM", "value": "INTERNET"}],
                "port": "INTERFACE_1",
                "vlans": ["VLAN_1", "VLAN_2"],
                "items": ["bits received", "bits sent"],
                "history_type": "3",
            },
            {
                "tags_list": [{"tag": "SYSTEM", "value": "INTERNET"}],
                "port": "INTERFACE_2",
                "vlans": None,
                "items": ["bits received", "bits sent"],
                "history_type": "3",
            },
            {
                "tags_list": [{"tag": "SYSTEM", "value": "NAVEGACION"}],
                "port": None,
                "vlans": None,
                "items": [
                    "Squid: HTTP traffic received per second",
                    "Squid: HTTP traffic sent per second",
                ],
                "history_type": "0",
            },
            {
                "tags_list": [{"tag": "SYSTEM", "value": "SERVER_1"}],
                "port": None,
                "vlans": None,
                "items": [
                    "CPU utilization",
                ],
                "history_type": "3",
            },
            {
                "tags_list": [{"tag": "SYSTEM", "value": "SERVER_2"}],
                "port": None,
                "vlans": None,
                "items": [
                    "CPU utilization",
                ],
                "history_type": "3",
            },
            {
                "tags_list": [
                    {"tag": "class", "value": "os"},
                    {"tag": "SYSTEM", "value": "SYSTEM"},
                    {"tag": "target", "value": "linux"},
                ],
                "port": None,
                "vlans": None,
                "items": ["Pulse: Usuarios"],
                "history_type": "3",
            },
            {
                "tags_list": [{"tag": "SYSTEM", "value": "VPN"}],
                "port": None,
                "vlans": None,
                "items": ["GlobalProtect: Usuarios"],
                "history_type": "3",
            },
        ]
        return config_data

    def get_data_from_items(self, items):
        data = []
        for host_id, item_list in items.items():
            host_data = [
                {
                    "x": item["name"],
                    "value": history["value"],
                    "y": history["clock"],
                }
                for item in item_list
                for history in item.get("histories", [])
            ]
            data.append({"host_id": host_id, "data": host_data})
        return data

    def prepare_data_for_chart(self, raw_data):
        # Group the data by host and parameter
        grouped_data = {}
        for entry in raw_data:
            host_id = entry["host_id"]
            for item in entry["data"]:
                y = int(item["y"])
                if y > 0:
                    # Convert to datetime object in UTC
                    date_utc = datetime.datetime.utcfromtimestamp(y).replace(
                        tzinfo=pytz.utc
                    )
                    # Convert UTC time to local server time
                    date = date_utc.astimezone(LOCAL_TZ)

                    host_name, parameter_name = item["x"].split(": ")
                    key = f"{host_id} - {host_name} - {parameter_name}"

                    if key not in grouped_data:
                        grouped_data[key] = {
                            "labels": [],
                            "detailedLabels": [],
                            "values": [],
                        }

                    grouped_data[key]["labels"].append(date.strftime("%H:%M"))
                    grouped_data[key]["detailedLabels"].append(
                        date.strftime("%Y-%m-%d %H:%M:%S")
                    )
                    grouped_data[key]["values"].append(float(item["value"]))

        # Extract datasets from the grouped data
        datasets = []
        for key, data in grouped_data.items():
            datasets.append(
                {
                    "label": key,
                    "data": data["values"],
                }
            )

        # Find the maximum value
        all_values = [value for dataset in datasets for value in dataset["data"]]
        max_value = round(max(all_values)) if all_values else 0

        return {
            "datasets": datasets,
            "originalLabels": grouped_data[key]["labels"] if grouped_data else [],
            "maxValue": max_value,
            "groupedData": grouped_data,
        }

    def get(self, request):
        if "export" in request.GET and request.GET["export"] == "csv":
            return self.export_data_as_csv(request)

        # Get the time parameters from the form
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)

        if start_time and end_time:
            time_from = int(
                datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M").timestamp()
            )
            time_till = int(
                datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M").timestamp()
            )
        else:
            time_from = time_till = None

        data_names = [
            "internet_data",
            "network_data",
            "proxy_data",
            "vpn_data",
            "firewall_data",
        ]
        context = {}

        # Create a dictionary to store the export data for each plot
        export_data = {}

        for config, name in zip(self.config_data, data_names):
            ids = self.zabbix._get_host_ids_by_tag(config["tags_list"])
            items, itemids = self.zabbix._get_items_by_host_ids(
                ids,
                config["items"],
                config["port"],
                config["vlans"],
                history_type=config["history_type"],
                time_from=time_from,
                time_till=time_till,
            )
            raw_data = self.get_data_from_items(items)
            transformed_data = self.prepare_data_for_chart(raw_data)
            context[name] = json.dumps(transformed_data)
            export_data[name] = transformed_data

        request.session["export_data"] = export_data

        return render(request, "scorecard.html", context)

    def export_data_as_csv(self, request):
        export_data = request.session.get("export_data", {})
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="dades grafiques.csv"'
        writer = csv.writer(response)
        writer.writerow(["Gràfica", "Conjunt de dades", "Port", "Temps", "Valor(kbps)"])

        for graph_name, graph_data in export_data.items():
            for dataset in graph_data["datasets"]:
                label = dataset["label"]
                port = "N/A"  # Default port value

                for config in self.config_data:
                    if any(item for item in config.get("items", []) if item in label):
                        port = config.get("port", "N/A")
                        break  # Exit the loop once a matching port is found

                for value, timestamp in zip(
                    dataset["data"], graph_data["groupedData"][label]["detailedLabels"]
                ):
                    writer.writerow([graph_name, label, port, timestamp, round(value)])

        return response
