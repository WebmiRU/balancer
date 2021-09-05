import json
import queue
import threading
import time

import docker


class Container:
    def __init__(self, attrs):
        self.id = attrs['Id']
        self.is_running = attrs['State']['Running']
        self.name = attrs['Name']

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Docker(threading.Thread):
    __containers = []
    updates_json = queue.Queue()

    def __init__(self):
        super().__init__()
        self.client = docker.from_env()

    def get(self, container_id: str):
        pass

    def get_all(self):
        pass

    def update_all_containers(self, try_counter=0):
        if try_counter > 0:
            print("TRY COUNTER %s" % try_counter)
            time.sleep(1)

        if try_counter > 10:  # FATAL ERROR
            pass

        self.__containers.clear()

        try:
            for container in self.client.containers.list(all=True):
                item = Container(container.attrs)
                self.__containers.append(item.json())

            # Заменить на список всех контейнеров в JSON-формате
            self.updates_json.put(None)
            print(self.__containers)
        except Exception as e:
            print("DOCKER NOT FOUND ALL ERR")
            print(e)
            self.update_all_containers(try_counter + 1)

    def events(self):
        for event in self.client.events(decode=True):
            try:
                if event.get('Type') == 'container':
                    container_attrs = self.client.containers.get(event.get('id')).attrs
                    container = Container(container_attrs)
                    self.updates_json.put(container)
                else:
                    print("EVENT TYPE: %s" % event.get('Type'))
            # except docker.errors.NotFound:
            except Exception as e:
                print("DOCKER NOT FOUND ERR")
                print(e)
                self.update_all_containers()

    def run(self):
        self.events()
