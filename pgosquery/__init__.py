from multicorn import ForeignDataWrapper
import psutil
import socket


class PgOSQuery(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(PgOSQuery, self).__init__(options, columns)
        self.table_type = options.get("tabletype", "processes")
        self.columns = columns

    def execute(self, quals, columns):
        func = getattr(self, self.table_type)
        for v in func(quals, columns):
            yield v

    ###################################################################
    # Tables
    ###################################################################

    def processes(self, quals, columns):
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=self.columns.keys())
            except psutil.NoSuchProcess:
                pass
            else:
                yield pinfo

    def listening_ports(self, quals, columns):
        for proc in psutil.process_iter():
            try:
                for conn in proc.connections(kind="inet"):
                    if conn.status == "LISTEN":
                        yield {
                            "pid": proc.pid,
                            "address": conn.laddr[1],
                            "port": conn.laddr[1],
                            # protocol
                            # family
                        }
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                pass

    def net_connections(self, quals, columns):
        types = {
            socket.SOCK_DGRAM: "udp",
            socket.SOCK_STREAM: "tcp"
        }
        def status(string):
            return None if string == psutil.CONN_NONE else string
        for proc in psutil.process_iter():
            try:
                for conn in proc.connections(kind="inet"):
                    yield {
                        "pid": proc.pid,
                        "address": conn.laddr[0],
                        "port": conn.laddr[1],
                        "type": types[conn.type],
                        "status": status(conn.status)
                    }
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                pass
