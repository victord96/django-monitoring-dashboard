# Django Monitoring Dashboard

A web-based monitoring dashboard built with Django and JavaScript for retrieving, processing, and visualizing network monitoring data.

The application integrates with the Zabbix API to collect monitoring information and display it through interactive charts, providing a clearer view of network activity and historical data.

## Features

- Integration with the Zabbix API
- Host and item filtering
- Historical monitoring data retrieval
- Network traffic data processing
- Interactive data visualization
- Dynamic charts with Chart.js
- Filtering by tags and network interfaces
- Data aggregation and reporting
- Django-based backend

## Technologies

- Python
- Django
- JavaScript
- Chart.js
- Zabbix API
- HTML
- CSS

## How it works

The Django backend communicates with the Zabbix API to retrieve information about monitored hosts, items and historical metrics.

The retrieved data is filtered and processed before being sent to the frontend, where JavaScript and Chart.js are used to generate interactive visualizations.

The application can work with different monitored devices and interfaces, allowing network data to be organized and compared over time.

## Project structure

The project separates the monitoring logic, data processing and visualization layers:

- **Django** handles the backend and application logic.
- **Zabbix API** provides monitoring and historical data.
- **JavaScript** processes the data received by the frontend.
- **Chart.js** generates the interactive charts and visualizations.

## Purpose

This project was developed to simplify the visualization and analysis of monitoring data by providing a web interface on top of information retrieved from Zabbix.

It demonstrates practical experience working with Django, external APIs, data processing and frontend data visualization.
