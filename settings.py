from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
import logging
from pathlib import Path


configs = [
    "./settings.conf",
    "/etc/don_quixote/settings.conf"

]
settings = {}
localization = {}

def read_settings():

    for config in configs:
        config_path = Path(config)
        if config_path.is_file():
            exec(open(config).read(), settings)
    #checking if  needed tokens exist
    if not "telegram_token" in settings:
        exit(1)
    elif not "sancho_disguise" in settings:
        exit(1)
    else:
        #print(settings['sancho_disguise'], settings['telegram_token'])
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        localization_path = Path(settings['localization']+".py")
        if localization_path.is_file():
            exec(open(settings['localization']+".py").read(), localization)


read_settings()
print("Settings loaded successfully!")