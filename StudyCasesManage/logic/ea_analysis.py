import pickle
import numpy as np
import pprint
import seaborn as sns
import matplotlib.pyplot as plt


def save_obj(obj, name):
    with open('./pkl/obj_' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('./pkl/obj_' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def getRank(d):
    sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=False)
    i = 1
    d_rank = {}
    for val in sorted_d:
        d_rank[val[0]] = i
        i = i + 1
    return d_rank


if __name__ == '__main__':
    #comparison manifestos vs timelines
    l1_timelines_manifestos = load_obj('l1_timelines_manifestos')
    l1_timelines_manifestos_rank = getRank(l1_timelines_manifestos)
    l2_timelines_manifestos = load_obj('l2_timelines_manifestos')
    l2_timelines_manifestos_rank = getRank(l2_timelines_manifestos)
    dcorr_timelines_manifestos = load_obj('dcorr_timelines_manifestos')
    dcorr_timelines_manifestos_rank = getRank(dcorr_timelines_manifestos)
    cos_timelines_manifestos = load_obj('cos_timelines_manifestos')
    cos_timelines_manifestos_rank = getRank(cos_timelines_manifestos)

    #comparison relevant query vs timelines
    l1_timelines_relevant = load_obj('l1_timelines_relevant')
    l1_timelines_relevant_rank = getRank(l1_timelines_relevant)
    l2_timelines_relevant = load_obj('l2_timelines_relevant')
    l2_timelines_relevant_rank = getRank(l2_timelines_relevant)
    dcorr_timelines_relevant = load_obj('dcorr_timelines_relevant')
    dcorr_timelines_relevant_rank = getRank(dcorr_timelines_relevant)
    cos_timelines_relevant = load_obj('cos_timelines_relevant')
    cos_timelines_relevant_rank = getRank(cos_timelines_relevant)

    #manifestos
    labels_y = ['L1-Norm', 'L2-Norm',
                'Distance\nCorrelation', 'Cosine\nSimilarity']
    candidates_in_manifestos = []
    values_in_manifestos = []
    values_in_manifestos_labels = []

    for key in l1_timelines_manifestos.keys():
        candidates_in_manifestos.append(key)
        l1_val = l1_timelines_manifestos[key]
        l2_val = l2_timelines_manifestos[key]
        dcorr_val = dcorr_timelines_manifestos[key]
        cos_val = cos_timelines_manifestos[key]
        values_in_manifestos.append((l1_val, l2_val, dcorr_val, cos_val))
        values_in_manifestos_labels.append(("("+str(l1_timelines_manifestos_rank[key])+")\n"+"{:.2f}".format(l1_val),
                                            "("+str(l2_timelines_manifestos_rank[key])+")\n"+"{:.2f}".format(
                                                l2_val),
                                            "("+str(dcorr_timelines_manifestos_rank[key])+")\n"+"{:.2f}".format(
                                                dcorr_val),
                                            "("+str(cos_timelines_manifestos_rank[key])+")\n"+"{:.2f}".format(cos_val)))

    #print(candidates_in_manifestos)
    #print(values_in_manifestos)
    values_in_manifestos_npMatrix = np.array(values_in_manifestos)
    values_in_manifestos_npMatrix_original = np.array(values_in_manifestos)
    for i in [0, 1, 2, 3]:
        values_in_manifestos_npMatrix[:, i] /= np.max(values_in_manifestos_npMatrix[:, i])

    #relevant
    candidates_in_relevant = []
    values_in_relevant = []
    values_in_relevant_labels = []

    for key in l1_timelines_relevant.keys():
        candidates_in_relevant.append(key)
        l1_val = l1_timelines_relevant[key]
        l2_val = l2_timelines_relevant[key]
        dcorr_val = dcorr_timelines_relevant[key]
        cos_val = cos_timelines_relevant[key]
        values_in_relevant.append((l1_val, l2_val, dcorr_val, cos_val))
        values_in_relevant_labels.append(
            ("(" + str(l1_timelines_relevant_rank[key]) + ")\n" + "{:.2f}".format(l1_val),
             "(" + str(l2_timelines_relevant_rank[key]
                       ) + ")\n" + "{:.2f}".format(l2_val),
             "(" + str(dcorr_timelines_relevant_rank[key]
                       ) + ")\n" + "{:.2f}".format(dcorr_val),
             "(" + str(cos_timelines_relevant_rank[key]) + ")\n" + "{:.2f}".format(cos_val)))

    values_in_relevant_npMatrix = np.array(values_in_relevant)
    values_in_relevant_npMatrix_original = np.array(values_in_relevant)
    for i in [0, 1, 2, 3]:
        values_in_relevant_npMatrix[:,
                                    i] /= np.max(values_in_relevant_npMatrix[:, i])
    #print(candidates_in_relevant)
    #print(values_in_relevant)

    labels_values_in_manifestos = np.transpose(np.asarray(values_in_manifestos_labels))
    plt.figure(figsize=(16, 5))
    #heat_map = sns.heatmap(np.transpose(values_in_manifestos_npMatrix), cmap='YlGn', annot=True, linewidths=.5)
    heat_map = sns.heatmap(np.transpose(values_in_manifestos_npMatrix), cmap='Blues',
                           annot=labels_values_in_manifestos, linewidths=.5, fmt='',
                           annot_kws={"size": 17}, cbar=False)
    heat_map.set_yticklabels(labels_y, rotation=0, fontsize=17)
    heat_map.set_xticklabels(candidates_in_manifestos,
                             rotation=25, fontsize=17)
    #cbar = heat_map.collections[0].colorbar
    #cbar.ax.tick_params(labelsize=12)
    plt.xlabel("Candidates", fontsize=18)
    #plt.ylabel("Evaluated Metrics", fontsize=16)
    plt.title("Candidate Timelines versus Manifestos", fontsize=24)
    plt.savefig(
        "Candidate Timelines versus Manifestos - Comparison.pdf", bbox_inches='tight')
    plt.show()

    labels_values_in_relevant = np.transpose(
        np.asarray(values_in_relevant_labels))
    plt.figure(figsize=(16, 5))
    #heat_map = sns.heatmap(np.transpose(values_in_relevant_npMatrix), cmap='YlGn', annot=True, linewidths=.5)
    heat_map = sns.heatmap(np.transpose(values_in_relevant_npMatrix), cmap='Blues',
                           annot=labels_values_in_relevant, linewidths=.5, fmt='',
                           annot_kws={"size": 17}, cbar=False)
    heat_map.set_yticklabels(labels_y, rotation=0, fontsize=17)
    heat_map.set_xticklabels(candidates_in_relevant, rotation=25, fontsize=17)
    #cbar = heat_map.collections[0].colorbar
    #cbar.ax.tick_params(labelsize=12)
    plt.xlabel("Candidates", fontsize=18)
    #plt.ylabel("Evaluated Metrics", fontsize=16)
    plt.title("Candidate Timelines versus Designed Query", fontsize=24)
    plt.savefig(
        "Candidate Timelines versus Designed Query - Comparison.pdf", bbox_inches='tight')
    plt.show()
