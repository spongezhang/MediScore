#!/usr/bin/env python2

import sys
import os
lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../lib")
sys.path.append(lib_path)

import json
import argparse
import pandas as pd
import errno
import collections

from ProvenanceMetrics import *

def err_quit(msg, exit_status=1):
    print(msg)
    exit(exit_status)

def load_json(json_fn):
    try:
        with open(json_fn, 'r') as json_f:
            return json.load(json_f)
    except IOError as ioerr:
        err_quit("{}. Aborting!".format(ioerr))

def load_csv(csv_fn, sep="|"):
    try:
        return pd.read_csv(csv_fn, sep)
    except IOError as ioerr:
        err_quit("{}. Aborting!".format(ioerr))

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            err_quit("{}. Aborting!".format(exc))
        
# Returns ordered array of named tuples representing nodes
def system_out_to_ordered_nodes(system_out):
    node_w_confidence = collections.namedtuple('node_w_confidence', [ 'confidence', 'file' ])
    node_set_w_confidence = [ node_w_confidence(n["nodeConfidenceScore"], n["file"]) for n in system_out["nodes"] ]
    node_set_w_confidence.sort(reverse=True)
    return node_set_w_confidence

def build_provenancefiltering_agg_output_df():
    df = pd.DataFrame(columns=[
                               "MeanAP",
                               "MeanNodeRecall@200",
                               "MeanNodeRecall@300",
                               "BaseMeanNodeRecall@200",
                               "BaseMeanNodeRecall@300",
                               "DonorMeanNodeRecall@200",
                               "DonorMeanNodeRecall@300",
                               "InterMeanNodeRecall@200",
                               "InterMeanNodeRecall@300"
                               ])
    dtypes = { "MeanAP": float,
               "MeanNodeRecall@200": float,
               "MeanNodeRecall@300": float,
               "BaseMeanNodeRecall@200": float,
               "BaseMeanNodeRecall@300": float,
               "DonorMeanNodeRecall@200": float,
               "DonorMeanNodeRecall@300": float,
               "InterMeanNodeRecall@200": float,
               "InterMeanNodeRecall@300": float
               }

    # Setting column data type one by one as pandas doesn't offer a
    # convenient way to do this
    for col, t in dtypes.items():
        df[col] = df[col].astype(t)

    return df

def build_provenancefiltering_output_df():
    df = pd.DataFrame(columns=["JournalName",
                               "ProvenanceProbeFileID",
                               #"ProvenanceOutputFileName",
                               #"NumSysNodes",
                               #"NumRefNodes",
                               "MeanAP",
                               "NodeRecall@200",
                               "NodeRecall@300",
                               "BaseNodeRecall@200",
                               "BaseNodeRecall@300",
                               "DonorNodeRecall@200",
                               "DonorNodeRecall@300",
                               "InterNodeRecall@200",
                               "InterNodeRecall@300" ])
    dtypes = { "JournalName": str,
               "ProvenanceProbeFileID": str,
               "MeanAP": float,
               "NodeRecall@200": float,
               "NodeRecall@300": float,
               "BaseNodeRecall@200": float,
               "BaseNodeRecall@300": float,
               "DonorNodeRecall@200": float,
               "DonorNodeRecall@300": float,
               "InterNodeRecall@200": float,
               "InterNodeRecall@300": float }

    # Setting column data type one by one as pandas doesn't offer a
    # convenient way to do this
    for col, t in dtypes.items():
        df[col] = df[col].astype(t)

    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Score Medifor ProvenanceFiltering task output")
    parser.add_argument("-t", "--skip-trial-disparity-check", help="Skip check for trial disparity between INDEX_FILE and SYSTEM_OUTPUT_FILE", action="store_true")
    parser.add_argument("-o", "--output-dir", help="Output directory for scores", type=str, required=True)
    parser.add_argument("-x", "--index-file", help="Task Index file", type=str, required=True)
    parser.add_argument("-r", "--reference-file", help="Reference file", type=str, required=True)
    parser.add_argument("-n", "--node-file", help="Node file", type=str, required=True)
    parser.add_argument("-d", "--donor-node-file", help="Node file", type=str, required=True)
    parser.add_argument("-b", "--base-node-file", help="Node file", type=str, required=True)
    parser.add_argument("-i", "--inter-node-file", help="Node file", type=str, required=True)
    parser.add_argument("-w", "--world-file", help="World file", type=str, required=True)
    parser.add_argument("-R", "--reference-dir", help="Reference directory", type=str, required=True)
    parser.add_argument("-s", "--system-output-file", help="System output file (i.e. <EXPID>.csv)", type=str, required=True)
    parser.add_argument("-S", "--system-dir", help="System output directory where system output json files can be found", type=str, required=True)
    parser.add_argument("-a", "--additional-suffix", help="System output directory where system output json files can be found", type=str, required=True)
    args = parser.parse_args()

    trial_index = load_csv(args.index_file)
    ref_file = load_csv(args.reference_file)
    nodes_file = load_csv(args.node_file)
    donor_nodes_file = load_csv(args.donor_node_file)
    base_nodes_file = load_csv(args.base_node_file)
    inter_nodes_file = load_csv(args.inter_node_file)
    world_index = load_csv(args.world_file)

    system_output_index = load_csv(args.system_output_file)

    def check_for_trial_disparity():
        # detect missing trials
        ref_probes = [ t.ProvenanceProbeFileID for t in trial_index.itertuples() ]
        remaining_sys_probes = [ t.ProvenanceProbeFileID for t in system_output_index.itertuples() ]

        missing_probes = []
        for probe_id in ref_probes:
            try:
                remaining_sys_probes.remove(probe_id)
            except ValueError:
                missing_probes.append(probe_id)

        errs = []
        if len(missing_probes) > 0:
            errs.append("Error, missing the following ProvenanceProbeFileIDs from the system output:\n{}".format("\n".join(map(lambda p: "\t" + p, missing_probes))))
        if len(remaining_sys_probes) > 0:
            errs.append("Error, extraneous ProvenanceProbeFileIDs in the system output:\n{}".format("\n".join(map(lambda p: "\t" + p, remaining_sys_probes))))

        if len(errs) > 0:
            errs.append("Aborting!")
            err_quit("\n".join(errs))

    if not args.skip_trial_disparity_check:
        check_for_trial_disparity()
            
    trial_index_ref = pd.merge(trial_index, ref_file, on = "ProvenanceProbeFileID")
    trial_index_ref_sysout = pd.merge(trial_index_ref, system_output_index, on = "ProvenanceProbeFileID")

    world_nodes = pd.merge(nodes_file, world_index, on = "WorldFileID", how = "inner")
    donor_world_nodes = pd.merge(donor_nodes_file, world_index, on = "WorldFileID", how = "inner")
    base_world_nodes = pd.merge(base_nodes_file, world_index, on = "WorldFileID", how = "inner")
    inter_world_nodes = pd.merge(inter_nodes_file, world_index, on = "WorldFileID", how = "inner")

    output_records = build_provenancefiltering_output_df()
        
    for trial in trial_index_ref_sysout.itertuples():
        system_out = load_json(os.path.join(args.system_dir, trial.ProvenanceOutputFileName))
        
        probe_node_wfn = trial.ProvenanceProbeFileName_x
        world_set_nodes = { node.WorldFileName_x for node in world_nodes[world_nodes.ProvenanceProbeFileID == trial.ProvenanceProbeFileID].itertuples() }
        donor_world_set_nodes = { node.WorldFileName_x \
                for node in donor_world_nodes[donor_world_nodes.ProvenanceProbeFileID == trial.ProvenanceProbeFileID].itertuples() }
        base_world_set_nodes = { node.WorldFileName_x \
                for node in base_world_nodes[base_world_nodes.ProvenanceProbeFileID == trial.ProvenanceProbeFileID].itertuples() }
        inter_world_set_nodes = { node.WorldFileName_x \
                for node in inter_world_nodes[inter_world_nodes.ProvenanceProbeFileID == trial.ProvenanceProbeFileID].itertuples() }
        world_set_nodes.add(probe_node_wfn)

        ordered_sys_nodes = system_out_to_ordered_nodes(system_out)
        
        sys_nodes_list = [node.file for node in ordered_sys_nodes]
        out_rec = { "JournalName": trial.JournalName,
                    "ProvenanceProbeFileID": trial.ProvenanceProbeFileID,
                    "MeanAP": node_map(world_set_nodes, sys_nodes_list)}

        for n in [ 200, 300]:
            sys_nodes_at_n = { node.file for node in ordered_sys_nodes[0:n] }
            out_rec.update({
                             "DonorNodeRecall@{}".format(n): node_recall(donor_world_set_nodes, sys_nodes_at_n),
                             "BaseNodeRecall@{}".format(n): node_recall(base_world_set_nodes, sys_nodes_at_n),
                             "InterNodeRecall@{}".format(n): node_recall(inter_world_set_nodes, sys_nodes_at_n),
                             "NodeRecall@{}".format(n): node_recall(world_set_nodes, sys_nodes_at_n) })

        output_records = output_records.append(pd.Series(out_rec), ignore_index=True)

    output_agg_records = build_provenancefiltering_agg_output_df()
    aggregated = { 
                   "MeanAP": output_records["MeanAP"].mean(),
                   "DonorMeanNodeRecall@200": output_records["DonorNodeRecall@200"][output_records["DonorNodeRecall@200"]>-0.5].mean(),
                   "DonorMeanNodeRecall@300": output_records["DonorNodeRecall@300"][output_records["DonorNodeRecall@300"]>-0.5].mean(),
                   "BaseMeanNodeRecall@200": output_records["BaseNodeRecall@200"][output_records["BaseNodeRecall@200"]>-0.5].mean(),
                   "BaseMeanNodeRecall@300": output_records["BaseNodeRecall@300"][output_records["BaseNodeRecall@200"]>-0.5].mean(),
                   "InterMeanNodeRecall@200": output_records["InterNodeRecall@200"][output_records["InterNodeRecall@200"]>-0.5].mean(),
                   "InterMeanNodeRecall@300": output_records["InterNodeRecall@300"][output_records["InterNodeRecall@300"]>-0.5].mean(),
                   "MeanNodeRecall@200": output_records["NodeRecall@200"][output_records["NodeRecall@200"]>-0.5].mean(),
                   "MeanNodeRecall@300": output_records["NodeRecall@300"][output_records["NodeRecall@200"]>-0.5].mean(),
                }#[out_rec["DonorNodeRecall@200"]>-0.5]

    output_agg_records = output_agg_records.append(pd.Series(aggregated), ignore_index=True)

    mkdir_p(args.output_dir)
    try:
        with open(os.path.join(args.output_dir, "trial_scores_{}.csv".format(args.additional_suffix)), 'w') as out_f:
            output_records.to_csv(path_or_buf=out_f, sep="|", float_format='%.3f', index=False)
    except IOError as ioerr:
        err_quit("{}. Aborting!".format(ioerr))
    try:
        with open(os.path.join(args.output_dir, "scores_{}.csv".format(args.additional_suffix)), 'w') as out_f:
            output_agg_records.to_csv(path_or_buf=out_f, sep="|", float_format='%.3f', index=False)
    except IOError as ioerr:
        err_quit("{}. Aborting!".format(ioerr))
