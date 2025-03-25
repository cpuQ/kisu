import dearpygui.dearpygui as dpg

def setup_gui(config, audio):

    title = config.title

    def always_on_top_callback():
        dpg.set_viewport_always_top(dpg.get_value('always_on_top'))

    main_bg_primary = (42, 42, 45)
    main_bg_secondary = (48, 48, 52)
    main_hover_col = (238, 109, 167)
    main_active_col = (223, 101, 154)
    main_thing_col = (228, 98, 156)
    main_font_col = (192, 195, 199)

    with dpg.theme(tag='_window_theme'):

        with dpg.font_registry():
            default_font = dpg.add_font(config.font_file, 15)

        with dpg.theme_component(dpg.mvAll):

            # main window
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, main_bg_primary)
            dpg.add_theme_color(dpg.mvThemeCol_Border, main_bg_primary)
            dpg.add_theme_color(dpg.mvThemeCol_Text, main_font_col)

            # components
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding,)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8,8)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, main_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, main_hover_col)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, main_active_col)

            # buttons
            #dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, 0.5)
            dpg.add_theme_color(dpg.mvThemeCol_Button, main_bg_secondary)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, main_hover_col)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, main_active_col)

            # slider stuff
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 4)
            dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 4)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, main_thing_col)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, main_bg_secondary)

            # checkbox
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, main_thing_col)

    with dpg.window(tag=title):
        dpg.bind_item_theme(title, '_window_theme')
        dpg.bind_font(default_font)
        with dpg.group(horizontal=True):
            with dpg.group():
                with dpg.group(horizontal=True):
                    dpg.add_button(label=config.button1, width=50, height=20)
                    with dpg.tooltip(dpg.last_item()):
                        dpg.add_text('change button 1', wrap=200)
                    dpg.add_button(label=config.button2, width=50, height=20)
                    with dpg.tooltip(dpg.last_item()):
                        dpg.add_text('change button 2', wrap=200)
                dpg.add_spacer(height=0.9)
                with dpg.group():
                    dpg.add_slider_int(
                        tag='volume',
                        default_value=config.volume,
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
                        default_value=config.delay,
                        min_value=-20,
                        max_value=20,
                        tracked=True,
                        width=108,
                        height=13,
                        track_offset=1.0
                    )
                    with dpg.tooltip(dpg.last_item()):
                        dpg.add_text('delay (ms)', wrap=200)

                with dpg.group(horizontal=True, horizontal_spacing=5):
                    dpg.add_checkbox(tag='always_on_top', default_value=True, callback=always_on_top_callback)
                    with dpg.tooltip(dpg.last_item()):
                        dpg.add_text('keep this window on top')
                    dpg.add_text('made by cpuQ')
                    dpg.add_text('<3', color=main_hover_col)

            with dpg.group():
                dpg.add_button(label='<- reload', tag='a', width=92, height=20)
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('rescan sounds in folder', wrap=200)
                dpg.add_spacer(height=0.9)
                dpg.add_button(label='start', tag='run_button', width=92, height=47)
