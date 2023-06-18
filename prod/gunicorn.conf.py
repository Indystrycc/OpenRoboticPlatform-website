import multiprocessing

accesslog = "-"
bind = "unix:/run/gunicorn/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "main:create_app()"
