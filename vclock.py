from typing import Self


class VectorClock:
 def __init__(self, node_id, all_nodes):
    self.node_id = node_id
    self.clock = {nid: 0 for nid in all_nodes}

 def increment(self):
    self.clock[self.node_id] += 1

 def update(self, received_clock):
    for node, timestamp in received_clock.items():
        self.clock[node] = max(self.clock[node], timestamp)
        self.increment()    
         
 def is_causally_ready(self, received_clock, sender_id):
    for node in self.clock:
        if node == sender_id:
         if received_clock[node] != self.clock[node] + 1:
            return False
        else:
            if received_clock[node] > self.clock[node]:
                return False
    return True
