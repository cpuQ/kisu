import pygame.mixer as mixer
import pygame._sdl2.audio as sdl2_audio
import os
import time
import random

class AudioManager:
    def __init__(self, config, executor):
        self.config = config
        self.executor = executor
        self.volume = self.config.volume
        self.initialized = False
        self.init_audio()
        self.load_sounds()

    def get_devices(self, capture_devices: bool = False):
        """get output devices with sdl2"""
        if not self.initialized:
            mixer.init()
            devices = tuple(sdl2_audio.get_audio_device_names(capture_devices))
            mixer.quit()
            return devices
        return tuple(sdl2_audio.get_audio_device_names(capture_devices))

    def init_audio(self):
        """set the output device"""
        devices = self.get_devices()
        if not devices:
            self.initialized = False
            return
        if 0 <= self.config.device < len(devices):
            device = devices[self.config.device]
            if self.initialized:
                mixer.quit()
            mixer.init(devicename=device)
            self.initialized = True

    def _make_sound_obj(self, path, folder):
        """convert the files to pygame sound object"""
        if not self.initialized:
            self.init_audio()
        path = os.path.join(path,folder)
        sounds = []
        if os.path.exists(path):
            files = [f for f in os.listdir(path) if f.endswith(('.wav', '.mp3', '.ogg', 'flac'))]
            sounds.extend(mixer.Sound(os.path.join(path, f)) for f in files)
        else:
            os.makedirs(path)
        return sounds

    def load_sounds(self):
        """load button sounds from directories"""
        self.button1_sounds = {
            'press': self._make_sound_obj(self.config.button1_dir, 'press'),
            'release': self._make_sound_obj(self.config.button1_dir, 'release'),
        }
        self.button2_sounds = {
            'press': self._make_sound_obj(self.config.button2_dir, 'press'),
            'release': self._make_sound_obj(self.config.button2_dir, 'release'),
        }

    def _add_delay(self, sound):
        """delays sound playback without blocking main thread"""
        time.sleep(self.config.delay/1000)
        sound.play()

    def play_sound(self, button, state):
        """play the sound weee"""
        action_map = {
            'button1': self.button1_sounds,
            'button2': self.button2_sounds
        }

        if sounds := action_map[button][state]:

            # play only if sound is found in directory
            if sounds:
                sound = random.choice(sounds)
                sound.set_volume(self.config.volume/100)
                self.executor.submit(self._add_delay, sound)

    def set_volume(self, volume):
        """set the volume of all sounds"""
        self.config.volume = volume

    def set_delay(self, delay):
        """set the delay for sound playback"""
        self.config.delay = delay

    def cleanup(self):
        """quit mixer"""
        mixer.quit()
