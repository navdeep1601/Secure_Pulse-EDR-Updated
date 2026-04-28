import sys
import os
import time

# Allow importing from subfolders
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'traps'))

from core.inventory import get_free_ports
from core.engine import MirageEngine

TARGET_PORTS = [21, 22, 23, 80, 445, 3389]

if __name__ == "__main__":
    print("[*] SecurePulse Mirage: Initializing System...")
    free_ports = get_free_ports(TARGET_PORTS)
    
    engine = MirageEngine(free_ports)
    engine.start()
    
    print(f"[*] Engine Active. {len(free_ports)} Traps Deployed.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
