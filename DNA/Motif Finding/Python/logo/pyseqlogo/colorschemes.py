## Credits: Weblogo project http://weblogo.threeplusone.com/manual.html
import six
basepairing = {
    'G': 'blue',
    'C': 'blue',
    'T': 'darkorange',
    'A': 'darkorange',
    'U': 'darkorange'
}

meme = {'G': 'orange', 'A': 'red', 'C': 'blue', 'T': 'darkgreen'}

classic = {
    'G': 'orange',
    'T': 'red',
    'U': 'red',
    'C': 'blue',
    'A': 'darkgreen'
}

hydrophobicity = {
    'R': 'blue',
    'K': 'blue',
    'D': 'blue',
    'E': 'blue',
    'N': 'blue',
    'Q': 'blue',
    'S': 'darkgreen',
    'G': 'darkgreen',
    'H': 'darkgreen',
    'T': 'darkgreen',
    'A': 'darkgreen',
    'P': 'darkgreen',
    'Y': 'black',
    'V': 'black',
    'M': 'black',
    'C': 'black',
    'L': 'black',
    'F': 'black',
    'I': 'black',
    'W': 'black'
}

chemistry = {
    'G': 'darkgreen',
    'S': 'darkgreen',
    'T': 'darkgreen',
    'Y': 'darkgreen',
    'C': 'darkgreen',
    'Q': 'purple',
    'N': 'purple',
    'K': 'blue',
    'R': 'blue',
    'H': 'blue',
    'D': 'red',
    'E': 'red',
    'A': 'black',
    'V': 'black',
    'L': 'black',
    'I': 'black',
    'P': 'black',
    'W': 'black',
    'F': 'black',
    'M': 'black'
}

cbb_palette_values = [
    "#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2",
    "#D55E00", "#CC79A7"
]
cbb_palette_colors = [
    'black', 'orange', 'skyblue', 'green', 'yellow', 'blue', 'red', 'magenta'
]
cbb_palette = dict(list(zip(cbb_palette_colors, cbb_palette_values)))

# CINEMA
"""
Cinema
Multiple sequence alignment program (Parry-Smith, D.J., Payne, A.W.R, Michie, A.D. and
Attwood, T.K. (1997) "CINEMA - A novel Colour INteractive Editor for Multiple Alignments."
Gene, 211(2), GC45-56)

blue: polar positive H, K, R
red: polar negative D, E
green: polar neutral S, T, N,Q
white: non-polar aliphatic A, V, L, I, M
purple: non-polar aromatic F, Y, W
brown: P, G
yellow: C
"""


def _unwrap_dict(dict_of_list):
    unwrapped_dict = {}
    for key, values in six.iteritems(dict_of_list):
        if not isinstance(values, list):
            values = [values]
        for value in values:
            if value in list(unwrapped_dict.keys()):
                raise ValueError('Duplicated key : {}'.format(value))
            unwrapped_dict[value] = key
    return unwrapped_dict


cinema = {
    'blue': ['H', 'K', 'R'],
    'red': ['D', 'E'],
    'green': ['S', 'T', 'N', 'Q'],
    'black': ['A', 'V', 'I', 'L', 'M'],
    'purple': ['F', 'Y', 'W'],
    'yellow': ['C']
}

# Lesk
"""
Lesk
Lesk A.M. (2002) Introduction to Bioinformatics, Oxford University Press, page 187
yellow: small nonpolar G, A, S, T
green: hydrophobic C, V, I, L, P, F, Y, M, W
magenta: polar N, Q, H
red: negatively charged D, E
blue: positively charged K, R
"""
lesk = {
    'yellow': ['G', 'A', 'S', 'T'],
    'green': ['C', 'V', 'U', 'L', 'P', 'F', 'Y', 'M', 'W'],
    'red': ['D', 'E'],
    'blue': ['K', 'R']
}

# Mod. Cinema
"""
Mod. Cinema
Modified Cinema
blue: polar positive H, K, R
red: polar negative D, E
green: hydrophobic V, L, I, M
dark green: non-polar aromatic F, Y, W
purple: polar neutral S, T, N,Q
light blue A, P, G, C
"""
mod_cinema = {
    'blue': ['H', 'K', 'R'],
    'red': ['D', 'E'],
    'green': ['V', 'L', 'I', 'M'],
    'darkgreen': ['F', 'Y', 'W'],
    'purple': ['S', 'T', 'N', 'Q'],
    'lightblue': ['A', 'P', 'G', 'C']
}
# IMGT
imgt = {
    'R': '#E60606',
    'K': '#C64200',
    'Q': '#FF6600',
    'N': '#FF9900',
    'E': '#FFCC00',
    'D': '#FFCC99',
    'H': '#FFFF99',
    'P': '#FFFF00',
    'Y': '#CCFFCC',
    'W': '#CC99FF',
    'S': '#CCFF99',
    'T': '#00FF99',
    'G': '#00FF00',
    'A': '#CCFFFF',
    'M': '#99CCFF',
    'C': '#00FFFF',
    'F': '#00CCFF',
    'L': '#3366FF',
    'V': '#0000FF',
    'I': '#000080',
}

physiochemical = {
    '#1B04AC': ['A', 'I', 'L', 'V'],
    '#FFFF00': ['P'],
    '#CCFFCC': ['Y'],
    '#CC99FF': ['W'],
    '#00FF00': ['G'],
    '#00CCFF': ['F'],
    '#CCECFF': ['C', 'M'],
    '#89F88B': ['S', 'T'],
    '#FFCC00': ['D', 'E'],
    '#CCA504': ['N', 'Q'],
    '#EC1504': ['R', 'H', 'K']
}

clustalx = {
    'blue': ['A', 'I', 'L', 'M', 'F', 'W', 'V'],
    'red': ['K', 'R'],
    'magenta': ['E', ' D'],
    'green': ['N', 'Q', 'S', 'T'],
    'pink': ['C'],
    'orange': ['G'],
    'cyan': ['P'],
    'yellow': ['H', 'Y']
}

rasmol = {
    '#E60A0A': ['D', 'E'],
    '#E6E600': ['C', 'M'],
    '#145AFF': ['K', 'R'],
    '#FA9600': ['S', 'T'],
    '#3232AA': ['F', 'Y'],
    '#00DCDC': ['N', 'Q'],
    '#EBEBEB': ['G'],
    '#0F820F': ['L', 'V', 'I'],
    '#C8C8C8': ['A'],
    '#B45AB4': ['W'],
    '#8282D2': ['H'],
    '#DC9682': ['P'],
}

default_colorschemes = {
    'basepairing': basepairing,
    'meme': meme,
    'classic': classic,
    'hydrophobicity': hydrophobicity,
    'chemistry': chemistry,
    'imgt': imgt,
    'mod_cinema': _unwrap_dict(mod_cinema),
    'cinema': _unwrap_dict(cinema),
    'lesk': _unwrap_dict(lesk),
    'physiochemical': _unwrap_dict(physiochemical),
    'clustalx': _unwrap_dict(clustalx),
    'rasmol': _unwrap_dict(rasmol)
}
