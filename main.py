import dearpygui.dearpygui as dpg
import sys
from concurrent.futures import ThreadPoolExecutor
from scripts.gui import KisuGUI
from scripts.config import Config
from scripts.audio import AudioManager
from scripts.listen import KeyboardListener

def main():

    # make context first
    dpg.create_context()

    # set config
    config = Config()

    with ThreadPoolExecutor(max_workers=5) as executor:

        # audio thing
        audio = AudioManager(config, executor)

        # start keyboard listenre
        listener = KeyboardListener(config, executor, audio)

        # make gui object
        gui = KisuGUI(config, audio, listener)

        # add gui to listener to make the gui buttons reactive
        listener.set_gui(gui)

        # setup and create gui
        gui.setup_gui()
        dpg.create_viewport(
            title=f'{config.title} v{config.version}',
            min_width=242,
            min_height=136,
            width=242,
            height=136,
            resizable=True,
            small_icon=config.small_ico,
            large_icon=config.large_ico,
        )
        dpg.set_viewport_always_top(config.always_on_top)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(config.title, True)

        # import and style the window if its windows lol
        if config.platform.startswith('win'):
            import pywinstyles
            pywinstyles.change_header_color(None, '#2a2a2d')
            pywinstyles.change_border_color(None, "#2a2a2d")
            pywinstyles.change_title_color(None, '#c0c3c7')

        try:
            dpg.start_dearpygui()
        finally:
            if listener.running:
                listener.stop()
            if audio.initialized:
                audio.cleanup()
            config.save()

    # gui cleanup, and exit
    dpg.destroy_context()
    sys.exit(0)

if __name__ == '__main__':
    main()
