from multicorn import ForeignDataWrapper
import psutil


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
            conns = []
            for proc in psutil.process_iter():
                try:
                    for conn in proc.get_connections(kind="inet"):
                        conns.append((proc.pid, conn))
                except psutil._error.AccessDenied:
                    pass

            for pid, conn in conns:
                if conn.status == "LISTEN":
                    yield {
                        "pid": pid,
                        "address": conn.laddr[0],
                        "port": conn.laddr[1],
                    }
