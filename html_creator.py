import os


def html_creator(signal_names: list, signal_graphs: list, all_graph: str) -> str:
    num_signals = len(signal_names)

    # read in the partial html template
    direct = os.path.split(__file__)[0]
    partial_column_path = os.path.join('Templates', 'partial_column_template.html')
    with open(partial_column_path, 'r') as f:
        partial_html = f.read()

    drop_down_ops = ""
    func_ops1 = ""
    func_ops2 = ""
    for op in range(0, num_signals):
        # create the options for the drop down menus
        signal_str = f'\n<option value="{op+2}">{signal_names[op]}</option>'
        drop_down_ops += signal_str

        # create the function to make the changes to the displayed html
        func_str = """ else if (document.getElementById("dropBox1").value == "VALUE_REPLACE") {
            document.getElementById("divText1").innerHTML = 'GRAPH_REPLACE';
        }"""
        func_str = func_str.replace("VALUE_REPLACE", str(op+2))
        func_str = func_str.replace("GRAPH_REPLACE", signal_graphs[op])
        func_ops1 += func_str

        # for the second function it should change the second column
        func_str2 = func_str.replace('dropBox1', 'dropBox2')
        func_ops2 += func_str2.replace('divText1', 'divText2')

    # replace the placeholder text with the dynamically created html strings
    partial_html = partial_html.replace('{{drop_down_options}}', drop_down_ops)
    partial_html = partial_html.replace('{{all_graph}}', all_graph)
    partial_html = partial_html.replace('{{func1_options}}', func_ops1)
    partial_html = partial_html.replace('{{func2_options}}', func_ops2)

    return(partial_html)