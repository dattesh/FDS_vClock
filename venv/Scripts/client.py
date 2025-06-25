import requests, time
nodes = {
 'A': 'http://localhost:5000',
 'B': 'http://localhost:5001',
 'C': 'http://localhost:5002'
}
# Simulate a causally ordered PUT
vc1 = {'A': 1, 'B': 0, 'C': 0}
vc2 = {'A': 1, 'B': 1, 'C': 0}
print("Writing key1 from A")
r1 = requests.post(nodes['A'] + "/put", json={
 "key": "x",
 "value": "1",
 "vector_clock": vc1,
 "sender": "A"
})
print(r1.json())
time.sleep(1)
print("Writing key1 from B (dependent)")
r2 = requests.post(nodes['B'] + "/put", json={
 "key": "x",
 "value": "2",
 "vector_clock": vc2,
 "sender": "B"
})
print(r2.json())
