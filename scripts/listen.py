from pynput import keyboard #, mouse

class InputListener:
    def __init__(self, config, executor):
        self.executor = executor
        #self.audio_manager = audio_manager
        self.config = config
        self.active_inputs = set()
        self.listen_inputs = [
            self._fix_btn(self.config.button1),
            self._fix_btn(self.config.button2)
        ]

    # fix the button string to pynput object
    def _fix_btn(self, button):
        try:
            return keyboard.KeyCode.from_char(button)
        except ValueError:
            if hasattr(keyboard.Key, button):
                return getattr(keyboard.Key, button)
            # elif button.lower() in {'mouse1', 'mouse_left'}:
            #     return mouse.Button.left
            # elif button.lower() in {'mouse2', 'mouse_right'}:
            #     return mouse.Button.right
            # elif button.lower() in {'mouse3', 'mouse_middle'}:
            #     return mouse.Button.middle
            # elif button.lower() in {'mouse4', 'mouse_x1'}:
            #     return mouse.Button.x1
            # elif button.lower() in {'mouse5', 'mouse_x2'}:
            #     return mouse.Button.x2
        return None

    def check(self, state):
        if any(button in self.active_inputs for button in self.listen_inputs):
            #self.executor.submit(self.audio_manager.play_sound, state)
            print(f'{state} sound played')

    def on_press(self, key):
        if key in self.active_inputs:
            return
        self.active_inputs.add(key)
        self.executor.submit(self.check('press'))

    def on_release(self, key):
        self.active_inputs.discard(key)
        self.executor.submit(self.check('release'))

    # def on_click(self, x, y, button, pressed):
    #     if pressed:
    #         state = 'press'
    #         self.pressed_inputs.add(button)
    #     else:
    #         state = 'release'
    #         self.pressed_inputs.discard(button)
    #     self.check(state)

    def hotkey(self):
        self.detected_input = None
        def on_press(key):
            self.detected_input = key
            return False
        # def on_click(x, y, button, pressed):
        #     if pressed:
        #         self.detected_input = button
        #         return False
        with keyboard.Listener(on_press=on_press) as k_listener: #, mouse.Listener(on_click=on_click) as m_listener:
            k_listener.join()
            #m_listener.join()

        if self.detected_input == keyboard.Key.esc:
            return False

        self.listen_inputs = [
            self._fix_btn(self.config.button1),
            self._fix_btn(self.config.button2)
        ]
        return self.detected_input

    def start(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        #self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener.start()
        #self.mouse_listener.start()

    def stop(self):
        self.keyboard_listener.stop()
        #self.mouse_listener.stop()
