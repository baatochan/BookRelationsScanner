from flask import json, send_file
import requests


def main(dataJSON, filename):
    try:
        f = open("gephi.gdf", "w")

        nodes = "Pawulon działa"
        f.write(nodes)
        f.close()

        return send_file('../../gephi.gdf', attachment_filename=filename+'.gdf')
    except Exception as e:
        return str(e)


# def gdf_gen(dependendencyTable, personsTable):
#     f = open("gephi.gdf", "w")

#     nodes = gdf_nodes(dependendencyTable, personsTable)
#     f.write(nodes)

#     edges = gdf_edges(dependendencyTable, personsTable)
#     f.write(edges)
#     f.close()


# def gdf_nodes(dependendencyTable, personsTable):
#     node_section = \
#         "nodedef> name VARCHAR, label VARCHAR, class VARCHAR, value DOUBLE\n"

#     for p in range(0, len(personsTable)):
#         occ = dependendencyTable[p][p]
#         node_section += str(p) + "," + personsTable[p] + "," + \
#             personClassification(dependendencyTable, personsTable, occ) + \
#             "," + str(occ) + "\n"

#     return node_section


# def gdf_edges(dependendencyTable, personsTable):
#     edge_section = \
#         "edgedef> source VARCHAR, target VARCHAR, type VARCHAR, value DOUBLE\n"

#     for y in range(0, len(personsTable) - 1):
#         for x in range(y + 1, len(personsTable)):
#             edge = dependendencyTable[y][x]
#             edge_section += str(y) + "," + str(x) + "," + \
#                 connectionClassification(
#                     dependendencyTable, personsTable, edge) + \
#                 "," + str(edge) + "\n"

#     return edge_section


if __name__ == "__main__":
    main(dataJSON)
