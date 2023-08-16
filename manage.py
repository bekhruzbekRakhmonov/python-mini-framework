from httpserver import HTTPServer
import sys

if __name__ == '__main__':
    server = HTTPServer()
    try:
        server.run()
    except KeyboardInterrupt:
        sys.exit(0)