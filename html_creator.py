import os
from bs4 import BeautifulSoup
import random

class start_ops():
    def __init__(self,num_signals):
        self.list = [f"document.getElementById('div1.graph_{x}').style.display = 'none';" for x in range(0,num_signals)]


def html_creator(signal_names: list, signal_graphs: list, overview_graph: str) -> str:
    num_signals = len(signal_names)

    # read in the partial html template
    direct = os.path.split(__file__)[0]
    partial_column_path = os.path.join('Templates', 'partial_column_template.html')
    with open(partial_column_path, 'r') as f:
        partial_html = f.read()

    # initiate variables
    drop_down_ops = ""
    func_ops = ""
    all_graphs = overview_graph.replace("<div>", '<div id="div1.overview">') + "\n"
    graph_ids = {}

    # pull overview id
    soup = BeautifulSoup(overview_graph, "html.parser")
    id = soup.div.findAll('div', class_="plotly-graph-div")[0].get('id')
    hash1 = hex(random.getrandbits(128))[2:-1]
    graph_ids[id] = hash1

    for op in range(0, num_signals):
        # create the options for the drop down menus
        signal_str = f'\n<option value="{op+2}">{signal_names[op]}</option>'
        drop_down_ops += signal_str

        # Create function to change what is displayed
        func_str = """ else if (document.getElementById("dropBox1").value == "{{VALUE_REPLACE}}") {
            {{spec_options}}
        }"""
        spec_str = func_str.replace("{{VALUE_REPLACE}}", str(op+2))
        spec_options = start_ops(num_signals).list
        spec_options[op] = spec_options[op].replace('none', 'block')
        spec_options =  "document.getElementById('div1.overview').style.display = 'none';\n" + "\n".join(spec_options)
        spec_str = spec_str.replace("{{spec_options}}", spec_options)
        func_ops += spec_str

        # pull graph id list (so no divs get duplicate ids)
        soup = BeautifulSoup(signal_graphs[op], "html.parser")
        id = soup.div.findAll('div', class_="plotly-graph-div")[0].get('id')
        hash1 = hex(random.getrandbits(128))[2:-1]
        graph_ids[id] = hash1

        # create html containing all graphs
        all_graphs += signal_graphs[op].replace("<div>", f'<div id="div1.graph_{op}">') + "\n"



    # replace the placeholder text with the dynamically created html strings
    partial_html = partial_html.replace('{{drop_down_options}}', drop_down_ops)
    partial_html = partial_html.replace('{{all_graph}}', all_graphs)

    # replace ids for second set of graphs
    for id in graph_ids:
        all_graphs = all_graphs.replace(id, graph_ids[id])

    # continue replacing placeholder text (some places need replacement to differentiate col1 and col2)
    partial_html = partial_html.replace('{{all_graph2}}', all_graphs.replace("div1", "div2"))
    partial_html = partial_html.replace('{{func1_options}}', func_ops)
    partial_html = partial_html.replace('{{func2_options}}', func_ops.replace("div1", "div2").replace("dropBox1", "dropBox2"))
    partial_html = partial_html.replace('{{start_conditions}}', "\n".join(start_ops(num_signals).list))
    full_html = partial_html.replace('{{start_conditions2}}', ("\n".join(start_ops(num_signals).list).replace("div1", "div2")))

    return(full_html)