# -*- coding:utf-8 -*-

DEFAULT_PREFS = [
    # Key, function, {allowed_values}, default_value, type]
    ["toolbar_arrow", 'set_show_arrow', 'bool', True, "toolbar*"],
    ["toolbar_iconsize", 'set_icon_size', {"menu":1,"small-tool":2,"large-tool":3,"button":4,"dnd":5,"dialog":6}, 1, "toolbar*"],
    ["toolbar_tooltips", 'set_tooltips', 'bool', True, "toolbar*"],
    ["toolbar_style", 'set_style', {"icon":0,"text":1,"text under icon":2,"text alongside icon":3}, 0, "toolbar*"],
    ["editview_showlinemarks", 'set_show_line_marks', 'bool', True, "editview"],
    ["editview_showlinenumbers", 'set_show_line_numbers', 'bool', True, "editview"],
    ["editview_cursorvisible", 'set_cursor_visible', 'bool', True, "editview"],
    ["editview_hlcurrentline", 'set_highlight_current_line', 'bool', True, "editview"],
    ["editview_wrapmode", 'set_wrap_mode', {"none":0,"char":1,"word":2,"word+char":3}, 2, "editview"],
]


#------------------------------------------------------------------------------


