import sys
import os
import configparser
from Database import Database
from libraryscanner import LibraryScanner
from yjmpd import YJMPD
from API import API
from HTTPServer import HTTPServerThread

config = configparser.ConfigParser()
try:
    config.read("../config.cfg")
    HTTP_PORT = int(config.get("HTTP", "port"))
    HTTP_DOMAIN = str(config.get("HTTP", "domainname"))
    DAEMON_PORT = int(config.get("Daemon", "port"))
    MUSIC_DIR = str(config.get("Library", "musicdir"))

    DB_USERNAME = config.get("Database", "username")
    DB_PASSWORD = config.get("Database", "password")
    DB_HOST = config.get("Database", "host")
    DB_DATABASE = config.get("Database", "database")
    DB_PORT = config.getint("Database", "port")

except Exception as e:
    print(e.with_traceback())
    sys.exit(1)


class MainDaemon(YJMPD):
    def run(self):
        database = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
        http_thread = HTTPServerThread(HTTP_PORT, API(database, HTTP_DOMAIN + ":" + str(HTTP_PORT), MUSIC_DIR))
        http_thread.start()
        LibraryScanner(db, MUSIC_DIR)


if __name__ == "__main__":
    username = os.getenv('USER')
    if username is None:
        dir = "/tmp/.pydaemon.pid"
    else:
        dir = "/home/" + username + "/.pydaemon.pid"
    daemon = MainDaemon(dir, MUSIC_DIR)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        elif 'debug' == sys.argv[1]:
            db = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
            HTTP_thread = HTTPServerThread(HTTP_PORT, API(db, HTTP_DOMAIN + ":" + str(HTTP_PORT), MUSIC_DIR))
            HTTP_thread.start()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|status|restart" % sys.argv[0])
        sys.exit(2)
