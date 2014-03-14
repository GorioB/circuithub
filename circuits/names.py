import random

def giveName():
	n= ['Asimov','Scalzi',
	'Herbert','Adams',
	'Card',
	'Doctorow','Gaiman',
	'Gibson','Orwell',
	'Huxley','Clarke',
	'Vonnegut','Heinlein',
	'King','Riddle',
	'Atwood','Mieville',
	'Martin','Rothfuss']

	a = ['Anteater','Cat',
	'Groundhog','Porcupine',
	'Hyena','Mole',
	'Stallion','Tapir',
	'Koala','Dog',
	'Muskrat','Crow',
	'Weasel','Newt',
	'Reindeer','Jerboa',
	'Cheetah','Snake',
	'Platypus','Dinosaur']

	c = ['Amaranth','Amber','Amethyst',
	'Burgundy','Carmine','Chartreuse',
	'Cobalt','Lavender','Magenta',
	'Mauve','Periwinkle','Turquoise',
	'Sapphire','Auburn','Plum',
	'Ocher','Maroon','Purple',
	'Cerulian','Vermilion']
	i,j,k = random.randint(0,18),random.randint(0,19),random.randint(0,19)
	return (n[i]+a[j]+c[k])[:20]
