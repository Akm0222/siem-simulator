from flask import Flask, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Connect to Elasticsearch - running on localhost from Docker
es = Elasticsearch("http://localhost:9200")

@app.route('/')
def home():
    try:
        # Query for documents tagged as a threat
        query = {
            "query": {
                "match": {
                    "tags": "threat_detected"
                }
            },
            "sort": [
                { "@timestamp": "desc" }
            ],
            "size": 100 # Get the latest 100 alerts
        }
        
        resp = es.search(index="siem-logs-*", body=query)
        alerts = [hit['_source'] for hit in resp['hits']['hits']]

    except Exception as e:
        alerts = [{"message": f"Could not connect to Elasticsearch: {e}"}]

    return render_template('index.html', alerts=alerts)

if __name__ == '__main__':
    app.run(debug=True, port=5001)