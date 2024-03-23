# Load imports
import argparse
import sys
import os
import netplotbrain
import pandas as pd
import matplotlib.pyplot as plt


def parse_command_line_args():
    parser = argparse.ArgumentParser(prog="Brain Visualization",
                                     description="Show the node connections of brain fMRI datasets",
                                     epilog="Uses the netplotbrain package")
    parser.add_argument('-d', '--data', nargs="?", default=None, help="Path to the dataset (optional)")
    parser.add_argument('-o', '--output', nargs="?", default=None, help="Output filename (optional)")
    args = parser.parse_args()
    return args.data, args.output


if __name__ == "__main__":
    nodes_path = 'yeo_nodes.csv'
    edges_path, output_filename = parse_command_line_args()
    if not edges_path:
        edges_path = 'yeo_edges.csv'
    if not output_filename:
        output_filename = edges_path.split(".")[0] + ".png"

    # Example node and edges dataframes included with package
    nodes = pd.read_csv(nodes_path, sep=',', index_col=0)
    edges = pd.read_csv(edges_path, sep=',', index_col=0)

    netplotbrain.plot(template='MNI152NLin2009cAsym',
                      template_style='glass',
                      nodes=nodes,
                      node_size=1,
                      edges=edges,
                      view=['LSR', 'AIP'])

    plt.savefig(output_filename, dpi=200)
    plt.close('all')
    print(f"Generated {output_filename}")


# Run: python ph.py -d mx645_8.csv