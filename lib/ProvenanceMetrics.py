import numpy as np

def set_similarity_overlap(set_1, set_2):
    return 2 * np.float64(len(set_1 & set_2)) / (len(set_1) + len(set_2))

def SimNLO(nodeset_1, edgeset_1, nodeset_2, edgeset_2):
    return 2 * np.float64(len(nodeset_1 & nodeset_2) + len(edgeset_1 & edgeset_2)) / (len(nodeset_1) + len(nodeset_2) + len(edgeset_1) + len(edgeset_2))

def SimNO(nodeset_1, nodeset_2):
    return set_similarity_overlap(nodeset_1, nodeset_2)

def SimLO(edgeset_1, edgeset_2):
    return set_similarity_overlap(edgeset_1, edgeset_2)

def node_recall(ref_nodeset, sys_nodeset):
    if len(ref_nodeset)==0:
        return -1.0
    return np.float64(len(ref_nodeset & sys_nodeset)) / len(ref_nodeset)

def node_map(ref_nodeset, sys_nodeset):
    gt_number = len(ref_nodeset)
    total_count = 0
    right_count = 0
    ap = 0.0
    for node in sys_nodeset:
        total_count+=1
        if node in ref_nodeset:
            right_count+=1
            ap = ap + right_count/float(total_count)/float(gt_number)
    return np.float64(ap)
