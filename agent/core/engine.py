import threading
from ..traps.ssh_trap import start_ssh_trap
from ..traps.web_trap import start_web_trap
from ..traps.generic_trap import start_generic_trap

class MirageEngine:
    def __init__(self, free_ports):
        self.free_ports = free_ports
        self.threads = []

    def start(self):
        for port in self.free_ports:
            if port == 22:
                target = start_ssh_trap
            elif port == 80:
                target = start_web_trap
            else:
                target = start_generic_trap
            
            t = threading.Thread(target=target, args=(port,), daemon=True)
            t.start()
            self.threads.append(t)
