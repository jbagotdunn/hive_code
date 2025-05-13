# for this to work, move alembic archibe node away from oring
node = '/obj/obj_name'
# node = hou.selectedNodes()
material = '/mat/principledshader'

top_node = hou.node(node)
all_nodes = top_node.allNodes()
null_nodes = []

for node in all_nodes:
    if node.type().name() == 'geo':
        node.setParms({'shop_materialpath': material})

    if node.type().name() == 'alembic':
        dir = node.parent().path() + '/'
        null_node = hou.node('/%s' % dir).createNode(
            'null', 'OUT_%s' % node.name())
        node_pos = node.position()
        null_node.setInput(0, node)
        null_nodes.append(null_node.path())

geo_node = hou.node('/obj').createNode('geo', top_node.name())
dir = geo_node.path() + '/'
oms = []

for null_node in null_nodes:
    name = 'om_{}'.format(null_node.split('/')[-1])
    om = hou.node('%s' % dir).createNode('object_merge', name)
    om.setParms({'objpath1': null_node,
                 'xformtype': 1})
    oms.append(om)

merge_node = hou.node('%s' % dir).createNode('merge', 'merge')
for i, om in enumerate(oms):
    merge_node.setInput(i, om)

unpack_node = hou.node('%s' % dir).createNode('unpack', 'unpack')
unpack_node.setInput(0, merge_node)

null_name = 'OUT_{}'.format(top_node.name())
null_node = hou.node('%s' % dir).createNode('null', null_name)
null_node.setInput(0, unpack_node)

output_node = hou.node('%s' % dir).createNode('output', 'output')
output_node.setInput(0, null_node)

# collsions section
for i, om in enumerate(oms):
    collision_node = hou.node('%s' % dir).createNode('collisionsource::2.0',
                                                     'collsion_{}'.format(i))
    collision_node.setInput(0, om)

    geo_col_null_node = hou.node('%s' % dir).createNode('null', 'OUT_geo_coll_null')
    geo_col_null_node.setInput(0, collision_node)

    vdb_col_null_node = hou.node('%s' % dir).createNode('null', 'OUT_geo_VDB_null')
    vdb_col_null_node.setInput(0, collision_node, 1)

hou.Node.layoutChildren(geo_node)