import html_creator as hc
import plot
from flapjack import Flapjack
import os

fj_user = "saisam17"
fj_pass = "Il0vem$her"

direct = __file__
shallow_sbol = os.path.join(os.path.split(direct)[0], 'Tests', 'Test_files', 'Sample1.xml')
file_path_out = os.path.join(os.path.split(direct)[0], 'Tests', 'Test_files', 'out.html')
print(shallow_sbol)
# file_path_in = "C:/Users/saisa/Plugin-Visual-Test/tests/test_files/Sample1.xml"

# Flapjack login
fj_url = "flapjack.rudge-lab.org:8000" 
fj = Flapjack(url_base=fj_url)
fj.log_in(username=fj_user, password=fj_pass)
fj_access_token = fj.access_token
signal_names, signal_plots, all_graph = plot.create_signal_graphs(shallow_sbol, fj_access_token)
signal_plots = [x.replace("</body>", "").replace("</html>", "").replace("<body>", "").replace("<html>", "") for x in signal_plots]
all_graph = all_graph.replace("</body>", "").replace("</html>", "").replace("<body>", "").replace("<html>", "")
result = hc.html_creator(signal_names, signal_plots, all_graph)
with open(file_path_out, 'w+') as f:
    f.write(result)

# with open(file_path_out, 'w+') as f:
#     f.write(signal_plots[0])