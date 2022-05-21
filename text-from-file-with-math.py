import obspython as obs
import ast, math, os
import operator as op

# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}

interval = 30
dest_name = ""
file_path = ""
equation = ""
last_mod = 0

# ------------------------------------------------------------

def eval_expr(expr):
    return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)

def update_text():
    global interval
    global file_path
    global dest_name
    global equation
    global last_mod

    dest = obs.obs_get_source_by_name(dest_name)
    if file_path is not None and dest is not None:
        file_mod = os.path.getmtime(file_path)
        if file_mod <= last_mod:
            # return early if file hasn't been modified (release opened obs resources)
            return obs.obs_source_release(dest)
        last_mod = file_mod

        text = get_file_text(file_path)
        text = text.replace(",", "").replace(".", "")
        # if there is no equation just use the number converted from the file and rounded down to a whole number
        if equation != "":
            new_number = math.floor(eval_expr(equation.replace("x", text)))
        else:
            new_number = math.floor(int(text, 10))
        set_source_text(dest, str(new_number))
    obs.obs_source_release(dest)

def get_file_text(file_path):
	file = open(file_path, "r")
	text = file.read()
	file.close()
	return text


def set_source_text(src, string):
    src_settings = obs.obs_source_get_settings(src)
    obs.obs_data_set_string(src_settings, "text", string)
    obs.obs_source_update(src, src_settings)
    obs.obs_data_release(src_settings)


def refresh_pressed(props, prop):
	update_text()

# ------------------------------------------------------------

def script_description():
	return "Updates a text source to the text from a file and applies a given equation to it if provided. Always rounds the result.\n\nBy Matt Hatter"

def script_update(settings):
    global interval
    global file_path
    global dest_name
    global equation

    interval = obs.obs_data_get_int(settings, "interval")
    dest_name = obs.obs_data_get_string(settings, "dest")
    file_path = obs.obs_data_get_string(settings, "file_path")
    equation = obs.obs_data_get_string(settings, "equation")

    obs.timer_remove(update_text)

    if dest_name != "" and file_path != "":
        obs.timer_add(update_text, interval * 1000)

def script_defaults(settings):
	obs.obs_data_set_default_int(settings, "interval", 30)

def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_int(props, "interval", "Update Interval (seconds)", 5, 3600, 1)
    obs.obs_properties_add_path(props, "file_path", "Text File Path", obs.OBS_PATH_FILE, "*.txt", "//")
    obs.obs_properties_add_text(props, "equation", "Equation (use 'x' as variable, e.g. 'x*2')", obs.OBS_TEXT_DEFAULT)

    dest_input = obs.obs_properties_add_list(props, "dest", "Text Destination", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(dest_input, name, name)

        obs.source_list_release(sources)

    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props
