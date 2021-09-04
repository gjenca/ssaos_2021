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
p1.node('a',label_angle=-90)
p1.cr()
p1.node('b',label_angle=0)
p1.skip()
p1.node('c',label_angle=180)
p1.add_arrow('a','b')
p1.add_arrow('a','c')
p1.cr()
p1.skip()
p1.node('d',label_angle=0)
p1.skip()
p1.node('e',label_angle=180)
p1.add_arrow('b','d',color='red')
p1.add_arrow('c','e',color='red')
p1.add_arrow('d','c',color='red')
p1.cr()
p1.skip(2)
p1.node('f',label_angle=90)
p1.add_arrow('d','f')
p1.add_arrow('e','f')
p1.label='cog(r)'
p1.label_at=(2,4)
tex_after="\n".join([
    '\pspolygon[linearc=0.2,linestyle=dashed](0.6,1.8)(2,3.3)(3.4,1.8)',
    '\pspolygon[linearc=0.2,linestyle=dashed](-0.4,1.2)(1,-0.3)(2.4,1.2)',
])
sys.stdout.write(t.render(diags=(p1,),tex_after=tex_after))




