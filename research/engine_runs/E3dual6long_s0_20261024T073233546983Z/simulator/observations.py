"""Analysis only: graph census and lineage are unavailable to the chemistry."""
import numpy as np

def components(n, edges):
    adj = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)
    seen, result = set(), []
    for i in range(n):
        if i in seen:
            continue
        stack, comp = [i], set()
        while stack:
            j = stack.pop()
            if j in comp:
                continue
            comp.add(j)
            stack.extend(adj[j])
        seen.update(comp)
        ends = [j for j in comp if len(adj[j]) == 1]
        order = []
        if len(comp) == 1:
            order = [i]
        elif ends or all(len(adj[j]) == 2 for j in comp):
            current, previous = min(ends) if ends else min(comp), -1
            while current not in order:
                order.append(current)
                nxt = [j for j in adj[current] if j != previous]
                if not nxt:
                    break
                previous, current = current, nxt[0]
        result.append((comp, order, bool(not ends and len(comp) >= 3)))
    return result


def simple_polygon(points):
    for i in range(len(points)):
        a, b = points[i], points[(i + 1) % len(points)]
        for j in range(i + 2, len(points)):
            if i == 0 and j == len(points) - 1:
                continue
            c, d = points[j], points[(j + 1) % len(points)]
            cross = lambda u, v: u[0] * v[1] - u[1] * v[0]
            if cross(b - a, c - a) * cross(b - a, d - a) < 0 and cross(d - c, a - c) * cross(d - c, b - c) < 0:
                return False
    return True


def area(points):
    return .5 * abs(np.sum(points[:, 0] * np.roll(points[:, 1], -1) - points[:, 1] * np.roll(points[:, 0], -1)))


class CopyObserver:
    def __init__(self, config):
        self.target = config.get("sequence", "001011")
        self.initial_count = len(self.target)
        self.complete, self.detached = set(), set()
        self.history, self.frames, self.times, self.edges_frames = [], [], [], []
        self.pairing_frames = []
        self.events = []
        self.new_source_events = self.complete_source_events = 0
        self.best_partial = 0
        self.translated, self.translated_detached = set(), set()
        self.edge_parent = {}
        self.certified = {tuple(range(self.initial_count)): 0} if config.get("template", True) and config.get("seed_family", 0) == 0 else {}
        self.last_shapes = []
        self.food_events=[]; self.food_turnovers={}; self.last_food=None
        self.food_edges_frames=[]; self.food_binding_frames=[]
        self.copy_pairing_frames=[];self.last_copy_pairing=None
        self.coexistence_enabled=bool(config.get('dual_faces',False) or (config.get('free_units',0) and config.get('function_units',0)))
        self.joint_detached_ever=False;self.joint_tool_events=0

    def __call__(self, time, pos, edges, pairing, bits, events, families=None, food=None,copy_pairing=None):
        unpaired=lambda i:pairing[i]<0 and (copy_pairing is None or copy_pairing[i]<0)
        self.last_copy_pairing=None if copy_pairing is None else copy_pairing.copy()
        food_events=[e for e in events if e.get('kind')=='food']
        events=[e for e in events if e.get('kind')!='food']
        if families is None:
            families = np.zeros(len(bits), dtype=int)
        comp_list = components(len(bits), edges)
        active_full = set()
        for comp, order, cycle in comp_list:
            if order and not cycle and all(families[i] == 0 for i in comp):
                text = "".join(str(int(bits[i])) for i in order)
                if text in (self.target, self.target[::-1]):
                    active_full.add(tuple(sorted(comp)))
        # Only a previously observed, still complete parent can certify ancestry.
        prior = {key: gen for key, gen in self.certified.items() if key in active_full}
        for event in events:
            source = event["source"]
            parents = [key for key in prior if all(i in key for i in source)]
            self.edge_parent[tuple(sorted(event["formed"]))] = parents[0] if len(parents) == 1 else None
        correct_now = []
        detached_g_now=[];detached_f_now=[]
        self.last_shapes = []
        for comp, order, cycle in comp_list:
            if order and len(order) > 1 and all(families[i] == 1 for i in comp):
                p = pos[order]
                self.last_shapes.append({"sequence": "".join(str(int(bits[i])) for i in order),
                                         "contains_initial_material": any(i < self.initial_count for i in comp),
                                         "units": len(comp),
                                         "end_to_end": float(np.linalg.norm(p[-1] - p[0])),
                                         "radius_of_gyration": float(np.sqrt(np.mean(np.sum((p - p.mean(axis=0)) ** 2, axis=1))))})
            if not order or cycle or any(i < self.initial_count for i in comp):
                continue
            text = "".join(str(int(bits[i])) for i in order)
            if not all(families[i] == families[order[0]] for i in comp):
                raise AssertionError("Mixed chemical backbones violate family compatibility")
            if families[order[0]] == 1:
                if text in (self.target, self.target[::-1]):
                    key = tuple(sorted(comp))
                    self.translated.add(key)
                    if all(unpaired(i) for i in comp):
                        self.translated_detached.add(key)
                        detached_f_now.append(key)
                continue
            if text in self.target or text[::-1] in self.target:
                self.best_partial = max(self.best_partial, len(text))
            if text in (self.target, self.target[::-1]):
                key = tuple(sorted(comp))
                self.complete.add(key)
                correct_now.append(comp)
                parents = [self.edge_parent.get(tuple(sorted((order[q], order[q + 1]))))
                           for q in range(len(order) - 1)]
                if parents and parents[0] in prior and all(p == parents[0] for p in parents):
                    self.certified.setdefault(key, prior[parents[0]] + 1)
                if all(unpaired(i) for i in comp):
                    self.detached.add(key)
                    detached_g_now.append(key)
        if detached_g_now and detached_f_now:self.joint_detached_ever=True
        for e in events:
            source = e["source"]
            if all(i >= self.initial_count for i in source):
                self.new_source_events += 1
            if any(all(i in comp for i in source) for comp in correct_now):
                self.complete_source_events += 1
            self.events.append({"time": time, **e})
        if food is not None:
            self.last_food=food
            for e in food_events:
                support=e['support']; key=None; exact=False; certified=False
                if all(i>=0 for i in support):
                    for comp,order,cycle in comp_list:
                        if len(comp)<2 or not all(i in comp for i in support) or not all(families[i]==1 for i in comp): continue
                        key=tuple(sorted(comp))
                        text=''.join(str(int(bits[i])) for i in order)
                        exact=not cycle and text in (self.target,self.target[::-1])
                        parents=[self.edge_parent.get(tuple(sorted((order[q],order[q+1])))) for q in range(len(order)-1)]
                        certified=(exact and all(i>=self.initial_count and pairing[i]<0 for i in comp)
                                   and bool(parents) and parents[0] is not None and all(p==parents[0] for p in parents))
                        break
                item=dict(time=time,**e,chain=list(key) if key else None,exact_chain=exact,
                          expressed_certified=certified)
                self.food_events.append(item)
                if certified: self.food_turnovers[key]=self.food_turnovers.get(key,0)+1
                if certified and correct_now:self.joint_tool_events+=1
        if not self.times or time - self.times[-1] >= .49:
            self.times.append(time)
            if getattr(self, 'record_trajectory', True):
                self.frames.append(pos.copy())
                self.pairing_frames.append(pairing.copy())
                if copy_pairing is not None:self.copy_pairing_frames.append(copy_pairing.copy())
                mat = np.zeros((len(bits), len(bits)), dtype=np.uint8)
                for i, j in edges:
                    mat[i, j] = mat[j, i] = 1
                self.edges_frames.append(mat)
                if food is not None:
                    nf=len(food['food_bound']); fm=np.zeros((nf,nf),dtype=np.uint8)
                    for a,b in food['products']: fm[a,b]=fm[b,a]=1
                    self.food_edges_frames.append(fm)
                    self.food_binding_frames.append(np.array(food['site_bound'],dtype=np.int64))
            self.history.append({"time": time, "edges": len(edges),
                                 "paired_sites": int(np.count_nonzero(pairing >= 0)),
                                 "complete_ever": len(self.complete), "detached_ever": len(self.detached),
                                 "translated_ever": len(self.translated), "translated_detached_ever": len(self.translated_detached),
                                 "certified_max_generation": max(self.certified.values(), default=0)})
        self.last_bits = bits.copy()
        self.last_families = families.copy()

    def summary(self):
        metrics={"complete_copy_sets_ever": len(self.complete), "detached_copy_sets_ever": len(self.detached),
                "complete_sets": sorted(self.complete), "detached_sets": sorted(self.detached),
                "best_matching_fragment": self.best_partial,
                "ligation_events": len(self.events), "ligations_using_new_chains": self.new_source_events,
                "ligations_using_complete_copies": self.complete_source_events,
                "translated_chains_ever": len(self.translated),
                "translated_detached_ever": len(self.translated_detached),
                "translated_sets": sorted(self.translated),
                "certified_generations": [{"units": list(key), "generation": gen} for key, gen in sorted(self.certified.items()) if gen > 0],
                "certified_max_generation": max(self.certified.values(), default=0),
                "certified_detached_generation2": sum(key in self.detached and gen >= 2 for key, gen in self.certified.items()),
                "ancestry_criterion": "Every backbone edge comes from the same previously complete still-intact parent; observation only",
                "functional_chain_shapes_final": self.last_shapes,
                "sequence_convention": "unoriented chain: sequence identified up to reversal",
                "history": self.history, "events": self.events}
        if self.last_food is not None:
            metrics.update(food_products=len(self.last_food['products']),
                food_double_bound_ligations=sum(all(i>=0 for i in e['support']) for e in self.food_events),
                food_chain_supported_ligations=sum(e['chain'] is not None for e in self.food_events),
                food_exact_chain_ligations=sum(e['exact_chain'] for e in self.food_events),
                food_expressed_tool_ligations=sum(e['expressed_certified'] for e in self.food_events),
                food_max_turnovers_per_expressed_tool=max(self.food_turnovers.values(),default=0),
                food_events=self.food_events)
        if self.coexistence_enabled:
            metrics.update(joint_detached_ever=int(self.joint_detached_ever),
                           food_ligations_with_new_G_present=self.joint_tool_events)
        return metrics


class VesicleObserver:
    def __init__(self, config):
        self.n = config.get("units", 16)
        self.frames, self.times, self.edges_frames, self.history = [], [], [], []
        self.closed_sets = set()

    def __call__(self, time, pos, edges):
        closed = []
        largest, turns = 0, []
        tail_edges = set(edges[1])
        for comp, order, cycle in components(self.n, edges[0]):
            largest = max(largest, len(comp))
            if len(order) >= 3:
                d = np.diff(pos[order], axis=0)
                turns.extend(np.arctan2(d[:-1, 0] * d[1:, 1] - d[:-1, 1] * d[1:, 0],
                                       np.sum(d[:-1] * d[1:], axis=1)).tolist())
            matching = all(tuple(sorted((order[i], order[(i + 1) % len(order)]))) in tail_edges
                           for i in range(len(order))) if cycle else False
            if cycle and matching and simple_polygon(pos[order]) and simple_polygon(pos[self.n + np.array(order)]):
                a = area(pos[order])
                if a > 1:
                    closed.append({"units": len(comp), "area": a})
                    self.closed_sets.add(tuple(sorted(comp)))
        self.times.append(time)
        if getattr(self, 'record_trajectory', True):
            mat = np.zeros((2, self.n, self.n), dtype=np.uint8)
            for row in (0, 1):
                for i, j in edges[row]:
                    mat[row, i, j] = mat[row, j, i] = 1
            self.frames.append(pos.copy())
            self.edges_frames.append(mat)
        self.history.append({"time": time, "closed": closed, "largest_head_component": largest,
                             "mean_signed_turn_deg": float(np.rad2deg(np.mean(turns))) if turns else 0.,
                             "head_edges": len(edges[0]), "tail_edges": len(edges[1])})

    def summary(self):
        return {"closed_sets_ever": len(self.closed_sets), "closed_sets": sorted(self.closed_sets),
                "final_closed": self.history[-1]["closed"],
                "final_largest_component": self.history[-1]["largest_head_component"],
                "final_mean_signed_turn_deg": self.history[-1]["mean_signed_turn_deg"],
                "history": self.history}

