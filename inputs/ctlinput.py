import MySQLdb
import MySQLdb.cursors
import config

class CTLInput(object):
    db = None
    result = []

    def __init__(self):
        db = MySQLdb.connect(host=config.db_host,
                             user=config.db_user,
                             passwd=config.db_pass,
                             db=config.db_name,
                             cursorclass=MySQLdb.cursors.SSCursor)
        self.db = db
