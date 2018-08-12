from __init__ import app as application

if __name__ == "__main__":
    ap.run()


uwsgi --chdir /home/sarah/api --wsgi-file /home/sarah/api/wsgi.py --socket /home/sarah/api/api.sock
