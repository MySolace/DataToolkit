from ctlinput import CTLInput
from sys import stdout

class Messages(CTLInput):
    subsets = 100-1

    def __init__(self):
        super(Messages, self).__init__()
        print "Retrieving rows..."

        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM message")
        rows = cursor.fetchone()[0]
        cursor.close()

        for i in range(0, self.subsets):
            self.getSubgroup(i, rows)
        stdout.write("\n")

    def __iter__(self):
        return iter(self.result)

    def __len__(self):
        return len(self.result)

    def getSubgroup(self, i, totalrows):
        stdout.write("\r%d%%" % i)
        stdout.flush()
        perpage = totalrows/(self.subsets+1)
        start = i*perpage

        # Use a deferred join.
        # See #2: http://www.iheavy.com/2013/06/19/3-ways-to-optimize-for-paging-in-mysql/
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT m.*, a.address
            FROM message m
            INNER JOIN (SELECT id
                FROM message
                LIMIT %d OFFSET %d)
            AS message_join USING (id)
            JOIN actor a on m.actor_id=a.id;
        """ % (perpage, start))
        columns = cursor.description
        self.result = self.result + [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor]
        cursor.close()
