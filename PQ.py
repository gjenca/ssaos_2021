import sys
import copy
from cdiagram import MatrixDiagram,Position
from jinja2 import Template,FileSystemLoader,Environment
from cdutils import triangle_over

env=Environment(loader=FileSystemLoader('.'),
    line_statement_prefix='%%',variable_start_string='<<',variable_end_string='>>')
t=env.get_template('graphs.tex')

p1=MatrixDiagram()
p1.skip()
p1.node('a',label_angle=90)
p1.cr()
p1.node('b')
p1.skip()
p1.node('c')
p1.add_arrow('a','b')
p1.add_arrow('a','c')
p1.label='P'
p1.label_at=(1,2)

p2=MatrixDiagram()
p2.node('d')
p2.skip()
p2.node('e')
p2.cr()
p2.skip()
p2.node('f')
p2.add_arrow('d','f')
p2.add_arrow('e','f')
p2.label='Q'
p2.label_at=(4,2)
p2.cluster_all().shift((3,0))

sys.stdout.write(t.render(diags=(p1,p2)))




