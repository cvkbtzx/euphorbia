#-*- coding:utf-8 -*-

##  EUPHORBIA - GTK LaTeX Editor
##  Module: EuphorbiaEditor.prefs.defaults
##  Copyright (C) 2008-2011   Bzoloid
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


"""Definition of default preferences."""


#------------------------------------------------------------------------------

DEFAULT_PREFS = [
    # [Key, {functions}, {allowed_values}, default_value, widget_name]
    ["window_maximized", {True:'maximize', False:'unmaximize'}, None, False, "window"],
    ["toolbar_arrow", 'set_show_arrow', 'bool', True, "toolbar*"],
    ["toolbar_iconsize", 'set_icon_size', {"l_size-menu":1,"l_size-small-tool":2,"l_size-large-tool":3,"l_size-button":4,"l_size-dnd":5,"l_size-dialog":6}, 2, "toolbar*"],
    ["toolbar_tooltips", 'set_tooltips', 'bool', True, "toolbar*"],
    ["toolbar_style", 'set_style', {"l_b-icon":0,"l_b-text":1,"l_b-text-under-icon":2,"l_b-text-alongside-icon":3}, 0, "toolbar*"],
    ["editview_showlinemarks", 'set_show_line_marks', 'bool', True, "editview"],
    ["editview_showlinenumbers", 'set_show_line_numbers', 'bool', True, "editview"],
    ["editview_cursorvisible", 'set_cursor_visible', 'bool', True, "editview"],
    ["editview_highlightcurrentline", 'set_highlight_current_line', 'bool', True, "editview"],
    ["editview_wrapmode", 'set_wrap_mode', {"l_wrap-none":0,"l_wrap-char":1,"l_wrap-word":2,"l_wrap-word+char":3}, 2, "editview"],
    ["editview_font", 'set_font', 'font', "Monospace 10", "editview"],
    ["editview_drawspaces", 'set_draw_spaces', {"l_draw-none":0,"l_draw-space":1,"l_draw-tab":2,"l_draw-tab+space":3,"l_draw-eol":4,"l_draw-all":15}, 0, "editview"],
    ["editview_maxundo", 'set_max_undo_levels', 'int,-1,999', -1, "editview"],
    ["editview_tabwidth", 'set_tab_width', 'int,1,32', 4, "editview"],
    ["editview_showrightmargin", 'set_show_right_margin', 'bool', False, "editview"],
    ["editview_rightmarginpos", 'set_right_margin_position', 'int,1,999', 72, "editview"],
    ["editview_highlightmatchingbrackets", 'set_highlight_matching_brackets', 'bool', False, "editview"],
    ["editview_spacesinsteadoftabs", 'set_insert_spaces_instead_of_tabs', 'bool', False, "editview"],
    ["editview_indentontab", 'set_indent_on_tab', 'bool', False, "editview"],
    ["editview_autoindent", 'set_auto_indent', 'bool', True, "editview"],
    ["editview_smarthomeend", 'set_smart_home_end', {"l_home-disabled":0,"l_home-before":1,"l_home-after":2,"l_home-always":3}, 3, "editview"],
    ["editview_style", 'set_stylescheme', None, 'classic', "editview"],
    ["sidepanel_expandlevel", 'set_expand_level', 'int,0,7', 3, 'structbrowser'],
    ["sidepanel_symcolorfromtheme", None, 'bool', False, None],
    ["gui_sidepanelshow", 'showpanel', None, True, "sidepanel"],
    ["gui_bottompanelshow", 'showpanel', None, True, "bottompanel"],
    ["files_trash", None, 'bool', True, None],
    ["files_backup", None, 'bool', False, None],
    ["files_reopenprj", None, 'bool', True, None],
    ["files_lastprj", None, None, None, None],
    ["search_loop", None, 'bool', False, None],
    ["print_1header", None, 'bool', False, None],
    ["print_1header_separator", None, 'bool', True, None],
    ["print_1header_text", None, 'text', "|%f|", None],
    ["print_1header_font", None, 'font', "Sans 8", None],
    ["print_2footer", None, 'bool', False, None],
    ["print_2footer_separator", None, 'bool', True, None],
    ["print_2footer_text", None, 'text', "%F||page %N/%Q", None],
    ["print_2footer_font", None, 'font', "Sans 8", None],
    ["print_margin_1top", None, 'int,0,9999', 0, None],
    ["print_margin_2left", None, 'int,0,9999', 0, None],
    ["print_margin_3right", None, 'int,0,9999', 0, None],
    ["print_margin_4bottom", None, 'int,0,9999', 0, None],
    ["print_nlinesfont", None, 'font', "Monospace 6", None],
    ["print_nlinesinterval", None, 'int,0,50', 5, None],
    ["system_datadir", None, None, '', None],
    ["system_confdir", None, None, '', None],
    ["system_maindir", None, None, '', None],
    ["plugins_list", None, None, [], None],
]


#------------------------------------------------------------------------------


