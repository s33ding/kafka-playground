from flask import Flask, request, jsonify
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
import threading
from datetime import datetime

app = Flask(__name__)

# Kafka configuration
KAFKA_SERVERS = ['kafka-brokers:9092']

# Store consumed messages
consumed_messages = []

# Initialize producer
producer = None
kafka_connected = False

def get_producer():
    global producer, kafka_connected
    if producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None
            )
            kafka_connected = True
        except Exception as e:
            kafka_connected = False
            print(f"Kafka connection failed: {e}")
    return producer

# Consumer thread
def consume_messages():
    try:
        consumer = KafkaConsumer(
            'playground-topic',
            bootstrap_servers=KAFKA_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
            group_id='playground-consumer'
        )
        
        for message in consumer:
            consumed_messages.append({
                'timestamp': datetime.now().isoformat(),
                'topic': message.topic,
                'partition': message.partition,
                'offset': message.offset,
                'key': message.key.decode('utf-8') if message.key else None,
                'value': message.value
            })
            # Keep only last 50 messages
            if len(consumed_messages) > 50:
                consumed_messages.pop(0)
    except Exception as e:
        print(f"Consumer error: {e}")

# Start consumer thread
consumer_thread = threading.Thread(target=consume_messages, daemon=True)
consumer_thread.start()

@app.route('/kafka-src-app')
@app.route('/kafka-src-app/')
def home():
    status = "✅ Connected" if kafka_connected else "❌ Disconnected"
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>Kafka Playground</title></head>
    <body>
        <h1>🚀 Kafka Playground</h1>
        <p>Kafka Status: <strong>{status}</strong></p>
        <div>
            <h2>Send Message</h2>
            <input type="text" id="topic" placeholder="Topic" value="playground-topic">
            <input type="text" id="key" placeholder="Key (optional)">
            <textarea id="message" placeholder="Message" rows="3">{{
  "user": "demo",
  "action": "test",
  "timestamp": "{datetime.now().isoformat()}"
}}</textarea><br>
            <button onclick="sendMessage()">Send to Kafka</button>
            <button onclick="sendBatch()">Send 5 Messages</button>
        </div>
        <div>
            <h2>Topic Management</h2>
            <input type="text" id="newTopic" placeholder="New topic name" value="my-topic">
            <button onclick="createTopic()">Create Topic</button>
            <button onclick="listTopics()">List Topics</button>
            <div id="topics"></div>
        </div>
        <div id="result"></div>
        <script>
        function sendMessage() {{
            const topic = document.getElementById('topic').value;
            const key = document.getElementById('key').value;
            const message = document.getElementById('message').value;
            
            fetch('/kafka-src-app/send', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{topic, key, message}})
            }}).then(r => r.json()).then(data => {{
                document.getElementById('result').innerHTML = '<p><strong>' + data.status + '</strong></p>';
            }});
        }}
        
        function sendBatch() {{
            for(let i = 1; i <= 5; i++) {{
                setTimeout(() => {{
                    const message = JSON.stringify({{
                        batch_id: Date.now(),
                        message_num: i,
                        timestamp: new Date().toISOString()
                    }});
                    document.getElementById('message').value = message;
                    sendMessage();
                }}, i * 200);
            }}
        }}
        </script>
    </body>
    </html>
    '''

@app.route('/kafka-src-app/send', methods=['POST'])
def send():
    try:
        producer = get_producer()
        if not producer:
            return jsonify({'status': 'Error: Kafka not connected'})
        
        data = request.json
        topic = data.get('topic', 'playground-topic')
        key = data.get('key')
        message_text = data.get('message', '{}')
        
        # Parse message as JSON if possible
        try:
            message = json.loads(message_text)
        except:
            message = {'text': message_text}
        
        # Send to Kafka
        producer.send(topic, value=message, key=key if key else None)
        producer.flush()
        
        return jsonify({
            'status': f'✅ Message sent to topic "{topic}"' + (f' with key "{key}"' if key else '')
        })
    except Exception as e:
        return jsonify({'status': f'❌ Error: {str(e)}'})

@app.route('/kafka-src-app/health')
def health():
    return jsonify({
        'status': 'ok',
        'kafka_connected': kafka_connected,
        'kafka_servers': KAFKA_SERVERS
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
