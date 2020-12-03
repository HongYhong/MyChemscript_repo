from rdkit import Chem
import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument('--input', required=True,help='the path of the input file')
parser.add_argument('--format',help='the output format you want,default is the standard input of autodock vina.Available arguments are vina , json ')
parser.add_argument('--buffer',help='the default value of buffer is 4.')

args = parser.parse_args()

protein = Chem.MolFromPDBFile(args.input)


xcoordinates = []
ycoordinates = []
zcoordinates = []

if args.buffer is None:
    buffer = 4
else:
    buffer = args.buffer

for i in range(0,protein.GetNumAtoms()):
    pos = protein.GetConformer().GetAtomPosition(i)
    xcoordinates.append(pos.x)
    ycoordinates.append(pos.y)
    zcoordinates.append(pos.z)

#edges coordinates of the box
max_x = round(max(xcoordinates) + buffer)
min_x = round(min(xcoordinates) - buffer)
max_y = round(max(ycoordinates) + buffer)
min_y = round(min(ycoordinates) - buffer)
max_z = round(max(zcoordinates) + buffer)
min_z = round(min(zcoordinates) - buffer)

#input parameters for autodock vina
x_center = round((max_x + min_x)/2,2)
y_center = round((max_y + min_y)/2,2)
z_center = round((max_z + min_z)/2,2)
x_size = round(max_x - min_x,2)
y_size = round(max_y - min_y,2)
z_size = round(max_z - min_z,2)




if args.format == None or args.format == 'vina':
    with open('./config.txt','w') as conffile:
        conffile.write('center_x = {}\ncenter_y = {}\ncenter_z = {}\nsize_x = {}\nsize_y = {}\nsize_z = {}\n'.format(x_center,y_center,z_center,x_size,y_size,z_size))
elif args.format == 'json':
    data = [{'center_x' : x_center , 'center_y' : y_center , 'center_z' : y_center , 'size_x' : x_size , 'size_y' : y_size , 'size_z' : z_size , 'max_x' : max_x , 'max_y' : max_y , 'max_z' : max_z , 'min_x' : min_x , 'min_y' : min_y , ' min z' : min_z}]
    with open('./config.json','w') as confjson:
        json.dump(data, confjson)