import hashlib

class ConsistentHashing:
    def __init__(self):
        self.RING_metadata = {}

    def hash(self, key):
        md5_hash = hashlib.md5(key.encode()).hexdigest()
        # md5_hash = int(md5_hash[:3], 16)
        if len(md5_hash) == 32:
            return md5_hash # For testing, just take one byte. Easier to check
        else:
            raise Exception('Error in hash. Not getting all the character. Error when sorting probably')


    def update_ring_intervals(self, ecsprint):
        ecsprint(f'Updating the ring')
        if len(self.RING_metadata) != 0:
            self.RING_metadata = {k: self.RING_metadata[k] for k in sorted(self.RING_metadata)}
            # sorted_hash_list = sorted(list_hash, key=lambda x: int(x, 16)) # Todo use it
            previous_hash = list(self.RING_metadata.keys())[-1]
            for key, values in self.RING_metadata.items():
                values[0] = previous_hash
                previous_hash = key
        else:
            ecsprint(f'No nodes. Ring not updated.')

    def new_node(self, kvs_data, id, handle_json_REPLY, ecsprint):
        ecsprint(f'Adding new node')
        new_hash = self.hash(f'{kvs_data[id]["host"]}:{kvs_data[id]["port"]}')
        kvs_data[id]['hash_key'] = new_hash

        if len(self.RING_metadata) > 0:
            old_ring = {}
            for key, value in self.RING_metadata.items():
                old_ring[key] = [value[0], value[1]]

            self.RING_metadata[new_hash] = [None, new_hash, kvs_data[id]["host"], kvs_data[id]["port"]]
            self.update_ring_intervals(ecsprint)

            for data in kvs_data.values():
                data['previous_hash'] = self.RING_metadata[data['hash_key']][0]

            old_hashes = list(old_ring.keys())
            next_hash = min(old_hashes)
            old_hashes.sort()
            for key in old_hashes:
                if key > new_hash:
                    next_hash = key
                    break
            for key, value in kvs_data.items():
                if value['hash_key'] == next_hash:
                    data = {
                        'interval': [old_ring[next_hash][0], new_hash],
                        'responsable': f'{kvs_data[id]["host"]}:{kvs_data[id]["port"]}'
                    }
                    handle_json_REPLY(sock=value['sock'], request=f'arrange_ring', data=data)
                    break

        elif len(self.RING_metadata) == 0:
            self.RING_metadata[new_hash] = [None, new_hash, kvs_data[id]["host"], kvs_data[id]["port"]]
            self.update_ring_intervals(ecsprint)
            for data in kvs_data.values():
                data['previous_hash'] = self.RING_metadata[data['hash_key']][0]
        else:
            ecsprint('Error. Node not added. Check')

    def remove_node(self, kvs_data, id, sock, handle_json_REPLY, ecsprint):
        ecsprint(f'Removing node {kvs_data[id]["name"]}')
        old_ring = {}
        for key, value in self.RING_metadata.items():
            old_ring[key] = [value[0], value[1]]
        del self.RING_metadata[kvs_data[id]['hash_key']]

        if len(self.RING_metadata) > 0:
            self.update_ring_intervals(ecsprint)

            new_hash = list(self.RING_metadata)
            new_hash.sort()
            next_bigger = min(new_hash)

            for hash in new_hash:
                if hash > kvs_data[id]['hash_key']:
                    next_bigger = hash
                    break

            for key, value in kvs_data.items():
                if value['hash_key'] == next_bigger:
                    data = {
                        'interval': [kvs_data[id]['previous_hash'], kvs_data[id]['hash_key']],
                        'responsable': f'{value["host"]}:{value["port"]}'
                    }
                    print('====== Removing node--> Sending reorganization')
                    handle_json_REPLY(sock=sock, request=f'arrange_ring', data=data)
                    break
        else:
            ecsprint(f'No other node to send the data')
            handle_json_REPLY(sock=sock, request=f'arrange_ring', data=None)















