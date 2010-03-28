# -*- coding:utf-8 -*-

"""Definition of preferences."""


#------------------------------------------------------------------------------

DEFAULT_PREFS = [
    # Key, function, {allowed_values}, default_value, widget_name]
    # Key, {functions}, None, default_value, widget_name]
    ["window_max", {True:'maximize', False:'unmaximize'}, None, False, "window"],
    ["toolbar_arrow", 'set_show_arrow', 'bool', True, "toolbar*"],
    ["toolbar_iconsize", 'set_icon_size', {"menu":1,"small-tool":2,"large-tool":3,"button":4,"dnd":5,"dialog":6}, 2, "toolbar*"],
    ["toolbar_tooltips", 'set_tooltips', 'bool', True, "toolbar*"],
    ["toolbar_style", 'set_style', {"icon":0,"text":1,"text under icon":2,"text alongside icon":3}, 0, "toolbar*"],
    ["editview_showlinemarks", 'set_show_line_marks', 'bool', True, "editview"],
    ["editview_showlinenumbers", 'set_show_line_numbers', 'bool', True, "editview"],
    ["editview_cursorvisible", 'set_cursor_visible', 'bool', True, "editview"],
    ["editview_highlightcurrentline", 'set_highlight_current_line', 'bool', True, "editview"],
    ["editview_wrapmode", 'set_wrap_mode', {"none":0,"char":1,"word":2,"word+char":3}, 2, "editview"],
    ["editview_font", 'set_font', 'font', "Monospace 10", "editview"],
    ["editview_maxundo", 'set_max_undo_levels', 'int,-1,9999', -1, "editview"],
    ["editview_tabwidth", 'set_tab_width', 'int,1,32', 4, "editview"],
    ["editview_showrightmargin", 'set_show_right_margin', 'bool', False, "editview"],
    ["editview_rightmarginpos", 'set_right_margin_position', 'int,1,999', 72, "editview"],
    ["editview_highlightmatchingbrackets", 'set_highlight_matching_brackets', 'bool', False, "editview"],
    ["editview_spacesinsteadoftabs", 'set_insert_spaces_instead_of_tabs', 'bool', False, "editview"],
    ["editview_indentwidth", 'set_indent_width', 'int,-1,32', -1, "editview"],
    ["editview_indentontab", 'set_indent_on_tab', 'bool', False, "editview"],
    ["editview_autoindent", 'set_auto_indent', 'bool', True, "editview"],
    ["editview_smarthomeend", 'set_smart_home_end', {"disabled":0,"before":1,"after":2,"always":3}, 3, "editview"],
    ["nbook_bottom_show", {True:'show', False:'hide'}, None, True, "hbox_bottom"],
    ["files_trash", None, 'bool', True, None],
    ["files_backup", None, 'bool', False, None],
    ["search_loop", None, 'bool', False, None],
    ["system_homedir", None, None, '', None],
    ["system_datadir", None, None, '', None],
]


#------------------------------------------------------------------------------


