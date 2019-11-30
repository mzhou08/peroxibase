import copy
from io import StringIO

from Bio import Phylo
from Bio.Phylo.Applications import PhymlCommandline
from Bio.Phylo.PAML import codeml
from Bio.Phylo.PhyloXML import Phylogeny

tree = Phylo.read("./muscle_Catalase.phy", "newick")
print(tree)



tree.rooted = True
Phylo.draw(tree)