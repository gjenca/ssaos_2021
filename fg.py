import sys
import copy
from cdiagram import MatrixDiagram,Position
from jinja2 import Template,FileSystemLoader,Environment
from cdutils import triangle_over

env=Environment(loader=FileSystemLoader('.'),
    line_statement_prefix='%%',variable_start_string='<<',variable_end_string='>>')
t=env.get_template('rels.tex')

relf=MatrixDiagram()
for (l,r) in zip('123','abc'):
    relf.node(l,label_angle=180)
    relf.node(r,label_angle=0)
    relf.add_arrow(l,r)
    relf.cr()
relf.add_arrow('3','a')
relf.label_at=(0.5,-0.5)
relf.label='f'
relg=MatrixDiagram()
for (l,r) in zip('123','abc'):
    relg.node(l,label_angle=180)
    relg.node(r,label_angle=0)
    relg.add_arrow(l,r)
    relg.cr()
relg.cluster_all().shift((1.5,0))
relg.add_arrow('2','a')
relg.add_arrow('3','b')
relg.label_at=(2,-0.5)
relg.label='g'
sys.stdout.write(t.render(diags=(relf,relg)))




