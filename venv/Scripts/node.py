from flask import Flask, request, jsonify
import os, threading, time
from vclock import VectorClock

app = Flask(__name__)

NODE_ID = os.environ.get("NODE_ID")
ALL_NODES = os.environ.get("ALL_NODES", "A,B,C").split(',')
PORT = int(os.environ.get("PORT", 5000))
vc = VectorClock(NODE_ID, ALL_NODES)
data_store = {}
buffer = []

@app.route("/put", methods=["POST"])
def put():
 payload = request.json
 key = payload['key']
 value = payload['value']
 recv_vc = payload['vector_clock']
 sender = payload['sender']

 if vc.is_causally_ready(recv_vc, sender):
    vc.update(recv_vc)
    data_store[key] = (value, recv_vc)
    return jsonify({"status": "applied", "vc": vc.clock})
 else:
    buffer.append(payload)
    return jsonify({"status": "buffered"})

@app.route("/get", methods=["GET"])
def get():
 key = request.args.get('key')
 return jsonify({"value": data_store.get(key, None), "vc": vc.clock})
def process_buffer():
 while True:
  for msg in buffer[:]:
   if vc.is_causally_ready(msg['vector_clock'], msg['sender']):
    buffer.remove(msg)
 vc.update(msg['vector_clock'])
 data_store[msg['key']] = (msg['value'], msg['vector_clock'])
 time.sleep(1)
if __name__ == "__main__":
 threading.Thread(target=process_buffer, daemon=True).start()
 app.run(host="0.0.0.0", port=PORT)