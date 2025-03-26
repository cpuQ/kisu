from pynput import keyboard

class KeyboardListener:
    def __init__(self, config, executor, audio):
        self.config = config
        self.executor = executor
        self.audio = audio
        self.running = False
        self.active_keys = set()
        self.hotkey_input = None
        self._set_input_keys()

    def _set_input_keys(self):
        """assign input keys from config to be listened"""
        self.listen_inputs = {
            self._fix_key(self.config.button1): 'button1',
            self._fix_key(self.config.button2): 'button2'
        }

    def _fix_key(self, key):
        """convert the key string to pynput object"""
        try:
            return keyboard.KeyCode.from_char(key)
        except ValueError:
            if hasattr(keyboard.Key, key):
                return getattr(keyboard.Key, key)
        return None

    def _get_key_button(self, key):
        """return assigned button name for a key"""
        return self.listen_inputs.get(key, None)

    def on_press(self, key):
        """submit playsound on key press"""
        if (key in self.active_keys) or (key not in self.listen_inputs):
            return
        button = self._get_key_button(key)
        self.active_keys.add(key)
        self.executor.submit(self.audio.play_sound, button, 'press')
        self.gui.set_button_active(button)

    def on_release(self, key):
        """submit playsound on key release"""
        button = self._get_key_button(key)
        if key in self.active_keys:
            self.active_keys.discard(key)
            self.executor.submit(self.audio.play_sound, button, 'release')
            self.gui.set_button_inactive(button)

    def hotkey(self):
        """for selecting hotkeys"""
        def on_press(key):
            self.hotkey_input = key
            return False
        with keyboard.Listener(on_press=on_press) as k_listener:
            k_listener.join()

        # esc to cancel
        if self.hotkey_input == keyboard.Key.esc:
            return False
        return self.hotkey_input

    def start(self):
        """start the keyboard listener"""
        # new listener everytime because it cannot be reused
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.keyboard_listener.start()
        self.running = True

    def stop(self):
        """stop the keyboard listener"""
        self.keyboard_listener.stop()
        self.running = False

    def set_gui(self, gui):
        """set gui reference to make the buttons reactive"""
        self.gui = gui
