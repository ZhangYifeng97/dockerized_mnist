# Run this to initialize the Cassandra Container



from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "mykeyspace"

def createKeySpace():
    cluster = Cluster(contact_points=['0.0.0.0'], port=9042)
    session = cluster.connect()

    session.execute("""
        CREATE KEYSPACE %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE)

    session.set_keyspace(KEYSPACE)

    session.execute("""
        CREATE TABLE ImgCls (
            file_name text,
            posted_time float,
            identified_digit int,
            PRIMARY KEY (posted_time)
        )"""
        )


if __name__ == "__main__":
    createKeySpace()
