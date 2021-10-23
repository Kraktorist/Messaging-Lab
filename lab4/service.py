from nameko.containers import ServiceContainer
from nameko.rpc import rpc

class GreetingService:
    name = "greeting_service"

    @rpc
    def hello(self, name):
        print(u"Hello, {}!".format(name))
        return u"Hello, {}!".format(name)


config = {
  "AMQP_URI": "pyamqp://guest:guest@localhost",
  "WEB_SERVER_ADDRESS": "0.0.0.0:8000",
  "rpc_exchange": "nameko-rpc",
  "max_workers": 10,
  "parent_calls_tracked": 10,
  "LOGGING": {
    "version": 1,
    "handlers": {
      "console": {
        "class": "logging.StreamHandler"
      }
    },
    "root": {
      "level": "DEBUG",
      "handlers": [
        "console"
      ]
    }
  }
}
# create a container
container = ServiceContainer(GreetingService, config=config)

# ``container.extensions`` exposes all extensions used by the service
service_extensions = list(container.extensions)

# start service
container.start()
