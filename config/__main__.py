from cleo import Application

from config.__version__ import __version__
from config.cli import (CloudFoundryCommand, ConfigClientCommand,
                        DecryptCommand, EncryptCommand)

application = Application("config-client", f"{__version__}")
application.add(CloudFoundryCommand())
application.add(ConfigClientCommand())
application.add(EncryptCommand())
application.add(DecryptCommand())


if __name__ == "__main__":
    application.run()
