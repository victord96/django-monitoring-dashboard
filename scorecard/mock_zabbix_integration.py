import random
from datetime import datetime, timedelta
import pytz


class MockZabbixIntegration:
    def __init__(self, url, api_token):
        self.url = url
        self.api_token = api_token

    def _make_request(self, method, params):
        # Esta implementación de mock simplemente redirige a los métodos mock correspondientes
        if method == "host.get":
            return self._mock_host_get(params)
        elif method == "item.get":
            return self._mock_item_get(params)
        elif method == "history.get":
            return self._mock_history_get(params)
        # Agrega aquí más métodos si tu aplicación los utiliza

    def _mock_host_get(self, params):
        # Simula una respuesta de host.get con una lista de host IDs.
        return {
            "jsonrpc": "2.0",
            "result": [
                {"hostid": "10084"},
                {"hostid": "10085"},
            ],
        }

    def _mock_item_get(self, params):
        # Simula una respuesta de item.get con una lista de items.
        return {
            "jsonrpc": "2.0",
            "result": [
                {
                    "itemid": "23296",
                    "name": "Network traffic: bits received",
                    "lastvalue": "12345",
                    "lastclock": "1609459200",
                    "hostid": "10084",
                },
                {
                    "itemid": "23297",
                    "name": "Network traffic: bits sent",
                    "lastvalue": "67890",
                    "lastclock": "1609459200",
                    "hostid": "10085",
                },
                # Agrega más items mockeados según sea necesario
            ],
        }

    def _mock_history_get(self, params):
        # Simula una respuesta de history.get con datos históricos de los items.
        histories = []
        for _ in range(10):  # Genera 10 puntos de datos históricos
            histories.append(
                {
                    "itemid": random.choice(params["itemids"]),
                    "clock": str(int(datetime.now().timestamp())),
                    "value": str(random.randint(10000, 100000)),
                }
            )
        return {"jsonrpc": "2.0", "result": histories}

    def _get_host_ids_by_tag(self, tags):
        # Simula obtener IDs de host basados en etiquetas
        return ["10084", "10085"]

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
        # Esta es la estructura esperada basada en tu descripción
        mock_items = {
            "10084": [
                {
                    "itemid": "3001",
                    "name": "Network traffic: bits received",
                    "lastvalue": "500000",
                    "lastclock": str(
                        int((datetime.now() - timedelta(minutes=1)).timestamp())
                    ),
                    "hostid": "10084",
                    "histories": [
                        {
                            "value": str(random.randint(10000, 100000)),
                            "clock": str(
                                int((datetime.now() - timedelta(minutes=i)).timestamp())
                            ),
                        }
                        for i in range(10)
                    ],
                },
                # Repite la estructura para otros ítems si es necesario
            ],
            # Repite la estructura para otros hostids si es necesario
        }

        filtered_items = {host_id: mock_items.get(host_id, []) for host_id in host_ids}
        itemids = [
            item["itemid"] for sublist in filtered_items.values() for item in sublist
        ]

        return filtered_items, itemids

    def _obtain_required_items(
        self, item, port, vlans, history_type="3", time_from=None, time_till=None
    ):
        # Simula la lógica para filtrar y obtener los items requeridos
        return item  # En este mock, simplemente devolvemos el ítem

    def _get_history_by_item_ids(
        self, item_ids, history_type="3", time_from=None, time_till=None
    ):
        # Simula obtener el historial de los valores de los items
        return self._mock_history_get({"itemids": item_ids})
