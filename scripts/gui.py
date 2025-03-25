import dearpygui.dearpygui as dpg
import os
import subprocess

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

    def setup_font(self):
        with dpg.font_registry():
            self.font = dpg.add_font(self.config.font_file, 15)

    def setup_theme(self):

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

                # buttons
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

    def setup_gui(self):

        # setup theme
        self.setup_font()
        self.setup_theme()

        with dpg.window(tag=self.config.title):
            dpg.bind_item_theme(dpg.last_item(), '_window_theme')
            dpg.bind_font(self.font)
            with dpg.group(horizontal=True):
                with dpg.group():
                    with dpg.group(horizontal=True):
                        dpg.add_button(label=self.config.button1, width=50, height=20, tag='button1', callback=self.hotkey_button, user_data='button1')
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('change button1', tag='button1_tooltip', wrap=200)
                        dpg.add_button(label=self.config.button2, width=50, height=20, tag='button2', callback=self.hotkey_button, user_data='button2')
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
                        )
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('volume', wrap=200)
                        dpg.add_slider_int(
                            tag='delay',
                            default_value=self.config.delay,
                            min_value=-20,
                            max_value=20,
                            tracked=True,
                            width=108,
                            height=13,
                        )
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('delay (ms)', wrap=200)

                    with dpg.group(horizontal=True, horizontal_spacing=5):
                        dpg.add_checkbox(tag='always_on_top', default_value=True, callback=self.always_on_top)
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('keep this window on top')
                        dpg.add_text('made by cpuQ', color=self.main_font_col_disabled)
                        dpg.add_text('<3', color=self.main_hover_col)

                with dpg.group():
                    with dpg.group(horizontal=True, horizontal_spacing=8):
                        dpg.add_button(label='/> reload', tag='reload_sounds', width=64, height=20)
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('rescan for changes in sounds', wrap=200)
                        dpg.add_button(label='...', tag='open_directory', width=20, height=20, callback=self.open_directory)
                        with dpg.tooltip(dpg.last_item()):
                            dpg.add_text('open sounds directory', wrap=200)

                    dpg.add_spacer(height=0.9)
                    dpg.add_button(label='start', tag='start_button', width=92, height=53, callback=self.start_button)

    # callbacks
    def always_on_top(self):
        dpg.set_viewport_always_top(dpg.get_value('always_on_top'))

    def open_directory(self):
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
        if self.state == 0:
            self.listener.start()
            dpg.configure_item('start_button', label='stop')
            self.state = 1
        elif self.state == 1:
            self.listener.stop()
            dpg.configure_item('start_button', label='start')
            self.state = 0

    def hotkey_button(self, button):
        self._toggle_all('disable')
        dpg.configure_item(button, label='...')
        dpg.set_value(f'{button}_tooltip', 'waiting for key, esc to cancel')

        hotkey = self.listener.hotkey()
        if hotkey:
            cleaned = str(hotkey).replace("'", "")
            setattr(self.config, button, cleaned)

        dpg.configure_item(button, label=f'{getattr(self.config, button)}')
        dpg.set_value(f'{button}_tooltip', f'change {button}')
        self._toggle_all('enable')

    def _toggle_all(self, toggle):

        # disable all ui stuff
        if toggle == 'disable':
            dpg.configure_item('button1', enabled=False)
            dpg.configure_item('button2', enabled=False)
            dpg.configure_item('volume', enabled=False)
            dpg.configure_item('delay', enabled=False)
            dpg.configure_item('reload_sounds', enabled=False)
            dpg.configure_item('always_on_top', enabled=False)
            dpg.configure_item('open_directory', enabled=False)
            dpg.configure_item('start_button', enabled=False)
        
        # enable all ui stuff
        if toggle == 'enable':
            dpg.configure_item('button1', enabled=True)
            dpg.configure_item('button2', enabled=True)
            dpg.configure_item('volume', enabled=True)
            dpg.configure_item('delay', enabled=True)
            dpg.configure_item('reload_sounds', enabled=True)
            dpg.configure_item('always_on_top', enabled=True)
            dpg.configure_item('open_directory', enabled=True)
            dpg.configure_item('start_button', enabled=True)