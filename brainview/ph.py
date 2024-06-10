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
    parser.add_argument('-d', '--dir', nargs="?", default=None, help="Path to the dataset directory(optional)")
    parser.add_argument('-e', '--edge', nargs="?", default=None, help="Path to the edge list (optional)")
    parser.add_argument('-o', '--output', nargs="?", default=None, help="Output filename (optional)")
    args = parser.parse_args()
    return args.dir, args.edge, args.output


def list_txt_csv_files(directory):
    txt_csv_files = []
    for file in os.listdir(directory):
        if file.endswith(".txt") or file.endswith(".csv"):
            edges_path = os.path.join(directory, file)
            txt_csv_files.append(edges_path)
    return txt_csv_files


def list_txt_csv_files_filtering_original_data_files(directory):
    txt_csv_files = []
    for file in os.listdir(directory):
        if file.startswith("subject_"):
            continue
        if file.endswith(".txt") or file.endswith(".csv"):
            edges_path = os.path.join(directory, file)
            txt_csv_files.append(edges_path)
    return txt_csv_files


if __name__ == "__main__":
    nodes_path = 'yeo_nodes.csv'
    nodes = pd.read_csv(nodes_path, sep=',', index_col=0)
    dir_path, edges_path, output_filename = parse_command_line_args()
    if not dir_path:
        if not edges_path:
            edges_path = 'yeo_edges.csv'
        if not output_filename:
            output_filename = edges_path.split(".")[0] + ".png"

        edges = pd.read_csv(edges_path, sep=',', index_col=0)

        netplotbrain.plot(template='MNI152NLin2009cAsym',
                          template_style='glass',
                          nodes=nodes,
                          node_size=1,
                          edges=edges,
                          view='S')

        plt.savefig(output_filename, dpi=200)
        plt.close('all')
        print(f"Generated {output_filename}")
    else:
        edges_path_list = list_txt_csv_files_filtering_original_data_files(dir_path)
        for edges_path in edges_path_list:
            output_filename = edges_path.split(".")[0] + ".png"
            edges = pd.read_csv(edges_path, sep=',', index_col=0)
            # view=['LSR', 'AIP'] for multiview
            netplotbrain.plot(template='MNI152NLin2009cAsym',
                              template_style='glass',
                              nodes=nodes,
                              node_size=1,
                              edges=edges,
                              view='S')

            plt.savefig(output_filename, dpi=200)
            plt.close('all')
            print(f"Generated {output_filename}")

# Run:
# load a single file of edge list
# python ph.py -e mx645_8.csv
# load a directory of edge list
# python ph.py -d /media/shovon/Codes/GithubCodes/brainview/paper_exp/single_view/random/subject1
# python ph.py -d /media/shovon/Codes/GithubCodes/brainview/paper_exp/single_view/real/subject4
