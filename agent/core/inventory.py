import psutil

def get_free_ports(target_ports):
    used = [conn.laddr.port for conn in psutil.net_connections() if conn.status == 'LISTEN']
    return [p for p in target_ports if p not in used]