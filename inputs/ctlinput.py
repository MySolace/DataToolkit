import MySQLdb
import config

class CTLInput(object):
    cursor = None
    result = []

    def __init__(self):
        db = MySQLdb.connect(host=config.db_host,
                             user=config.db_user,
                             passwd=config.db_pass,
                             db=config.db_name)
        self.cursor = db.cursor()