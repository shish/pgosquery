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
