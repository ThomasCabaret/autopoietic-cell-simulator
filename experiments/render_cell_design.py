"""Curated specification figures, not a picture of a simulated cell."""
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Circle
from matplotlib.colors import ListedColormap
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.audit_cell_design import load,assess


def graph():
    fig,ax=plt.subplots(figsize=(13,8.5));ax.set_xlim(0,12);ax.set_ylim(0,8);ax.axis('off')
    ax.add_patch(FancyBboxPatch((.2,.3),11.6,6.4,boxstyle='round,pad=.05',facecolor='#f4f8fb',edgecolor='#648a82',linewidth=2))
    ax.text(.4,6.38,'INTERIEUR — cellule construite au depart',fontsize=11,color='#42695f')
    def box(x,y,text,color='#dcecf1',w=2.25,h=.7):
        ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=.08',facecolor=color,edgecolor='#5c7285'))
        ax.text(x,y,text,ha='center',va='center',fontsize=10)
    def arrow(a,b,label='',color='#556b7d',curve=0.,offset=(0,0),dashed=False):
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=14,color=color,
            connectionstyle=f'arc3,rad={curve}',linestyle='--' if dashed else '-',linewidth=1.5))
        if label:
            x=(a[0]+b[0])/2+offset[0];y=(a[1]+b[1])/2+offset[1]
            ax.text(x,y,label,ha='center',fontsize=9,color=color,
                bbox=dict(facecolor='white',alpha=.9,edgecolor='none',pad=1.5))
    box(3.,7.45,'EXTERIEUR\nX / Y / Z + energie E',w=3.5)
    box(9.1,7.45,'EXTERIEUR\npuits de dechet W',w=3.1)
    box(3.,5.65,'X / Y / Z + E\nimportes',w=2.7)
    box(9.1,5.65,'W libre\na exporter',w=2.7)
    arrow((3.,7.02),(3.,6.06),'passage',offset=(-.8,0))
    arrow((9.1,6.06),(9.1,7.02),'sortie',offset=(.7,0))
    for x,label in [(2.,'N0 / N1\nnucleotides'),(6.,'A0 / A1\nacides amines'),(10.,'L\nlipide polaire')]:
        box(x,4.05,label,w=2.5)
    arrow((2.6,5.22),(2.,4.48),'via EN',offset=(-.65,0))
    arrow((4.,5.22),(5.5,4.48),'via EA',offset=(.2,.1))
    arrow((4.45,5.6),(9.5,4.48),'via EL',offset=(.15,.15))
    ax.text(6.2,4.75,'Chaque fabrication consomme E et relache W',ha='center',fontsize=9,color='#6c5b49')
    box(2.,2.2,'gN / gA / gL\n3 genes distincts',w=2.8)
    box(6.,2.2,'EN / EA / EL\n3 chaines fonctionnelles',w=3.)
    box(10.,2.2,'Frontiere\nL inseres et retenus',w=2.8)
    arrow((2.,3.62),(2.,2.63),'copie sur gene\n+ energie',offset=(-1.1,-.15))
    arrow((6.,3.62),(6.,2.63),'matiere A\n+ energie',offset=(1.05,-.15))
    arrow((3.5,2.2),(4.4,2.2),'traduction',offset=(0,.2))
    arrow((10.,3.62),(10.,2.63),'insertion\ndepuis dedans',offset=(1.05,-.15))
    # Causal arrows: tools return to all three synthesis roles. They do not
    # encode new molecular particle types or an engine sequence lookup.
    arrow((5.,1.8),(1.,4.8),'EN → N',color='#bd794a',curve=-.40,offset=(-1.1,-.35),dashed=True)
    arrow((6.,2.63),(6.,3.62),'EA → A',color='#bd794a',curve=-.8,offset=(-1.0,-.2),dashed=True)
    arrow((7.,1.8),(10.9,4.8),'EL → L',color='#bd794a',curve=.4,offset=(.9,-.4),dashed=True)
    ax.text(6.,.82,'La frontiere permet les apports et retient N / A / genes / outils.\n'
        'Les genes et outils initiaux sont permis ; chacun doit etre refabrique.',ha='center',fontsize=10)
    fig.suptitle('Architecture cible : 3 genes, 3 catalyseurs, dependances fermees sous hypotheses',fontsize=14)
    fig.text(.5,.015,'Schema de conception : EN/EA/EL selectifs, transport et insertion restent a demontrer. Fleches orange = dependance catalytique.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.04,1,.95]);fig.savefig(ROOT/'research/CELL_DEPENDENCIES.png',dpi=160);plt.close(fig)


def matrix(spec):
    classes=spec['interaction_classes'];modes=['none','catalytic','template','conditional','insertion','passage','retain']
    colors=['#e7edf1','#d59655','#a9c8df','#e6dca4','#d8756c','#94cbbd','#c5b1da']
    grid=np.zeros((len(classes),len(classes)),dtype=int)
    for r in spec['contact_contracts']:
        i,j=[classes.index(c) for c in r['pair']];grid[i,j]=grid[j,i]=modes.index(r['mode'])
    # The boundary is made of the same L, not an extra chemical species.
    # Its adjacent lipids retain the L--L lateral-contact contract.
    grid[classes.index('boundary'),classes.index('boundary')]=grid[classes.index('L'),classes.index('L')]
    labels=['Nourriture','E / W','N0 / N1','A0 / A1','Lipide L','Genes','EN','EA','EL','Frontiere']
    fig,ax=plt.subplots(figsize=(10,8));ax.imshow(grid,cmap=ListedColormap(colors),vmin=0,vmax=len(modes)-1)
    ax.set_xticks(range(len(labels)),labels,rotation=45,ha='right');ax.set_yticks(range(len(labels)),labels)
    symbols=['·','C','T','?','I','P','R']
    for i in range(len(labels)):
        for j in range(len(labels)):ax.text(j,i,symbols[grid[i,j]],ha='center',va='center',fontsize=12)
    ax.set_title('Contrats a tester : contacts, transport et non-affinite',pad=18)
    fig.text(.5,.02,'C catalyse ; T templating ; ? condition locale ; I insertion ; P passage ; R retention sans adhesion\n'
        '· aucune affinite chimique voulue (collisions mecaniques permises). Toutes ces selectivites restent a tester.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.09,1,1]);fig.savefig(ROOT/'research/CELL_INTERACTIONS.png',dpi=160);plt.close(fig)


def geometry(result):
    b=result['budgets'][1];fig,ax=plt.subplots(figsize=(8,5))
    R=b['membrane_radius'];old=b['current_preferred_radius']
    ax.add_patch(Circle((0,0),R,fill=False,color='#148e9c',lw=2))
    ax.add_patch(Circle((0,0),old,fill=False,color='#df7947',lw=2))
    ax.text(0,R+2,f"Cible nominale : rayon {R:.1f}, environ {b['membrane_molecules']} lipides",ha='center',fontsize=11)
    ax.annotate(f"Preference V8 : rayon {old:.2f}\nenviron {b['current_preferred_units']:.1f} lipides",xy=(old,0),xytext=(R*.28,-R*.35),arrowprops=dict(arrowstyle='->'),fontsize=10)
    ax.set_xlim(-R-6,R+6);ax.set_ylim(-R-5,R+7);ax.set_aspect('equal');ax.axis('off')
    fig.suptitle('Ecart de courbure : deux cercles a la meme echelle')
    fig.text(.5,.02,'Estimation geometrique 2D, pas une simulation. Une membrane construite initialement est autorisee.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.05,1,.95]);fig.savefig(ROOT/'research/CELL_SIZE.png',dpi=160);plt.close(fig)


if __name__=='__main__':
    spec=load();result=assess(spec);graph();matrix(spec);geometry(result)
    print('Three curated design figures generated')
