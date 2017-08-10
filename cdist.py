import mdtraj as md
import numpy as np
from collections import OrderedDict
a = md.load('prolig.pdb')
lig = a.top.select('resname LIG')
top = a.top
near_atoms = md.compute_neighbors(a, cutoff=0.5, query_indices=lig)
atoms = top.atoms
print('atoms', atoms)
print(type(near_atoms[0]))
residue_list = []
atom_list = []
h_list = []
for i in atoms:
    if i.index in near_atoms[0].tolist():
        atom_list.append(i.index)
        residue_list.append(i.residue.index)
        if i.element.symbol == 'H':
            print(i.element)
            h_list.append(i.index)

#       print(i.residue.index)
#       print(i.index)
print('atom_list', atom_list)
print(near_atoms)
print(residue_list)
residue_list = list(OrderedDict.fromkeys(residue_list))
phrase = []
for residue in residue_list:
    phrase.append('resid '+str(residue))
jphrase = ' or '.join(phrase)
print(jphrase)
jsel = top.select(jphrase + ' or resname LIG')
print(residue_list)
print('jphrase', jsel)
print(len(atom_list), len(jsel), len(near_atoms[0]))

print('h_list', h_list)
df, bonds = top.to_dataframe()
bonded_list = []
for pairbond in bonds:
    for bond in pairbond:
        print(bond)
        if bond in h_list:
            for atom in pairbond:
                if atom not in h_list and atom not in bonded_list:
                    bonded_list.append(atom)
bonded_list = bonded_list + atom_list
print('atom_list', atom_list)
print('bonded_list', bonded_list)
