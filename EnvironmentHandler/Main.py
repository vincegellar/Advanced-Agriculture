from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from EnvironmentHandler import app as environment_handler
from WebUI import app as web_ui
from BLL import announcer
from announcer import Announcer

announcer_thread = Announcer()

app = DispatcherMiddleware(environment_handler, {
    '/web-ui': web_ui
})

if __name__ == '__main__':
    run_simple('localhost', 8080, app)
