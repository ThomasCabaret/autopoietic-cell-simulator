"""Local chemistry hook factored from the archived research prototype."""
import numpy as np
from .reference import degree, normals, local_port_free, port_attraction, add_force
from .physics import orientation_kernel
from .substrates import Substrates
from .dual_faces import react as dual_react,reflected_force
from .assembly import RungAssembly
from .initial import groups,place

class CopyChemistry:
    def __init__(self, config, rng):
        self.config, self.rng = config, rng
        sequence = config.get("sequence", "001011")
        length = len(sequence)
        extra = config.get("free_units", 30)
        alphabet = config.get("alphabet", "01")
        functional_count = config.get("function_units", 0)
        bits = np.array([int(x) for x in sequence] + [int(alphabet[i % len(alphabet)]) for i in range(extra)]
                        + [int(alphabet[i % len(alphabet)]) for i in range(functional_count)])
        # Chemical support kinds: G can provide a templating backbone, F cannot.
        families = np.array([config.get("seed_family", 0)] * length + [0] * extra + [1] * functional_count)
        capacities = np.where(bits == config.get("caps_symbol", -1), 1, 2)
        n = len(bits)
        self.initial_groups=groups(config)
        grouped={q for g in self.initial_groups for q in g['units']}
        group_starts={g['units'][0]:g for g in self.initial_groups}
        for g in self.initial_groups:bits[list(g['units'])]=[int(b) for b in g['sequence']]
        capacities=np.where(bits==config.get('caps_symbol',-1),1,2)
        rungs = np.column_stack([np.arange(n), n + np.arange(n)])
        box = np.array(config.get("box", [10., 7.]))
        pos = np.empty((2 * n, 2))
        pos[:length, 0] = np.arange(length) + (box[0] - length + 1) / 2
        pos[:length, 1] = box[1] / 2 - .45
        pos[n:n + length] = pos[:length] + [0, .45]
        for i in range(length, n):
            if i in group_starts:
                place(group_starts[i],pos,n,box,rng,config.get('initial_min_separation',.60))
                continue
            if i in grouped:continue
            for attempt in range(20000):
                candidate = rng.uniform([.6, .6], box - .6)
                if np.min(np.linalg.norm(pos[:i] - candidate, axis=1)) > config.get("initial_min_separation", .60):
                    break
            else:
                raise RuntimeError("Initial packing jam: enlarge box or reduce initial minimum separation")
            pos[i] = candidate
            angle = rng.uniform(0, 2 * np.pi)
            pos[n + i] = candidate + .45 * np.array([np.cos(angle), np.sin(angle)])
        edges = {(i, i + 1) for i in range(length - 1)} if config.get("template", True) else set()
        for g in self.initial_groups:
            if g['backbone']:edges.update(zip(g['units'][:-1],g['units'][1:]))
        pairing = np.full(n, -1, dtype=int)
        gate = config.get("activation", True)
        cycle = config.get("release", "cycle")
        period, release_time = config.get("period", 60.), config.get("release_time", 10.)
        springs, angles = [], []
        self.pos = pos
        self.bits = bits
        self.families = families
        self.capacities = capacities
        self.n = n
        self.rungs = rungs
        self.box = box
        self.edges = edges
        self.pairing = pairing
        self.gate = gate
        self.cycle = cycle
        self.period = period
        self.release_time = release_time
        self.kinds = np.concatenate((np.zeros(n, dtype=np.int64), np.ones(n, dtype=np.int64)))
        self.contact = np.array([[.70,.28],[.28,0.]])
        self.springs = np.empty((0,4))
        self.angles = np.empty((0,5))
        self.mobility = .25
        self.food=Substrates(self,rng) if config.get('food_pairs',0) else None
        self.copy_pairing=np.full(n,-1,dtype=np.int64)
        self.back_pairs=np.empty((0,2),dtype=np.int64)
        self.assembly=RungAssembly(self,rng) if config.get('constructible',False) else None

    def react(self, time, dt, neighbors):
        if self.assembly is not None:self.assembly.react(self,time,dt,neighbors)
        if self.config.get('dual_faces',False):
            return self._finish(dt,neighbors,dual_react(self,time,dt,neighbors))
        config, rng = self.config, self.rng
        events = []
        pos = self.pos
        bits = self.bits
        families = self.families
        capacities = self.capacities
        n = self.n
        rungs = self.rungs
        box = self.box
        edges = self.edges
        pairing = self.pairing
        gate = self.gate
        cycle = self.cycle
        period = self.period
        release_time = self.release_time
        interval = dt * 5
        deg = degree(n, edges)
        active=rungs[:,1]>=0
        nrm = np.zeros((n,2))
        nrm[active]=normals(pos,rungs[active])
        release = cycle == "cycle" and time % period >= period - release_time
        for i in range(n):
            j = pairing[i]
            if j <= i:
                continue
            rate = .003
            if gate and deg[i] == 0 and deg[j] == 0:
                rate = 5.
            if release:
                rate = 12.
            if cycle == "local" and deg[i] > 0 and deg[j] > 0:
                rate = config.get("local_off_rate", .2)
            if rng.random() < -np.expm1(-rate * interval):
                pairing[i] = pairing[j] = -1
        if self.assembly is None:
            candidates = neighbors.pairs(pos[n:2*n], .3, "recognition")
        else:
            available=np.flatnonzero(active)
            candidates=available[neighbors.pairs(pos[rungs[active,1]],.3,'recognition')]
        candidates = candidates[bits[candidates[:, 0]] == bits[candidates[:, 1]]]
        rng.shuffle(candidates)
        for i, j in candidates:
            if self.assembly is not None and self.assembly.catalyst is not None:
                if self.assembly.catalyst.site_bound[i]>=0 or self.assembly.catalyst.site_bound[j]>=0:continue
            if self.food is not None and (self.food.site_bound[i]>=0 or self.food.site_bound[j]>=0):
                continue
            if pairing[i] >= 0 or pairing[j] >= 0 or np.dot(nrm[i], nrm[j]) > -.5:
                continue
            if release:
                continue
            if families[i] == 1 and families[j] == 1:
                continue
            if families[i] != families[j]:
                g, f = (i, j) if families[i] == 0 else (j, i)
                if deg[g] == 0 or deg[f] > (1 if config.get('gf_end_capture',False) else 0):
                    continue
            end_contact=config.get('gf_end_capture',False) and families[i]!=families[j]
            if config.get("monomer_only_capture", False) and not end_contact and not ((deg[i] > 0) != (deg[j] > 0)):
                continue
            if config.get("product_cooperativity", False):
                support, incoming = (i, j) if deg[i] > 0 else (j, i)
                if end_contact:support,incoming=g,f
                linked_neighbors = [b if a == support else a for a, b in edges if a == support or b == support]
                bound_kinds = [families[pairing[q]] for q in linked_neighbors if pairing[q] >= 0]
                if any(kind != families[incoming] for kind in bound_kinds):
                    continue
            rate = 35. if not gate or deg[i] or deg[j] else .1
            if rng.random() < -np.expm1(-rate * interval):
                pairing[i], pairing[j] = j, i
        # Symmetric completion: any existing edge can supply the parallel edge.
        for i, j in sorted(edges):
            if families[i] != 0 or families[j] != 0:
                continue
            a, b = pairing[i], pairing[j]
            if a < 0 or b < 0 or a == b:
                continue
            pair = tuple(sorted((int(a), int(b))))
            if pair in edges or not config.get("ligation", True):
                continue
            if families[a] != families[b]:
                continue
            d = pos[b] - pos[a]
            distance = np.linalg.norm(d)
            if not .72 < distance < 1.28 or np.dot(nrm[a], nrm[b]) < .5:
                continue
            if abs(np.dot(nrm[a], d)) > .5 * distance or abs(np.dot(nrm[b], d)) > .5 * distance:
                continue
            if not local_port_free(a, b, pos, edges, capacities[a]) or not local_port_free(b, a, pos, edges, capacities[b]):
                continue
            if rng.random() < -np.expm1(-config.get("ligation_rate", 12.) * interval):
                edges.add(pair)
                events.append({"source": (i, j), "formed": pair})
        return self._finish(dt,neighbors,events)

    def _finish(self,dt,neighbors,events):
        config=self.config;n=self.n;edges=self.edges;bits=self.bits
        families=self.families;pairing=self.pairing
        springs = [(i, int(r), 180., .45) for i,r in self.rungs if r>=0]
        angles = []
        for i, j in sorted(edges):
            springs.append((i, j, 100., 1.))
            stiffness = config.get("backbone_angle", 5.)
            preferred = []
            for q in (i, j):
                native = config.get("functional_cosines", {}).get(str(int(bits[q])), 0.)
                # Local pairing state masks native folding during expression.
                preferred.append(native if families[q] == 1 and pairing[q] < 0 else 0.)
            for q,other,value in ((i,j,preferred[0]),(j,i,preferred[1])):
                if families[q]==1 and pairing[q]<0 and config.get('functional_bend_cosines',{}) and not config.get('functional_cosines',{}):
                    continue
                angles.append((int(self.rungs[q,1]),q,other,stiffness,value))
        if config.get('functional_bend_cosines',{}):
            adjacency=[[] for _ in range(n)]
            for i,j in sorted(edges): adjacency[i].append(j); adjacency[j].append(i)
            for j,linked in enumerate(adjacency):
                if families[j]!=1 or len(linked)!=2: continue
                i,k=linked
                if any(pairing[q]>=0 for q in (i,j,k)): continue
                cosine=config['functional_bend_cosines'].get(str(int(bits[j])),0.)
                angles.append((i,j,k,config['functional_bend_strength'],cosine))
        for i in range(n):
            if pairing[i] > i:
                springs.append((int(self.rungs[i,1]), int(self.rungs[pairing[i],1]), 80., 0.))
        if self.food is not None:
            events.extend(self.food.react(self,dt,neighbors))
            springs.extend(self.food.springs())
        if self.assembly is not None and self.assembly.catalyst is not None:
            self.assembly.catalyst.refresh(self)
            springs.extend(self.assembly.catalyst.springs(self))
        self.springs = np.asarray(springs, dtype=float).reshape(-1,4)
        self.angles = np.asarray(angles, dtype=float).reshape(-1,5)
        if config.get('dual_faces',False):
            self.back_pairs=np.array([(i,int(j)) for i,j in enumerate(self.copy_pairing) if j>i],dtype=np.int64).reshape(-1,2)
        return events

    def extra_forces(self, neighbors):
        pairs = np.array([(i, int(j)) for i, j in enumerate(self.pairing) if j > i], dtype=np.int64).reshape(-1,2)
        force=orientation_kernel(self.pos, self.rungs, pairs)
        if self.config.get('dual_faces',False):
            force+=orientation_kernel(self.pos,self.rungs,self.back_pairs)
            force+=reflected_force(self.pos,self.back_pairs,self.n)[0]
        if self.food is not None: force+=self.food.forces(self,neighbors)
        if self.assembly is not None and self.assembly.catalyst is not None:
            force+=self.assembly.catalyst.forces(self,neighbors)
        return force

    def observe(self, callback, time, events):
        if self.assembly is not None:
            callback(time,self.pos,self.edges,self.pairing,self.bits,events,self.families)
            if hasattr(callback,'observe_assembly'):callback.observe_assembly(self,time)
            return
        if self.config.get('dual_faces',False):
            callback(time,self.pos,self.edges,self.pairing,self.bits,events,self.families,
                     self.food.export() if self.food is not None else None,self.copy_pairing)
            return
        if self.food is None:
            callback(time, self.pos, self.edges, self.pairing, self.bits, events, self.families)
        else:
            callback(time,self.pos,self.edges,self.pairing,self.bits,events,self.families,self.food.export())

    def bonds(self):
        pairs = [(int(self.rungs[i,1]), int(self.rungs[j,1])) for i,j in enumerate(self.pairing) if j>i]
        if self.config.get('dual_faces',False):pairs += [(int(i),int(j)) for i,j in self.back_pairs]
        bonds={"scaffold": self.rungs[self.rungs[:,1]>=0].tolist(), "backbone": sorted(self.edges), "pairing": pairs}
        if self.food is not None:
            bonds['backbone'] += [(2*self.n+a,2*self.n+b) for a,b in sorted(self.food.products)]
            bonds['pairing'] += [(self.n+i,2*self.n+int(f)) for i,f in enumerate(self.food.site_bound) if f>=0]
        if self.assembly is not None and self.assembly.catalyst is not None:
            bonds['pairing'] += [(int(self.rungs[i,1]),int(p)) for i,p in enumerate(self.assembly.catalyst.site_bound) if p>=0]
        return bonds

    def colors(self):
        palette = ["#148e9c", "#df7947", "#8d75bb"]
        colors=["#718594" if f == 0 else "#9a4aa0" for f in self.families] + [palette[int(b)] for b in self.bits]
        if self.assembly is not None:
            colors=colors[:self.n]+[palette[int(b)] for b in self.assembly.atom_bits]
        if self.food is not None: colors += [palette[f%2] for f in range(self.food.count)]
        return colors

    def export(self):
        state={"edges": sorted(self.edges), "pairing": self.pairing.tolist()}
        if self.config.get('dual_faces',False):state['copy_pairing']=self.copy_pairing.tolist()
        if self.food is not None: state['food']=self.food.export()
        if self.assembly is not None:state['assembly']=self.assembly.export(self)
        return state

    def restore(self, state):
        self.edges = {tuple(p) for p in state["edges"]}
        self.pairing = np.array(state["pairing"], dtype=np.int64)
        if self.assembly is not None:self.assembly.restore(self,state['assembly'])
        if self.config.get('dual_faces',False):
            self.copy_pairing=np.array(state['copy_pairing'],dtype=np.int64)
            self.back_pairs=np.array([(i,int(j)) for i,j in enumerate(self.copy_pairing) if j>i],dtype=np.int64).reshape(-1,2)
        if self.food is not None:
            self.food.restore(state['food']);self.food.refresh(self)
