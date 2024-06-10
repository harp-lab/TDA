# Load imports
import netplotbrain
import pandas as pd
import matplotlib.pyplot as plt


#Path to node and edge example data on netplotbrain
nodepath = 'https://raw.githubusercontent.com/wiheto/netplotbrain/main/examples/example_nodes.tsv'
edgepath = 'https://raw.githubusercontent.com/wiheto/netplotbrain/main/examples/example_edges.tsv'
#Example node and edges dataframes included with package
nodes = pd.read_csv(nodepath, sep='\t', index_col=0)
edges = pd.read_csv(edgepath, sep='\t', index_col=0)
# netplotbrain.plot(template='MNI152NLin2009cAsym',
#                   nodes=nodes,
#                   edges=edges)
netplotbrain.plot(template='MNI152NLin2009cAsym',
                  nodes=nodes,
                  edges=edges,view='S')



plt.savefig('singleview.png', dpi=150)
plt.close('all')
