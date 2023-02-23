from typing import (
    Any,
)

OPERATIONS = [
    "+", 
    "-",
]

VARS = {}

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
    if "." in str(value):
        var_name, var_index = value.split(".")
        var_index = _decode_value(var_index)
        return _decode_value(VARS[var_name][var_index])
    elif value in VARS:
        return _decode_value(VARS[value])
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
    VARS[var_name] = _decode_var_value(var_value)
    var = VARS[var_name]
    print(f"{var=}")
    if type(var) == list:
        return
    var_summation = None
    var_previous = None
    var_next = None
    var_operation = None
    for i, v in enumerate(var.split(" ")):
        if v in OPERATIONS:
            var_operation = v
            var_next = _decode_value(var.split(" ")[i+1])
            var_previous = var_summation or _decode_value(var.split(" ")[i-1])
            if var_operation == "+":
                if var_summation is None:
                    var_summation = var_previous + var_next
                else: 
                    var_summation += var_next
            print(f"{var_operation=}\n{var_next=}\n{var_previous=}\n{var_summation=}\n---")
    if var_operation is not None:
        VARS[var_name] = var_summation

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
    if line.startswith("#"): return
    line_segments_if_var = line.split(" = ")
    if len(line_segments_if_var) == 2:
        return _assign_var(line_segments_if_var[0], line_segments_if_var[1])
    line_segments = line.split(" ")
    if line_segments[0] == "out":
        return _output(list(line_segments[1:])[0])

def _run(content: str) -> None:
    for line_content in content.split("\n"):
        _unpack_line(line_content)
        