import shelve


import asyncio
# Open the shelf file
# with shelve.open('/Users/pedrorodriguezdeledesmajimenez/scripts/TUM_DatabasePractical/kvserver/kserver1/kserver1_storage.db') as shelf:
#     # Print all key-value pairs in the shelf
#     print("All key-value pairs:")
#     counter = 1
#     for key, value in shelf.items():
#         print(f"Item {counter}==> {key} | {value}")
#         counter += 1


class MyClass:
    def __init__(self):
        self.name = {}
        self.class2 = MyClass2(self.name)
        print(self.name)




class MyClass2:
    def __init__(self, name):
        self.name = name
        self.start_thread()

    def start_thread(self):
        self.name['k1']= 'p'


pedro = MyClass()

# async def greet(name):
#     print(f"Hello, {name}!")
#     # await asyncio.sleep(1)  # Simulate some async operation
#     print(f"Goodbye, {name}!")
#
# async def main():
#     tasks = [
#         asyncio.create_task(greet("Alice")),
#         asyncio.create_task(greet("Bob")),
#     ]
#
#     await asyncio.gather(*tasks)
#
# asyncio.run(main())
