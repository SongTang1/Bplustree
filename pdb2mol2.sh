#!/bin/bash
dataset=./refined-set
echo $dataset

for pdbfile in $dataset/*/*_pocket.pdb; do
	mol2file=${pdbfile%pdb}mol2
	#if [[ ! -e $mol2file ]]; then
	#	echo -e "open $pdbfile \n addh \n addcharge \n write format mol2 0 tmp.mol2 \n stop" | chimera2 --nogui
	# Do not use TIP3P atom types, pybel cannot read them
	#sed 's/H\.t3p/H    /' tmp.mol2 | sed 's/O\.t3p/O\.3  /' > $mol2file
	#fi
	echo ${mol2file##*/}
	obabel -i pdb $pdbfile -o mol2 -O $mol2file
done 
