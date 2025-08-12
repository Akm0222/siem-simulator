# SIEM Simulator (Mini Splunk)

A functional Security Information and Event Management (SIEM) tool built with Python and the ELK Stack to ingest, parse, and visualize security logs in real-time. This project simulates a security monitoring environment, featuring custom threat detection and a live dashboard.

## Features

- **Log Generation**: A Python script using the `faker` library generates realistic, multi-format security logs (Apache access, SSH logins, firewall blocks).
- **Real-Time Data Ingestion**: Logs are sent directly from the Python script to Elasticsearch, ensuring a real-time data pipeline.
- **Data Indexing & Storage**: Elasticsearch is used to index, store, and provide fast search capabilities for all incoming log data.
- **Threat Detection**: The Python script includes logic to tag suspicious events, such as failed SSH logins and firewall drops, marking them as threats.
- **Interactive Dashboard**: Kibana is used to create a dynamic dashboard with multiple visualizations:
  - A metric showing the total count of log events.
  - A pie chart breaking down events by type (e.g., `ssh_auth`, `firewall_drop`).
  - A live "Threat Feed" table that only displays logs tagged as a threat.
  - (Optional) A map visualization to show the geographic origin of source IP addresses.

## Tech Stack

- **Data Generation**: Python
- **Database / Indexing**: Elasticsearch
- **Visualization / Dashboard**: Kibana
- **Containerization**: Docker & Docker Compose

## How to Run This Project

**Prerequisites:**
- Docker Desktop installed and running.
- Anaconda/Miniconda installed.

**1. Clone the Repository**
```bash
git clone https://github.com/your-username/siem-simulator.git
cd siem-simulator

2. Set Up the Python Environment
```bash
# Create and activate the conda environment
conda create --name siem-env python=3.12
conda activate siem-env

# Install required Python libraries
```bash
python -m pip install faker elasticsearch==8.9.0

3. Start the SIEM Backend (Terminal 1)
# This starts Elasticsearch and Kibana
```bash
docker compose up

4. Start the Log Generator (Terminal 2)
```bash
# Make sure you are in your activated conda environment
conda activate siem-env

# Navigate to the script's directory
cd python_log_generator

# Run the script to start sending data
python log_generator.py

5. Set Up Kibana
Open your browser and navigate to http://localhost:5601.
Go to Stack Management > Data Views and create a new data view with the index pattern siem-logs-*.
Go to the Discover tab to see your logs streaming in.
Go to the Dashboard tab to build your visualizations.
