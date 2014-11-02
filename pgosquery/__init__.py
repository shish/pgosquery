from multicorn import ForeignDataWrapper
import psutil
import socket


class PgOSQuery(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(PgOSQuery, self).__init__(options, columns)
        self.table_type = options.get("tabletype", "processes")
        self.columns = columns

    def execute(self, quals, columns):
        if self.table_type == "processes":
            for proc in psutil.process_iter():
                try:
                    pinfo = proc.as_dict(attrs=self.columns.keys())
                except psutil.NoSuchProcess:
                    pass
                else:
                    yield pinfo

        if self.table_type == "listening_ports":
            for proc in psutil.process_iter():
                try:
                    for conn in proc.get_connections(kind="inet"):
                        if conn.status == "LISTEN":
                            yield {
                                "pid": proc.pid,
                                "address": conn.laddr[0],
                                "port": conn.laddr[1],
                            }
                except psutil.NoSuchProcess:
                    pass
                except psutil.AccessDenied:
                    pass

        if self.table_type == "net_connections":
            types = {
                socket.SOCK_DGRAM: "udp",
                socket.SOCK_STREAM: "tcp"
            }
            def status(string):
                return None if string == psutil.CONN_NONE else string
            for proc in psutil.process_iter():
                try:
                    for conn in proc.get_connections(kind="inet"):
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
