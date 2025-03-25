import dearpygui.dearpygui as dpg
import sys
from concurrent.futures import ThreadPoolExecutor
from scripts.gui import setup_gui
from scripts.config import Config

def main(): 
    dpg.create_context()

    with ThreadPoolExecutor(max_workers=10) as executor:

        # set config
        config = Config()

        # audio thing
        #audio = AudioManager(config, executor)

        # start keyboard/mouse listenre
        #listener = InputListener(config, audio, executor)
        #listener.start()

        # make gui
        setup_gui(config, 'aa')
        dpg.create_viewport(
            title=f'{config.title} v{config.version}',
            min_width=240,
            min_height=130,
            width=240,
            height=130,
            resizable=True,
            small_icon=config.small_ico,
            large_icon=config.large_ico,
        )
        dpg.set_viewport_always_top(config.always_on_top)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(config.title, True)

        if sys.platform == 'win32':
            import pywinstyles
            pywinstyles.change_header_color(None, '#2a2a2d')
            pywinstyles.change_border_color(None, "#2a2a2d")

        dpg.start_dearpygui()

    dpg.destroy_context()
    #listener.stop()
    sys.exit(0)

if __name__ == '__main__':
    main()
