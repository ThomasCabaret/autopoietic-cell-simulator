"""Generate a curated, single-page SVG atlas from the conditional cell specification.

This is documentation only. No network, simulation, sequence synthesis or engine
modification. Layout is explicit code; quantities and reactions use the auditor.
"""
import argparse,hashlib,json,os,sys
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.audit_cell_design import network,audit,sizing

W,H=2080,1480
INK='#19313b';MUTED='#667b80';PAPER='#f5f3ed';GOLD='#b5812d';WASTE='#b96d53'


def load_model(annotation_path=None):
    path=Path(annotation_path) if annotation_path else ROOT/'research/metabolism_map.json'
    annotations=json.loads(path.read_text(encoding='utf-8'))
    spec=json.loads((ROOT/annotations['specification']).read_text(encoding='utf-8'))
    if [r['id'] for r in spec['roles']]!=['N','A','L']:
        raise ValueError('Review the three-lane layout before adding/removing a functional role')
    if annotations['genome']['organization']!='one_strand_per_gene':raise ValueError('Review genome layout')
    if set(annotations['genome']['sequences'])!={r['gene'] for r in spec['roles']}:raise ValueError('Gene annotation drift')
    if len(annotations['current']['notes'])>4:raise ValueError('Review the evidence panel layout for more than four lines')
    nominal=next(c for c in spec['sizing']['cases'] if c['id']=='nominal')
    model=network(spec,nominal['length']);checked=audit(spec,model)
    if not checked['conditionally_regenerable']:raise ValueError(checked)
    current=json.loads((ROOT/annotations['current']['scenario']).read_text(encoding='utf-8'))
    g=current['chemistry']['genetics'];prepared=1+sum(x['family']==0 and x.get('backbone',True) for x in g['initial_assemblies'])
    return dict(spec=spec,annotations=annotations,nominal=nominal,network=model,
        budget=sizing(spec,nominal),current_sequence=g['sequence'],current_gene_copies=prepared,
        provenance={str(p):hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
            [annotations['specification'],'research/metabolism_map.json',annotations['current']['scenario'],
             'experiments/audit_cell_design.py','experiments/build_metabolism_map.py','docs/metabolism/viewer.html.in']})


class SVG:
    def __init__(self):self.items=[]
    def add(self,value):self.items.append(value)
    def text(self,x,y,text,size=20,color=INK,weight=400,anchor='start',tracking=None):
        track=f' letter-spacing="{tracking}"' if tracking is not None else ''
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}"{track}>{escape(str(text))}</text>')
    def lines(self,x,y,lines,size=18,color=MUTED,leading=26,**kwargs):
        for i,line in enumerate(lines):self.text(x,y+i*leading,line,size,color,**kwargs)
    def rect(self,x,y,w,h,fill='white',stroke='none',radius=16,width=1):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def path(self,d,color=INK,width=3,arrow=False,dash=False,halo=False):
        if halo:self.add(f'<path d="{d}" fill="none" stroke="{PAPER}" stroke-width="{width+8}" stroke-linecap="round" stroke-linejoin="round"/>')
        marker=f' marker-end="url(#arrow-{color[1:]})"' if arrow else ''
        pattern=' stroke-dasharray="7 7"' if dash else ''
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{marker}{pattern}/>')
    def circle(self,x,y,r,fill,stroke='none',width=1):
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def pill(self,x,y,label,color,width=100):
        self.rect(x,y,width,30,color,radius=15);self.text(x+width/2,y+21,label,14,'white',600,'middle')


def equation(reaction):
    def side(values):return ' + '.join((str(n)+' ' if n!=1 else '')+s for s,n in values.items())
    return side(reaction['inputs'])+'  →  '+side(reaction['outputs'])


def build_svg(m):
    a,s=m['annotations'],m['spec'];length=m['nominal']['length'];n=len(s['roles']);b=m['budget']
    v=SVG();v.add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="map-title map-desc">')
    v.add('<title id="map-title">'+escape(a['title'])+'</title>')
    v.add('<desc id="map-desc">Trois gènes séparés, trois synthétases visées. Précurseurs et énergie alimentent copie, expression et membrane. Spécification conditionnelle, séquences inconnues et recyclage non résolu.</desc>')
    v.add('<metadata id="map-data">'+escape(json.dumps(dict(specification=s['id'],provenance=m['provenance'],network=m['network'],network_scope='Nominal budget only; functional lengths and sequences remain unknown'),ensure_ascii=False))+'</metadata>')
    v.add('<defs>')
    for color in (INK,MUTED,GOLD,WASTE,'#147e9a','#7850a6','#278568'):
        v.add(f'<marker id="arrow-{color[1:]}" markerWidth="10" markerHeight="10" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L8 4 L0 8" fill="none" stroke="{color}" stroke-width="2"/></marker>')
    v.add('<linearGradient id="cell-fill" x2="0" y2="1"><stop stop-color="#ffffff"/><stop offset="1" stop-color="#f1f6f2"/></linearGradient>')
    v.add('<style>text{font-family:"Segoe UI",Arial,sans-serif} .lane{transition:opacity .18s} .map-focus .lane:not(.selected){opacity:.16} .role-hit{cursor:pointer}</style></defs>')
    v.rect(0,0,W,H,PAPER,radius=0)
    # Editorial header and a deliberately visible distinction between target and proof.
    v.text(60,56,'AUTOPOIETIC CELL SIMULATOR',16,MUTED,600,tracking=3)
    v.text(60,117,a['title'],52,INK,650)
    v.text(62,155,a['subtitle'],22,MUTED)
    v.rect(1410,35,610,143,'#e6ede6',radius=20)
    v.text(1435,70,f'{n} GÈNES / TAILLES INCONNUES',28,INK,650)
    v.text(1435,103,'La fonction devra déterminer la longueur du brin.',18,MUTED)
    v.text(1435,131,f'{length} bases : scénario de budget, aucune prédiction.',17,MUTED)
    v.pill(60,192,'CIBLE CONDITIONNELLE',INK,224)
    v.text(308,214,'Traits colorés : matière',17,MUTED)
    v.path('M550 207 H602',GOLD,3,arrow=True,dash=True)
    v.text(620,214,'Catalyse : outil conservé',17,MUTED)
    v.text(1010,214,'Matrice conservée ≠ matière du produit',17,MUTED)
    v.text(2020,214,a['reviewed']+f' · révision {a.get("revision",1):02d}',16,MUTED,anchor='end')
    # Compartment boundary is a diagram convention, never exported to dynamics.
    v.rect(274,266,1502,900,'url(#cell-fill)','#9fbdad',64,3)
    v.rect(287,279,1476,874,'none','#d0ddd2',54,2)
    v.text(320,308,'INTÉRIEUR · membrane, gènes et outils construits au départ',16,'#507664',600)
    v.text(60,307,'EXTÉRIEUR',16,MUTED,600,tracking=2)
    v.text(1810,307,'SORTIES',16,MUTED,600,tracking=2)
    # External source and finite-domain flux.
    v.rect(55,368,174,238,'white','#dbdfd6',22)
    v.text(78,403,'Apports',25,INK,600)
    for i,(label,color) in enumerate((('X',INK),('Y',INK),('Z',INK),('E',GOLD))):
        v.circle(90,440+i*41,12,color);v.text(119,447+i*41,label,22,color,600)
    v.lines(60,650,['Création au bord','du domaine, puis','diffusion.'],17)
    v.lines(60,751,['Débits réglables,','concentrations','non garanties.'],17)
    v.path('M230 450 H320 Q340 450 340 430 V352 Q340 340 355 340 H1660',INK,3,arrow=True)
    v.text(390,332,'PRÉCURSEURS X / Y / Z  ·  réservoir partagé',16,MUTED,600)
    v.path('M230 565 H310 Q322 565 322 550 V380 Q322 366 338 366 H1620',GOLD,2.5,arrow=True)
    v.text(1135,359,'E activé · apport externe déclaré',15,GOLD)
    # Spent carrier: the same W appears in each reaction, collected here by alias.
    v.rect(1810,377,214,180,'#f5e8df',radius=22)
    v.text(1834,419,'W',40,WASTE,600)
    v.lines(1834,455,['Porteur déchargé','issu des synthèses,','copies et expressions.'],17,WASTE,24)
    v.path('M1744 466 H1801',WASTE,3,arrow=True)
    v.lines(1810,598,['Diffusion vers dehors,','puis absorption au','bord du domaine.'],17)
    v.text(1715,453,'W',21,WASTE,600)
    v.lines(1810,729,['E → W conserve','le porteur ; l’énergie','est dissipée.'],17,WASTE)
    # Shared precursor and energy branches to all synthesis roles.
    for cx in (560,1040,1520):
        v.path(f'M{cx-55} 340 V408',INK,2.5,arrow=True)
        v.path(f'M{cx+55} 366 V408',GOLD,2.5,arrow=True)
    # Three role-specific paths. Positions are explicit, chemistry is data driven.
    for idx,role in enumerate(s['roles']):
        rid,gene,tool=role['id'],role['gene'],role['tool'];meta=a['roles'][rid];color=meta['color'];cx=560+480*idx
        v.add(f'<g class="lane role-hit" data-role="{rid}"><title>{escape(gene+" → "+tool+" : "+meta["enzyme"]+". Séquence non assignée ; fonction visée.")}</title>')
        # The enzyme's local catalytic feedback, not its consumption.
        v.path(f'M{cx-130} 780 H{cx-171} V481 H{cx-154}',GOLD,3,arrow=True,dash=True)
        v.text(cx-166,714,'catalyse',15,GOLD,anchor='middle')
        v.rect(cx-155,412,310,130,'white','#d9e1dc',18)
        v.text(cx-133,441,f'{idx+1:02d}  /  {meta["name"].upper()}',16,color,600)
        reactions=[r for r in m['network']['reactions'] if r['kind']=='synthesis' and tool in r['catalysts']]
        for j,r in enumerate(reactions):
            v.add(f'<g id="reaction-{r["id"]}">');v.text(cx-133,476+29*j,equation(r),20,INK,500);v.add('</g>')
        v.text(cx-133,526,meta['status'],15,MUTED)
        v.path(f'M{cx} 545 V578',color,4,arrow=True)
        v.rect(cx-101,582,202,87,color,radius=21)
        v.text(cx,618,' / '.join(role['products']),30,'white',600,'middle')
        v.text(cx,647,meta['description'],15,'white',anchor='middle')
        # Tools expressed from each corresponding gene, folds shown as an icon.
        v.add(f'<g id="species-{tool}">');v.rect(cx-130,740,260,82,'white','#d4ddda',20)
        v.text(cx-105,775,tool,30,color,600);v.text(cx-105,801,'outil à renouveler',16,MUTED)
        pts=[(cx+52,778),(cx+71,759),(cx+90,790),(cx+110,768)]
        v.path('M'+' L'.join(f'{x} {y}' for x,y in pts),color,3)
        for x,y in pts:v.circle(x,y,5,'white',color,2)
        v.add('</g>')
        # Expression requires both the gene template and A stock (shared bus).
        v.add(f'<g id="reaction-express_{tool}">')
        v.path(f'M{cx} 943 V824',MUTED,2.5,arrow=True)
        v.circle(cx,887,8,'white',color,2)
        v.text(cx+17,857,'expression directe',16,MUTED)
        v.text(cx+17,925,'matrice conservée',15,MUTED)
        v.add('</g>')
        # Single strand per gene. Unknown bars deliberately contain no invented sequence.
        v.add(f'<g id="species-{gene}">');v.rect(cx-155,947,310,141,'white',color,20,1.5)
        sequence=a['genome']['sequences'][gene]
        v.text(cx-132,982,gene,30,color,600);v.text(cx+132,979,'Taille inconnue',18,MUTED,anchor='end')
        if sequence is None:
            for q in range(6):
                for x in (cx-129+q*17,cx+29+q*17):v.rect(x,1001,12,16,'#d3dfdc',radius=3)
            v.text(cx,1017,'…',23,MUTED,anchor='middle')
        else:
            for q in range(len(sequence)):
                v.rect(cx-129+q*258/len(sequence),1001,max(2,258/len(sequence)-3),16,'#d3dfdc',radius=3)
        v.text(cx-132,1045,sequence if sequence else 'Séquence à concevoir',18,INK)
        v.text(cx-132,1072,'Un brin distinct · copies séparées',16,MUTED)
        v.add('</g>')
        # N feeds copies of every gene, including the genes that make N and A.
        v.add(f'<g id="reaction-copy_{gene}">')
        v.path(f'M{cx} 1125 V1093',a['roles']['N']['color'],3,arrow=True)
        v.add('</g>')
        v.add('</g>')
    # Shared amino-acid distribution to ALL three expression processes.
    ac=a['roles']['A']['color'];nc=a['roles']['N']['color'];lc=a['roles']['L']['color']
    v.path('M1145 625 H1257 Q1275 625 1275 644 V875 Q1275 887 1260 887 H560',ac,3.5,halo=True)
    v.path('M1275 887 H1520',ac,3.5)
    for cx in (560,1040,1520):v.circle(cx,887,6,ac)
    v.rect(650,861,357,29,'#f1ecf7',radius=8);v.text(828,882,'A0/A1 + E → chacun des trois outils + W',15,ac,anchor='middle')
    # N backbone bus is routed below every gene, making the causal loop explicit.
    v.path('M455 625 H352 Q336 625 336 642 V1110 Q336 1125 353 1125 H1530',nc,3.5,halo=True)
    for cx in (560,1040,1520):v.circle(cx,1125,5,nc)
    v.text(1009,1150,'Copie : gᵢ + N0/N1 + E → gᵢ + nouvelle copie gᵢ + W',17,nc,anchor='middle')
    # L reaches and joins the membrane from the interior, never by global repair.
    v.add('<g id="reaction-insert_L">')
    v.path('M1626 625 H1710 Q1746 625 1746 652 V973',lc,4,arrow=True)
    v.lines(1773,894,['L arrive depuis','l’intérieur ; échange','local et refermeture.'],16,lc,24)
    for j in range(8):
        y=990+j*17;v.circle(1740,y,6,lc);v.circle(1756,y,5,'#9ec9b1');v.path(f'M1740 {y} H1756',lc,2)
    v.add('</g>')
    v.text(1808,1072,'FRONTIÈRE DE L',16,lc,600)
    v.lines(1810,1101,['Retient N/A, gènes','et outils ; laisse','passer les apports.'],16,MUTED,23)
    # Gene-copy/energy bookkeeping: exact formal ledger, not a kinetic claim.
    v.text(335,1199,f'Budget hypothétique séparé : {length} bases/brin ; {m["nominal"]["gene_copies"]} copies/gène → {n*length*m["nominal"]["gene_copies"]} bases présentes. Total : {b["total_beads"]:,} billes. Tailles réelles inconnues.'.replace(',',' '),17,MUTED)
    # Bottom information is readable on one poster, not hidden behind tooltips.
    foot_y=1240
    for x,width in ((60,620),(710,620),(1360,660)):v.rect(x,foot_y,width,200,'white','#dce2da',18)
    v.text(84,1274,'01 / FERMETURE CAUSALE VISÉE',17,INK,600)
    v.lines(84,1307,[
        'EN produit les N : copies de gN, gA et gL.',
        'EA produit les A : chaînes EN, EA et EL, y compris elle-même.',
        'EL produit L : renouvellement de la frontière.',
        'Matrices et catalyseurs conservés ; réactifs + énergie requis.',
        f'Comptabilité : {s["assembly_energy_per_dimer"]} E/dimère, {s["polymerization_energy_per_bond"]} E/liaison de chaîne.',
        'Copie/expression : motifs locaux génériques, sans outil dédié.'
    ],17,MUTED,25)
    v.text(734,1274,'02 / DÉCHETS, RECYCLAGE & LIMITES',17,INK,600)
    v.lines(734,1307,[
        'W sort ; fragments et constituants usés restent à traiter.',
        'Fragments → précurseurs : mécanisme de recyclage à choisir.',
        'Pas de sortie magique des gros déchets, pas de gène ajouté.',
        'Homéostasie : éviter accumulation et extinction des gènes.',
        'X/Y/Z et E/W : notation cible, pas encore la chimie du moteur.'
    ],17,MUTED,25)
    v.text(1384,1274,'03 / CE QUI TOURNE AUJOURD’HUI',17,INK,600)
    v.lines(1384,1307,[
        f'{a["current"]["baseline"]} : un gène {m["current_sequence"]} de {len(m["current_sequence"])} bases, {m["current_gene_copies"]} copies initiales.',
        *a['current']['notes']
    ],17,MUTED,25)
    v.text(60,1466,'CARTE DE CONCEPTION · aucune reconnaissance de gène ou de cellule entière dans les lois · les noms EN/EA/EL désignent des assemblages à concevoir',14,MUTED)
    v.text(2020,1466,'Sources + génération : docs/metabolism',14,MUTED,anchor='end')
    v.add('</svg>');result='\n'.join(v.items)+'\n';ET.fromstring(result);return result


def build_html(svg):
    template=(ROOT/'docs/metabolism/viewer.html.in').read_text(encoding='utf-8')
    if template.count('<!-- GENERATED_MAP -->')!=1:raise ValueError('Expected one SVG slot')
    return template.replace('<!-- GENERATED_MAP -->',svg)


def preview(svg,png):
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    from PySide6.QtGui import QGuiApplication,QImage,QPainter,QFontDatabase
    from PySide6.QtSvg import QSvgRenderer
    from PySide6.QtCore import QByteArray,Qt
    app=QGuiApplication.instance() or QGuiApplication([])
    # Offscreen Windows Qt can have no enumerated system fonts in the sandbox.
    # Load fonts explicitly for QA; the distributed SVG keeps editable text.
    if not QFontDatabase.families():
        fontdir=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'
        for filename in ('segoeui.ttf','seguisb.ttf','segoeuib.ttf'):
            if (fontdir/filename).exists():QFontDatabase.addApplicationFont(str(fontdir/filename))
    if not QFontDatabase.families():raise RuntimeError('No font available for SVG QA')
    renderer=QSvgRenderer(QByteArray(svg.encode('utf-8')))
    if not renderer.isValid():raise ValueError('SVG did not load in Qt')
    img=QImage(W,H,QImage.Format.Format_ARGB32);img.fill(Qt.GlobalColor.white)
    painter=QPainter(img);renderer.render(painter);painter.end()
    png=Path(png);png.parent.mkdir(parents=True,exist_ok=True)
    if not img.save(str(png)):raise OSError('PNG write failed')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--preview',type=Path);args=p.parse_args()
    model=load_model();svg=build_svg(model);folder=ROOT/'docs/metabolism';folder.mkdir(parents=True,exist_ok=True)
    (folder/'metabolism.svg').write_text(svg,encoding='utf-8')
    (folder/'index.html').write_text(build_html(svg),encoding='utf-8')
    if args.preview:preview(svg,args.preview)
    print(json.dumps(dict(svg='docs/metabolism/metabolism.svg',html='docs/metabolism/index.html',
        genes=len(model['spec']['roles']),functional_lengths='unknown',
        nominal_budget_bases_per_gene=model['nominal']['length'],
        nominal_budget_genetic_bases=len(model['spec']['roles'])*model['nominal']['length'],
        conditional_audit_passed=True),ensure_ascii=False))


if __name__=='__main__':main()
