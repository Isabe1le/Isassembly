from typing import (
    Any,
)

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

def _decode_var_value(var_value) -> Any:
    var_value_list_segments = var_value.split(", ")
    if len(var_value_list_segments) == 1:
        if var_value_list_segments[0][-1] == ",":
            return var_value_list_segments[:-1]
    if len(var_value_list_segments) > 1:
        return var_value_list_segments
    return var_value_list_segments[0]

def _assign_var(var_name: str, var_value: Any) -> None:
    VARS[var_name] = _decode_var_value(var_value)
    var = VARS[var_name]
    print(f"{var=}")
    if type(var) == list:
        return
    values = var.split(" ")
    values_iter = iter(values)
    if not len(values) % 3:
        for i in range(len(values)):
            value1 = next(values_iter)
            operation = next(values_iter)
            value2 = next(values_iter)
            print("")
            # print(f"{values=}")
            # print(f"{next(values_iter)=}")

    # segments_if_list = var_value.split(".")
    # if len(segments_if_list) > 1:
    #     print(f"{var_value=}")
    #     for list_name, index in zip(*[iter(segments_if_list)]*2):
    #         print(f"{list_name=}, {index=}")
    #         index = int(index.split(" ")[0].replace(",",""))
    #         print(f"{index=}")
    #         var_value = _decode_var_value(VARS[list_name][int(index)])
    # VARS[var_name] = _decode_var_value(var_value)

def _output(output: str) -> None:
    if output in VARS:
        return print(VARS[str(output)])
    print(f"{VARS=}")
    print(f"{output=}")

def _unpack_line(line: str) -> None:
    line_segments_if_var = line.split(" = ")
    if len(line_segments_if_var) == 2:
        return _assign_var(line_segments_if_var[0], line_segments_if_var[1])
    line_segments = line.split(" ")
    if line_segments[0] == "out":
        return _output(list(line_segments[1:])[0])

def _run(content: str) -> None:
    for line_content in content.split("\n"):
        _unpack_line(line_content)
        