from multicorn import ForeignDataWrapper
import psutil
import q


class PgOSQuery(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(PgOSQuery, self).__init__(options, columns)
        self.columns = columns
        q(options)
        q(columns)

    def execute(self, quals, columns):
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            except psutil.NoSuchProcess:
                pass
            else:
                yield pinfo
