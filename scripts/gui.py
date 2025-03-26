import dearpygui.dearpygui as dpg
import os
import subprocess
import time

# fuck the ugly nesting idc the gui looks clean af
class KisuGUI:
    def __init__(self, config, audio, listener):
        self.config = config
        self.audio = audio
        self.listener = listener
        self.state = 0
        
        # theme stuff
        self.font = None
        self.main_bg_primary = (42, 42, 45)
        self.main_bg_secondary = (48, 48, 52)
        self.main_hover_col = (238, 109, 167)
        self.main_active_col = (223, 101, 154)
        self.main_thing_col = (228, 98, 156)
        self.main_font_col = (192, 195, 199)
        self.main_font_col_disabled = (155, 161, 168)

        # audio devices
        self.available_devices = []
        self.current_device = None

    def set_button_active(self, button_name):
        """change button color to active state when key is pressed"""

        if button_name and dpg.does_item_exist(button_name):
            # create temporary theme for the active button
            with dpg.theme() as active_theme:
                with dpg.theme_component(dpg.mvButton):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, self.main_active_col)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.main_active_col)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.main_active_col)

            # apply the theme to the button
            dpg.bind_item_theme(button_name, active_theme)

    def set_button_inactive(self, button_name):
        """reset button color to normal state when key is released"""

        if button_name and dpg.does_item_exist(button_name):
            # reset to default theme
            dpg.bind_item_theme(button_name, '_button_theme')

    def setup_font(self):
        """set dpg font registry for cusomt font"""
        with dpg.font_registry():
            self.font = dpg.add_font(self.config.font_file, 15)

    def setup_theme(self):
        """gui theme thing..."""

        with dpg.theme(tag='_window_theme'):

            with dpg.theme_component(dpg.mvAll):

                # main window
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, self.main_bg_primary)
                dpg.add_theme_color(dpg.mvThemeCol_Border, self.main_bg_primary)
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.main_font_col)
                dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, self.main_font_col_disabled)

                # components
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0,0)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8,8)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, self.main_bg_secondary)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, self.main_hover_col)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, self.main_active_col)

                # default buttons
                #dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, 0.5)
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.main_bg_secondary)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.main_hover_col)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.main_active_col)

                # slider stuff
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 4)
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, self.main_thing_col)
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, self.main_bg_secondary)

                # checkbox
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, self.main_thing_col)

        with dpg.theme(tag='_button_theme'):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.main_bg_secondary)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.main_hover_col)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.main_active_col)

    def setup_gui(self):
        """setup the main gui including themes and fonts"""

        # setup theme
        self.setup_font()
        self.setup_theme()

        # set audio thing
        self.refresh_audio_devices()

        with dpg.window(tag=self.config.title, no_scrollbar=True):
            dpg.bind_item_theme(dpg.last_item(), '_window_theme')
            dpg.bind_font(self.font)
            with dpg.group(horizontal=True):
                with dpg.group():
                    with dpg.group(horizontal=True):
                        dpg.add_button(label=self.config.button1, width=50, height=20, tag='button1', 
                                      callback=lambda s, a, u: self.hotkey_button(u), user_data='button1')
                        dpg.bind_item_theme('button1', '_button_theme')
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('change button1', tag='button1_tooltip', wrap=200)
                        dpg.add_button(label=self.config.button2, width=50, height=20, tag='button2', 
                                      callback=lambda s, a, u: self.hotkey_button(u), user_data='button2')
                        dpg.bind_item_theme('button2', '_button_theme')
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('change button2', tag='button2_tooltip', wrap=200)
                    dpg.add_spacer(height=0.9)
                    with dpg.group():
                        dpg.add_slider_int(
                            tag='volume',
                            default_value=self.config.volume,
                            min_value=0,
                            max_value=100,
                            tracked=True, 
                            width=108,
                            height=13,
                            clamped=True,
                            callback=lambda _, v: self.audio.set_volume(v)
                        )
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('volume', wrap=200)
                        dpg.add_slider_int(
                            tag='delay',
                            default_value=self.config.delay,
                            min_value=0,
                            max_value=50,
                            tracked=True,
                            width=108,
                            height=13,
                            callback=lambda _, d: self.audio.set_delay(d)
                        )
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('delay (ms)', wrap=200)

                    with dpg.group(horizontal=True, horizontal_spacing=5):
                        dpg.add_checkbox(tag='always_on_top', default_value=True, 
                                        callback=lambda s, a: self.always_on_top())
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('keep this window on top')
                        dpg.add_text('made by cpuQ', color=self.main_font_col_disabled)
                        dpg.add_text('<3', color=self.main_hover_col)

                with dpg.group():
                    with dpg.group(horizontal=True, horizontal_spacing=8):
                        dpg.add_button(label=self.config.device, width=26, height=20, tag='output_device_button', 
                                      callback=lambda s, a: self.output_device_button())
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text(self.available_devices[self.config.device], wrap=220, tag='output_device_button_tooltip')
                        dpg.add_button(label='/>', tag='reload_button', width=26, height=20, 
                                      callback=lambda s, a: self.reload_button())
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('rescan audio devices and sounds', wrap=200)
                        dpg.add_button(label='...', tag='open_directory_button', width=26, height=20, 
                                      callback=lambda s, a: self.open_directory_button())
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('open sounds directory', wrap=200)

                    dpg.add_spacer(height=0.9)
                    dpg.add_button(label='start', tag='start_button', width=94, height=53, 
                                  callback=lambda s, a: self.start_button())

    # callbacks
    def always_on_top(self):
        """makes the window always stay on top"""
        dpg.set_viewport_always_top(dpg.get_value('always_on_top'))

    def refresh_audio_devices(self):
        """store the list of audio devices"""
        self.available_devices = self.audio.get_devices()
        return self.available_devices

    def output_device_button(self):
        """cycle through available audio devices"""
        self._enable_all(False)
        self.listener.stop()
        if not self.available_devices:
            self.refresh_audio_devices()
            if not self.available_devices:
                dpg.configure_item('output_device_button', label=':c')
                dpg.configure_item('output_device_button_tooltip', default_value='no devices found')
                return

        # cycle to the next device
        self.config.device = (self.config.device + 1) % len(self.available_devices)
        selected_device = self.available_devices[self.config.device]

        # update the button label and tooltip
        dpg.configure_item('output_device_button', label=self.config.device)
        dpg.configure_item('output_device_button_tooltip', default_value=selected_device)

        # reinitialize audio
        self.audio.init_audio()
        self.listener.start()
        self._enable_all(True)

    def reload_button(self):
        """reload audio devices and sounds"""
        self._enable_all(False)
        self.listener.stop()
        self.refresh_audio_devices()
        self.audio.init_audio()
        self.audio.load_sounds()
        self.listener.start()
        self._enable_all(True)

    def open_directory_button(self):
        """open directory based on current platform"""
        path = self.config.sounds_dir
        if self.config.platform.startswith('win'):
            os.startfile(path)
        elif self.config.platform.startswith('darwin'):
            subprocess.run(['open', path])
        elif self.config.platform.startswith('linux'):
            subprocess.run(['xdg-open', path])
        else:
            raise OSError('unsupported operating system')

    def start_button(self):
        """start main keyboard listener"""
        if self.state == 0:
            self.listener.start()
            dpg.configure_item('start_button', label='stop')
            self.state = 1
        elif self.state == 1:
            self.listener.stop()
            dpg.configure_item('start_button', label='start')
            self.state = 0

    def hotkey_button(self, button):
        """set hotkeys for selected button"""
        self._enable_all(False)
        dpg.configure_item(button, label='...')
        dpg.set_value(f'{button}_tooltip', 'waiting for key, esc to cancel')

        if hotkey := self.listener.hotkey():
            cleaned = str(hotkey).replace("'", "")
            setattr(self.config, button, cleaned)
            self.listener._set_input_keys()

        dpg.configure_item(button, label=f'{getattr(self.config, button)}')
        dpg.set_value(f'{button}_tooltip', f'change {button}')
        self._enable_all(True)

    def _enable_all(self, enabled):
        """enable / disable all gui components during hotkey"""
        dpg.configure_item('button1', enabled=enabled)
        dpg.configure_item('button2', enabled=enabled)
        dpg.configure_item('volume', enabled=enabled)
        dpg.configure_item('delay', enabled=enabled)
        dpg.configure_item('always_on_top', enabled=enabled)
        dpg.configure_item('reload_button', enabled=enabled)
        dpg.configure_item('output_device_button', enabled=enabled)
        dpg.configure_item('open_directory_button', enabled=enabled)
        dpg.configure_item('start_button', enabled=enabled)
