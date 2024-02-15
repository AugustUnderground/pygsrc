from funcy import *
from functools import reduce
from collections import Counter
from random import randrange
import operator
import re

dropright = lambda n, x: x[:-n]
singleton = lambda e: [e]

def rng_color() -> str:
    hex = compose(rcurry(format)('x'),randrange)(0, int(2 ** 24 - 1), 1)
    return f'#{hex}'

def block2corners(l: str) -> dict[str,tuple[int,int]]:
    idx = l.split(' ',1)[0]
    crn = compose( sorted
                 , eval
                 , lambda c: f'[{c}]'
                 , partial(re.sub,r'\)\s\(','),(')
                 ,''.join
                 , list
                 , curry(dropwhile)(curry(operator.ne)('('))
                 )(l.split(' ',1)[1])
    xmin_,ymin_ = crn[0]
    xmax_,ymax_ = crn[-1]
    w   = xmax_ - xmin_
    h   = ymax_ - ymin_
    return {idx: {'width': w, 'height': h}}

def read_blocks(block_file: str) -> dict[str,dict[str,int]]:
    with open(block_file) as b:
        block_size = reduce( operator.or_
                           , compose( list
                                     , curry(map)(block2corners)
                                     , curry(map)(curry(dropright)(1))
                                     , curry(takewhile)(curry(operator.ne)('\n'))
                                     , curry(drop)(1),curry(dropwhile)(curry(operator.ne)('\n'))
                                     , curry(drop)(1),curry(dropwhile)(curry(operator.ne)('\n'))
                                     )(b.readlines()))
    return block_size

def block2place(l: str) -> dict[str,tuple[int,int]]:
    i,x,y = tuple(l.split('\t'))
    return {i: {'xmin': int(x), 'ymin': int(y)}}

def read_place(pl_file: str) -> dict[str,dict[str,int]]:
    with open(pl_file) as p:
        block_place = reduce( operator.or_
                            , compose( list, curry(map)(block2place)
                                           , curry(map)(curry(dropright)(1))
                                           , curry(takewhile)(curry(operator.ne)('\n'))
                                           , curry(drop)(1),curry(dropwhile)(curry(operator.ne)('\n'))
                                           )(p.readlines()))
    return block_place

def nets2conns(netlist: list[str], nets: list[set[str]]) -> list[set[str]]:
    if netlist:
        deg   = int(netlist[0].split(':')[1])
        nodes = compose( singleton
                       , set
                       , curry(map)(compose( ''.join
                                           , list
                                           , curry(takewhile)(curry(operator.ne)(' '))))
                       , curry(take)(deg)
                       )(netlist[1:])
        res   = nets2conns(list(drop(deg + 1, netlist)), nodes + nets)
    else:
        res   = nets
    return res

def read_nets(net_file: str) -> list[set[str]]:
    with open(net_file) as n:
        block_nets = compose( rcurry(nets2conns)([])
                            , list
                            , curry(map)(curry(dropright)(1))
                            , curry(dropwhile)(lambda l: not l.startswith('NetDegree'))
                            )(n.readlines())
    return block_nets

def connections(bid: str, cons: list[set[str]]):
    return compose( dict, Counter
                  )(reduce( operator.add
                          , [list(c - {bid}) for c in cons if bid in c] ) )

def read_gsrc(base: str, name: str, mode: str):
    path      = f'{base}/{mode}/{name}'
    blocks    = read_blocks(path + '.blocks')
    place     = read_place(path + '.pl')
    nets      = read_nets(path + '.nets')
    block_ids = set(blocks.keys())
    nets_f    = [n & block_ids for n in nets if len(n & block_ids) > 1]
    cons      = { b: { bb: 0 for bb in block_ids if bb != b} | connections(b,nets_f)
                  for b in block_ids}
    return { b: blocks[b] | place[b] | {'connections': cons[b]} | {'color': rng_color()}
            for b in block_ids}
