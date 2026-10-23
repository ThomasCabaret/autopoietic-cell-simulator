"""Local chemistry hook factored from the archived research prototype."""
import numpy as np
from .reference import degree, normals, local_port_free, port_attraction, add_force
from .physics import orientation_kernel
from .physics import attraction_kernel
from .docking import free_faces,update_faces,docking_force

class MembraneChemistry:
    def __init__(self, config, rng):
        self.config, self.rng = config, rng
        n = config.get("units", 16)
        rungs = np.column_stack([np.arange(n), n + np.arange(n)])
        long, short = 1., config.get("short_length", .75)
        shaft = .65
        fragment = config.get("fragment_size", n)
        pos = np.empty((2 * n, 2))
        edges = [set(), set()]
        init = config.get("initial", "straight")
        for start in range(0, n, fragment):
            size = min(fragment, n - start)
            ids = np.arange(start, start + size)
            if init == "straight":
                x = (np.arange(size) - (size - 1) / 2) * (long + short) / 2
                head = np.column_stack([x, np.full(size, shaft / 2)])
                tail = head - [0, shaft]
            else:
                # Preformed fragments; no initial ring or coordinated arrangement.
                angle_step = 2 * np.arcsin((long - short) / (2 * shaft)) if long != short else .001
                angles0 = (np.arange(size) - (size - 1) / 2) * angle_step
                radius = long / (2 * np.sin(angle_step / 2))
                head = np.column_stack([radius * np.sin(angles0), radius * (np.cos(angles0) - 1)])
                tail = head - shaft * np.column_stack([np.sin(angles0), np.cos(angles0)])
                theta = rng.uniform(0, 2 * np.pi)
                rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
                center = rng.uniform(-4, 4, size=2)
                head, tail = head @ rot.T + center, tail @ rot.T + center
            pos[ids], pos[n + ids] = head, tail
            for i in range(start, start + size - 1):
                edges[0].add((i, i + 1))
                edges[1].add((i, i + 1))
        pos += rng.normal(scale=.015, size=pos.shape)
        box = np.array(config["box"]) if "box" in config else None
        if box is not None:
            pos += box / 2
        springs, angles = [], []
        deg = [degree(n, e) for e in edges]
        self.pos = pos
        self.n = n
        self.rungs = rungs
        self.box = box
        self.edges = edges
        self.long = long
        self.short = short
        self.shaft = shaft
        self.deg = deg
        self.kinds = np.zeros(2*n, dtype=np.int64)
        self.contact = np.array([[.40]])
        self.springs = np.empty((0,4))
        self.angles = np.empty((0,5))
        self.mobility = .4
        self.face_links=[]
        if config.get('face_docking',False):
            directions=normals(pos,rungs)
            tangents=np.column_stack((-directions[:,1],directions[:,0]))
            for i,j in sorted(edges[0]&edges[1]):
                a=int(np.dot(pos[j]-pos[i],tangents[i])>0)
                self.face_links.append((i,j,a,1-a))
        self.broken_contacts=0

    def react(self, time, dt, neighbors):
        if self.config.get('face_docking',False):
            self.face_links,broken=update_faces(self.pos,self.face_links,self.config,self.rng,neighbors,dt*5)
            self.broken_contacts+=broken
            contacts={(i,j) for i,j,_,_ in self.face_links}
            self.edges=[contacts.copy(),contacts.copy()]
            self._face_mechanics()
            return []
        config, rng = self.config, self.rng
        events = []
        pos = self.pos
        n = self.n
        rungs = self.rungs
        box = self.box
        edges = self.edges
        long = self.long
        short = self.short
        shaft = self.shaft
        deg = self.deg
        nrm = normals(pos, rungs)
        for row, length in enumerate((long, short)):
            offset = row * n
            available = np.flatnonzero(degree(n, edges[row]) < 2)
            nearby = neighbors.pairs(pos[offset:offset+n], length + .22, "bond" + str(row))
            allowed = set(available.tolist())
            candidates = [(int(i), int(j)) for i, j in nearby if i in allowed and j in allowed]
            if not config.get("bonding", True):
                candidates = []
            rng.shuffle(candidates)
            for i, j in candidates:
                if (i, j) in edges[row]:
                    continue
                d = pos[offset + j] - pos[offset + i]
                distance = np.linalg.norm(d)
                if not length - .22 < distance < length + .22 or np.dot(nrm[i], nrm[j]) < .5:
                    continue
                if abs(np.dot(nrm[i], d)) > .6 * distance or abs(np.dot(nrm[j], d)) > .6 * distance:
                    continue
                rp = pos[offset:offset + n]
                if not local_port_free(i, j, rp, edges[row]) or not local_port_free(j, i, rp, edges[row]):
                    continue
                if config.get("cooperative_rows", False):
                    other = 1 - row
                    other_pos = pos[other * n:(other + 1) * n]
                    other_length = (long, short)[other]
                    if abs(np.linalg.norm(other_pos[j] - other_pos[i]) - other_length) > .18:
                        continue
                    if np.dot(nrm[i], nrm[j]) < .85:
                        continue
                    if (i, j) not in edges[other] and (
                        not local_port_free(i, j, other_pos, edges[other]) or
                        not local_port_free(j, i, other_pos, edges[other])):
                        continue
                if rng.random() < -np.expm1(-25 * dt * 5):
                    edges[row].add((i, j))
                    if config.get("cooperative_rows", False):
                        edges[1 - row].add((i, j))
        springs = [(i, n + i, 180., shaft) for i in range(n)]
        angles = []
        for row, length in enumerate((long, short)):
            offset, opposite = row * n, (1 - row) * n
            for i, j in sorted(edges[row]):
                springs.append((offset + i, offset + j, 120., length))
                angles.extend([(opposite + i, offset + i, offset + j, 1., 0.),
                               (opposite + j, offset + j, offset + i, 1., 0.)])
        deg = [degree(n, e) for e in edges]
        self.springs = np.asarray(springs, dtype=float).reshape(-1,4)
        self.angles = np.asarray(angles, dtype=float).reshape(-1,5)
        return events

    def extra_forces(self, neighbors):
        pos, n = self.pos, self.n
        if self.config.get('face_docking',False):
            free=free_faces(n,self.face_links)
            pairs=neighbors.pairs(pos[:n],self.long+4*self.config['dock_width'],'face_force')
            if self.face_links:
                existing={(i,j) for i,j,_,_ in self.face_links}
                pairs=np.array([(i,j) for i,j in pairs if (i,j) not in existing],dtype=np.int64).reshape(-1,2)
            return docking_force(pos,pairs,free,self.long,self.short,
                                 self.config['dock_energy'],self.config['dock_width'])[0]
        force = np.zeros_like(pos)
        for row, length in enumerate((self.long, self.short)):
            if self.config.get("oriented_ports", False):
                force += port_attraction(pos, self.rungs, self.edges[row], row, length,
                                         self.config.get("port_epsilon", .6), neighbors=neighbors)
                continue
            ids = np.flatnonzero(degree(n, self.edges[row]) < 2) + row*n
            pairs = neighbors.pairs(pos[ids], length+.5, "attraction"+str(row))
            force += attraction_kernel(pos, ids[pairs], length, self.config.get("end_attraction", 4.))
        return force

    def observe(self, callback, time, events):
        callback(time, self.pos, self.edges)

    def bonds(self):
        return {"scaffold": self.rungs.tolist(),
                "backbone": sorted(self.edges[0]) + [(i+self.n,j+self.n) for i,j in sorted(self.edges[1])],
                "pairing": []}

    def colors(self):
        return ["#148e9c"]*self.n + ["#df7947"]*self.n

    def export(self):
        state={"edges": [sorted(row) for row in self.edges]}
        if self.config.get('face_docking',False):
            state.update(face_links=self.face_links,broken_contacts=self.broken_contacts)
        return state

    def restore(self, state):
        self.edges = [{tuple(p) for p in row} for row in state["edges"]]
        self.face_links=[tuple(p) for p in state.get('face_links',[])]
        self.broken_contacts=state.get('broken_contacts',0)

    def _face_mechanics(self):
        n=self.n
        springs=[(i,n+i,180.,self.shaft) for i in range(n)]
        angles=[]
        for row,length in enumerate((self.long,self.short)):
            offset,other=row*n,(1-row)*n
            for i,j in sorted(self.edges[row]):
                springs.append((offset+i,offset+j,120.,length))
                angles.extend(((other+i,offset+i,offset+j,1.,0.),
                               (other+j,offset+j,offset+i,1.,0.)))
        self.springs=np.asarray(springs,dtype=float).reshape(-1,4)
        self.angles=np.asarray(angles,dtype=float).reshape(-1,5)
