from typing import (
    Any,
    Union,
)

OPERATIONS = [
    "+", 
    "-",
    "/",
    "*",
    "**",
]

VARS = {}
POINTS = {}

def run(filepath: str) -> None:
    with open(filepath) as fp:
        content = fp.read()
    syntax_check = _check_syntax(content)
    if syntax_check:
        return _run(content)
    raise SyntaxError(f"Incorrect syntax: {syntax_check}")

def _check_syntax(content: str) -> bool:
    return True

def _decode_value(value: Any) -> None:
    if "." in str(value) and not isinstance(value, float):
        var_name, var_index = value.split(".")
        var_index = _decode_value(var_index)
        return _decode_value(VARS[var_name][var_index])
    elif value in VARS:
        return _decode_value(VARS[value])
    else:
        if "." in str(value):
            return float(value)
        else:
            return int(value)


def _decode_var_value(var_value: Any) -> Any:
    var_value_list_segments = var_value.split(", ")
    if len(var_value_list_segments) == 1:
        if var_value_list_segments[0][-1] == ",":
            print(f"{var_value_list_segments=}")
            return var_value_list_segments[0][:-1]
    if len(var_value_list_segments) > 1:
        temp = []
        for segment in var_value_list_segments:
            temp.append(_decode_value(segment))
        return temp
    return var_value_list_segments[0]

def _assign_var(var_name: str, var_value: Any) -> None:
    var = var_value
    # print(f"{var=}")
    if isinstance(_decode_var_value(var_value), list):
        VARS[var_name] = _decode_var_value(var_value)
        return
    var_summation = None
    var_previous = None
    var_next = None
    var_operation = None
    for i, v in enumerate(var.split(" ")):
        if v in OPERATIONS:
            var_operation = v
            var_next = _decode_value(var.split(" ")[i+1])
            # print(var.split(" "))
            var_previous = var_summation or _decode_value(var.split(" ")[i-1])
            # print(f"{var_operation=}\n{var_next=}\n{var_previous=}\n{var_summation=}\n---")

            if var_operation == "+":
                if var_summation is None:
                    var_summation = var_previous + var_next
                else: 
                    var_summation += var_next
            elif var_operation == "-":
                if var_summation is None:
                    var_summation = var_previous - var_next
                else: 
                    var_summation -= var_next
            elif var_operation == "/":
                if var_summation is None:
                    var_summation = var_previous / var_next
                else: 
                    var_summation /= var_next
            elif var_operation == "*":
                if var_summation is None:
                    var_summation = var_previous * var_next
                else: 
                    var_summation *= var_next
            elif var_operation == "**":
                if var_summation is None:
                    var_summation = var_previous ** var_next
                else: 
                    var_summation **= var_next
    if var_operation is not None:
        VARS[var_name] = var_summation
        return
    VARS[var_name] = _decode_var_value(var_value)

def _fully_decode(item: str) -> int:
    while True:
        output = _decode_value(item)
        if output == item:
            return output
        else:
            item = output

def _output(output: str) -> None:
    if output in VARS:
        output = VARS[str(output)]
    final_out = ""
    if isinstance(output, list):
        for item in output:
            final_out += f"{_fully_decode(item)}, "
        final_out = final_out[:-2]
    else:
        final_out = _fully_decode(output)
    return print(f"OUT: {final_out}")

def _unpack_line(line: str) -> None:
    for tvar in VARS:
        VARS[tvar] = _fully_decode(VARS[tvar])
    if line.startswith("#"): return
    line_segments_if_var = line.split(" = ")
    if len(line_segments_if_var) == 2:
        return _assign_var(line_segments_if_var[0], line_segments_if_var[1])
    line_segments = line.split(" ")
    if line_segments[0] == "out":
        return _output(list(line_segments[1:])[0])
    elif line_segments[0] == "outstr":
        return print(line[7::])

def _run(content: Union[str, list]) -> None:
    if isinstance(content, str):
        lines = content.split("\n")
    else:
        lines = content
    no_run = False
    for line_no, line in enumerate(lines):
        if line.startswith("startpoint"):
            POINTS[line.split(" ")[1]] = {
                "start": line_no,
                "end": None,
                "lines": []
            }
            no_run = True
        elif line.startswith("endpoint"):
            POINTS[line.split(" ")[1]]["end"] = line_no
            no_run = False
        elif line.startswith("goto"):
            _, point, branchtype, arg1, condition, arg2 = line.split(" ")
            for pline_no, pline in enumerate(lines):
                if pline_no > POINTS[point]["start"] and pline_no < POINTS[point]["end"]:
                    POINTS[point]["lines"].append(pline)            
            if branchtype == "until":
                run = True
                while run:
                    arg1_decode = _fully_decode(arg1)
                    if "." in str(arg1_decode):
                        arg1_decode = float(arg1_decode)
                    else:
                        arg1_decode = int(arg1_decode)

                    arg2_decode = _fully_decode(arg2)
                    if "." in str(arg2_decode):
                        arg2_decode = float(arg2_decode)
                    else:
                        arg2_decode = int(arg2_decode)
                    if condition == ">":
                        if arg1_decode > arg2_decode: run = False
                    elif condition == "=":
                        if arg1_decode == arg2_decode: run = False
                    elif condition == ">=":
                        if arg1_decode >= arg2_decode: run = False
                    elif condition == "<":
                        if arg1_decode < arg2_decode: run = False
                    elif condition == "<=":
                        if arg1_decode <= arg2_decode: run = False
                    _run(POINTS[point]["lines"])
            elif branchtype == "if":
                run = False
                arg1_decode = _fully_decode(arg1)
                if "." in str(arg1_decode):
                    arg1_decode = float(arg1_decode)
                else:
                    arg1_decode = int(arg1_decode)

                arg2_decode = _fully_decode(arg2)
                if "." in str(arg2_decode):
                    arg2_decode = float(arg2_decode)
                else:
                    arg2_decode = int(arg2_decode)
                if condition == ">":
                    if arg1_decode > arg2_decode: run = True
                elif condition == "=":
                    if arg1_decode == arg2_decode: run = True
                elif condition == ">=":
                    if arg1_decode >= arg2_decode: run = True
                elif condition == "<":
                    if arg1_decode < arg2_decode: run = True
                elif condition == "<=":
                    if arg1_decode <= arg2_decode: run = True
                if run:
                    _run(POINTS[point]["lines"])
        elif line.startswith("input"):
            _, var_name = line.split(" ")
            VARS[var_name] = _fully_decode(input(""))

        if not no_run:
            _unpack_line(line)
