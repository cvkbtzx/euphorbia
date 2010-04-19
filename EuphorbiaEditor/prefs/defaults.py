# -*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Copyright (C) 2008-2010   Bzoloid
##
##  This program is free software; you can redistribute it and/or
##  modify it under the terms of the GNU General Public License
##  as published by the Free Software Foundation; either version 2
##  of the License, or (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program; if not, write to the Free Software Foundation,
##  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.


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
    ["editview_drawspaces", 'set_draw_spaces', {"none":0,"space":1,"tab":2,"tab+space":3,"eol":4,"all":15}, 0, "editview"],
    ["editview_maxundo", 'set_max_undo_levels', 'int,-1,999', -1, "editview"],
    ["editview_tabwidth", 'set_tab_width', 'int,1,32', 4, "editview"],
    ["editview_showrightmargin", 'set_show_right_margin', 'bool', False, "editview"],
    ["editview_rightmarginpos", 'set_right_margin_position', 'int,1,999', 72, "editview"],
    ["editview_highlightmatchingbrackets", 'set_highlight_matching_brackets', 'bool', False, "editview"],
    ["editview_spacesinsteadoftabs", 'set_insert_spaces_instead_of_tabs', 'bool', False, "editview"],
    ["editview_indentwidth", 'set_indent_width', 'int,-1,32', -1, "editview"],
    ["editview_indentontab", 'set_indent_on_tab', 'bool', False, "editview"],
    ["editview_autoindent", 'set_auto_indent', 'bool', True, "editview"],
    ["editview_smarthomeend", 'set_smart_home_end', {"disabled":0,"before":1,"after":2,"always":3}, 3, "editview"],
    ["editview_style", 'set_stylescheme', None, 'classic', "editview"],
    ["sidepanel_expandlevel", 'set_expand_level', 'int,0,7', 3, 'treedocstruct'],
    ["gui_sidepanelshow", 'showpanel', None, True, "sidepanel"],
    ["gui_bottompanelshow", 'showpanel', None, True, "bottompanel"],
    ["files_trash", None, 'bool', True, None],
    ["files_backup", None, 'bool', False, None],
    ["search_loop", None, 'bool', False, None],
    ["print_1header", None, 'bool', False, None],
    ["print_1header_separator", None, 'bool', True, None],
    ["print_1header_text", None, 'text', "|%f|", None],
    ["print_1header_font", None, 'font', "Sans 8", None],
    ["print_2footer", None, 'bool', False, None],
    ["print_2footer_separator", None, 'bool', True, None],
    ["print_2footer_text", None, 'text', "%F||page %N/%Q", None],
    ["print_2footer_font", None, 'font', "Sans 8", None],
    ["print_margin_1top", None, 'int,0,999', 0, None],
    ["print_margin_2left", None, 'int,0,999', 0, None],
    ["print_margin_3right", None, 'int,0,999', 0, None],
    ["print_margin_4bottom", None, 'int,0,999', 0, None],
    ["print_nlinesfont", None, 'font', "Monospace 6", None],
    ["print_nlinesinterval", None, 'int,0,50', 5, None],
    ["system_datadir", None, None, '', None],
    ["system_confdir", None, None, '', None],
    ["system_maindir", None, None, '', None],
]


#------------------------------------------------------------------------------


