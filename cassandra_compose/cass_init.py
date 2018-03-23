# Run this to initialize the Cassandra Container

import logging

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "mykeyspace"




def createKeySpace():
    try:
        cluster = Cluster(contact_points=['0.0.0.0'], port=9042)
        session = cluster.connect()
        log.info("Creating keyspace...")
        session.execute("""
            CREATE KEYSPACE %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
            """ % KEYSPACE)


        log.info("setting keyspace...")

        session.set_keyspace(KEYSPACE)



        log.info("creating table...")
        session.execute("""
            CREATE TABLE ImgCls (
                file_name text,
                posted_time timestamp,
                identified_digit int,
                PRIMARY KEY (posted_time)
            )"""
            )
    except Exception as e:
        log.error("Unable to create keyspace")
        log.error(e)


if __name__ == "__main__":
    createKeySpace()
