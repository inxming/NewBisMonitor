"""
Datebase Helper --- MySQL
"""

__author__ = 'CloudSky'
__version__= '0.5'

import MySQLdb

'''
rootdir = sys.path[0]
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename=os.path.join(rootdir,'dbhelper.log'),
    filemode='w',
    )	
'''

class DBHelper:
    def __init__(self):
        self.host = 'localhost'
        self.port = 9527
        self.user = 'root'
        self.passwd = ''
        self.db = ''
    def c2db(self):
        self.conn = MySQLdb.Connect(
            host = self.host,
            port = self.port,
            user = self.user,
            passwd = self.passwd,
            db = self.db,
            )
        self.cur = self.conn.cursor()
    def q2db(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()
    def initdb(self,hosts):
        self.c2db()
        self.cur.execute('Create Database If Not Exists OnlineMonitor')
        self.cur.execute('Create Table If Not Exists OnlineMonitor.total (`time` datetime key,`val` int unsigned )')
        for host in hosts:
            self.cur.execute('Create Table If Not Exists OnlineMonitor.' + host +' (`time` datetime Primary key,`val` int unsigned )')
        self.q2db()
    def insertval(self,host,val):
        self.c2db()
        self.cur.executemany(('insert into OnlineMonitor.' + host + ' (time,val) values(%s,%s)'),val)
        self.cur.executemany('insert into OnlineMonitor.total (time,val) values(%s,%s) ON DUPLICATE KEY UPDATE val=val+values(val)', val)
        self.q2db()
    def smartselect(self, tmp_time, host='total'):
        self.c2db()
        if tmp_time == 0:
            sql = 'select UNIX_TIMESTAMP(time),val from OnlineMonitor.%s order by time' % (host)
        else:
            sql = "select UNIX_TIMESTAMP(time),val from OnlineMonitor.%s where UNIX_TIMESTAMP(time)>%s" % (host,tmp_time/1000)
        self.cur.execute(sql)
        self.arr = []
        for i in self.cur.fetchall():
            self.arr.append([i[0]*1000,i[1]])
        return self.arr
        self.q2db()

        
if __name__ == '__main__':
    db = DBHelper()
    hosts = ['Dragon','Honor']
    hDragon = [('2016-08-23 00:05:00',150), ('2016-08-23 00:10:00',157), ('2016-08-23 00:15:00',183)]
    hHonor =[('2016-08-23 00:10:00',33), ('2016-08-23 00:15:00',66), ('2016-08-23 00:20:00',99)]
    db.initdb(hosts)
    db.insertval('Dragon',hDragon)
    db.insertval('Honor',hHonor)
