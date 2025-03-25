import dearpygui.dearpygui as dpg
import sys
from concurrent.futures import ThreadPoolExecutor
from scripts.gui import KisuGUI
from scripts.config import Config
#from scripts.audio import AudioManager
from scripts.listen import InputListener

def main(): 
    dpg.create_context()

    with ThreadPoolExecutor(max_workers=10) as executor:

        # set config
        config = Config()

        # audio thing
        #audio = AudioManager(config, executor)
        audio = 'a'

        # start keyboard/mouse listenre
        listener = InputListener(config, executor)

        # make gui
        gui = KisuGUI(config, audio, listener)
        gui.setup_gui()
        dpg.create_viewport(
            title=f'{config.title} v{config.version}',
            min_width=240,
            min_height=136,
            width=240,
            height=136,
            resizable=True,
            small_icon=config.small_ico,
            large_icon=config.large_ico,
        )
        dpg.set_viewport_always_top(config.always_on_top)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(config.title, True)

        if config.platform.startswith('win'):
            import pywinstyles
            pywinstyles.change_header_color(None, '#2a2a2d')
            pywinstyles.change_border_color(None, "#2a2a2d")
            pywinstyles.change_title_color(None, '#c0c3c7')

        dpg.start_dearpygui()

    dpg.destroy_context()
    sys.exit(0)

if __name__ == '__main__':
    main()
