import os
import sys
import configparser

# platform thing
def get_platform():
    platform = sys.platform
    if platform.startswith(('win', 'darwin', 'linux')):
        return platform
    else:
        raise OSError('unsupported operating system')

# handles paths properly when compiled or running from source
def script_dir():
    if getattr(sys, 'frozen', False):
        # for running as executable
        return os.path.dirname(sys.executable)
    else:
        # for running as script
        return os.path.dirname(os.path.abspath(sys.argv[0]))

# check config file
def config_check(file_path):
    config = configparser.ConfigParser()

    if not os.path.exists(file_path):
        # write default config to file
        config['buttons'] = {
            'button1': 'z',
            'button2': 'x'
        }
        config['sounds'] = {
            'volume': str(1),
            'device': str(1)
        }
        config['other'] = {
            'always_on_top': str(True)
        }
        with open(file_path, 'w') as configfile:
            config.write(configfile)
    else:
        # read existing file
        config.read(file_path)

    return config

class Config:

    def __init__(self):

        # title
        self.title = 'kisu'
        self.version = '0.2'

        # platform specific
        self.platform = get_platform()

        # script directory
        self.script_dir = script_dir()

        # resources things
        self.res_dir = os.path.join(self.script_dir, 'res')
        self.font_file = os.path.join(self.res_dir, 'cq-pixel-min.ttf')
        self.small_ico = os.path.join(self.res_dir, 'kisu_small.ico')
        self.large_ico = os.path.join(self.res_dir, 'kisu_large.ico')
        self.silent_audio = os.path.join(self.res_dir, 'silent.wav')

        # config file
        self.config_file = os.path.join(self.script_dir, 'config.ini')

        # audio folders
        self.sounds_dir = os.path.join(self.script_dir, 'sounds')
        self.button1_dir = os.path.join(self.sounds_dir, 'button1')
        self.button2_dir = os.path.join(self.sounds_dir, 'button2')

        # create folders if they dont exist
        os.makedirs(self.sounds_dir, exist_ok=True)
        os.makedirs(self.button1_dir, exist_ok=True)
        os.makedirs(self.button2_dir, exist_ok=True)

        # read config file
        config = config_check(self.config_file)
        self.button1 = str(config['buttons'].get('button1', 'z'))
        self.button2 = str(config['buttons'].get('button2', 'x'))
        self.volume = int(config['sounds'].get('volume', 80))
        self.delay = int(config['sounds'].get('delay', 0))
        self.device = int(config['sounds'].get('device', None))
        self.always_on_top = bool(config['other'].get('always_on_top', True))

    def save(self):
        """save the configs"""
        config = configparser.ConfigParser()
        config['buttons'] = {
            'button1': self.button1,
            'button2': self.button2
        }

        config['sounds'] = {
            'volume': str(self.volume),
            'delay': str(self.delay),
            'device': str(self.device)
        }

        config['other'] = {
            'always_on_top': str(self.always_on_top)
        }
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)
