
import sys
import copy

class Position(tuple):

    def __add__(self,other):

        return Position((self[0]+other[0],self[1]+other[1]))

    def __sub__(self,other):

        return Position((self[0]-other[0],self[1]-other[1]))

    def __mul__(self,scalar):

        return Position((self[0]*scalar,self[1]*scalar))

class Node(dict):

    def __init__(self,name,position,**props):

        self.name=name
        self.position=Position(position)
        if 'label' not in props:
            props['label']=name
        dict.__init__(self,props)

    def shift(self,delta):

        self.position=self.position+delta

    def shift_towards(self,goal,factor):

        self.shift((Position(goal)-self.position)*factor)

    def __repr__(self):

        return '\psnode%s{%s}{%s}' %(self.position,self.name,self['label'])

class Cluster(list):

    def shift(self,delta):

        for node in self:
            node.shift(delta)
        return self

    def centroid(self):

        x=float(sum(node.position[0] for nore in self))/len(self)
        y=float(sum(node.position[1] for nore in self))/len(self)

        return x,y

    def __repr__(self):

        return 'Cluster([%s])' % ','.join(repr(node) for node in self)

class Arrow(dict):

    def __init__(self,from_node,to_node,**props):

        self.from_node=from_node
        self.to_node=to_node

        if 'label' in props and props['label'][0] in '_^':
            props['label_position']=props['label'][0]
            props['label']=props['label'][1:]
        dict.__init__(self,props)

class Diagram(dict):

    def __init__(self):

        self.arrows=[]
        self.defaults={}
        super(Diagram,self).__init__()

    def add_node(self,name,position,**props):

        props_default=copy.copy(self.defaults)
        props_default.update(props)
        self[name]=Node(name,position,**props_default)
        return self[name]

    def add_arrow(self,from_name,to_name,**props):

        arr=Arrow(self[from_name],self[to_name],**props)
        self.arrows.append(arr)
        return arr

    def cluster_by_names(self,*names):

        return Cluster(self[name] for name in names)

    def cluster_all(self):

        return Cluster(iter(self.values()))

    def dimensions(self):

        max0=max(node.position[0] for node in self.values())
        max1=max(node.position[1] for node in self.values())
        return max0,max1

    def set_default(self,**props):

        self.defaults=props

    def unset_default(self,*names):

        for name in names:
            if name in self.defaults:
                del self.defaults[name]


class MatrixDiagram(Diagram):

    def __init__(self):

        self.current_row=0
        self.current_col=0
        self.frozen_arrows={}
        self.node_matrix=[]
        self.current_line=[]
        self.node_matrix.append(self.current_line)
        self.last_node=None
        super(MatrixDiagram,self).__init__()

    def cr(self):

        self.current_row+=1
        self.current_col=0
        self.current_line=[]
        self.node_matrix.append(self.current_line)

    def skip(self,cols=1):

        self.current_col+=cols
        self.current_line.extend([None]*cols)

    def node(self,name,**props):

        node=self.add_node(name,(self.current_col,self.current_row),**props)
        self.current_line.append(node)
        self.last_node=node
        current_pos=(self.current_col,self.current_row)
        if current_pos in self.frozen_arrows:
            for frozen_arrow in self.frozen_arrows[current_pos]:
                frozen_arrow(name)
            del self.frozen_arrows[current_pos]

        self.current_col+=1

    def arr(self,direction,**props):

        def make_unfreeze(from_name,**props):

            def unfreeze(to_name):

                self.add_arrow(from_name,to_name,**props)
            return unfreeze

        udlr=[direction.count(c) for c in "udlr"]
        p2delta=udlr[1]-udlr[0]
        p1delta=udlr[3]-udlr[2]
        pos=(self.last_node.position[0]+p1delta,self.last_node.position[1]+p2delta)
        node_to=self.node_by_pos(pos)
        if node_to:
            self.add_arrow(self.last_node.name,node_to.name,**props)
        else:
            if pos not in self.frozen_arrows:
                self.frozen_arrows[pos]=[]
            self.frozen_arrows[pos].append(make_unfreeze(self.last_node.name,**props))

    def rows(self,i1,i2):

        return Cluster(
                node for i in range(i1,i2)
                    for node in self.node_matrix[i]
                        if node is not None)
    def row(self,i):

        return self.rows(i,i+1)

    def columns(self,j1,j2):

        return Cluster(
                row[j]
                for row in self.node_matrix
                    for j in range(j1,j2)
                        if j<len(row) and row[j] is not None
        )

    def column(self,j):

        return self.columns(j,j+1)

    def node_by_pos(self,pos):

        if pos[0]>=len(self.node_matrix):
            return None
        if pos[1]>=len(self.node_matrix[pos[0]]):
            return None
        return self.node_matrix[pos[0]][pos[1]]



if __name__=='__main__':

    d=Diagram()
    d.add_node("A",(0,0))
    d.add_node("B",(1,0))
    d.add_arrow("A","B")
    print(d)
    d1=MatrixDiagram()
    d1.node("A",label="AA")
    print('label of node A ==',d1['A']['label'])
    d1.node("B")
    d1.cr()
    d1.skip()
    d1.node("C")
    d1.node("D")
    d1.add_arrow("A","B",label="f",label_position="^")
    d1.add_arrow("A","C")
    d1.add_arrow("C","B")
    d1.cluster_by_names("A","B").shift((0.5,0.5)).shift((0.2,0))
    print(d1)
    print(d1.row(0))
    print(d1.row(1))
    print(d1.column(2))


