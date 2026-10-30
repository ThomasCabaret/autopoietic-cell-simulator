"""Small copied view of existing research observers, with their observation time."""


def live_observations(observer,observed_time=None):
    state=observer.__dict__;rows=[];measured=None
    genetic=state.get('genetic_state') if 'genetic_state' in state else state
    if genetic and 'detached' in genetic:
        measured=genetic['history'][-1]['time'] if genetic.get('history') else None
        rows.extend([('Nouveaux G libérés',len(genetic['detached'])),
                     ('Nouveaux F libérés',len(genetic['translated_detached']))])
        assembly=genetic.get('assembly_state')
        if assembly is not None:
            rows.append(('Composants construits',len(assembly['events'])))
            events=genetic.get('assembly_catalytic_events',[])
            cat={e['support'] for e in events if e['catalyzed']}
            expressed={e['support'] for e in events if e['chain_kind']=='expressed'}
            used=set(genetic['assembly_incorporated'])
            rows.extend([('Dont catalysés',len(cat)),('Dont par F exprimés',len(expressed)),
                         ('Catalysés puis réutilisés',len(cat&used))])
    membrane=state.get('membrane_state')
    if membrane is None and state.get('history') and 'parent_closed' in state['history'][-1]:membrane=state
    if membrane and membrane.get('history'):
        last=membrane['history'][-1]
        if measured is None:measured=last['time']
        status='non classable' if not last['envelope_valid'] else ('fermée' if last['parent_closed'] else 'ouverte')
        rows.append(('Frontière observée',status))
        rows.append(('L insérés (observés)',len(membrane.get('inserted',[]))))
        if membrane.get('nr',0):
            rows.append(('Sondes retenues dedans',last['retained_inside'] if last['envelope_valid'] else 'non classable'))
            rows.append(('Sorties de sondes observées',last['retained_escaped']))
        if membrane.get('np',0):rows.append(('Sondes perméables entrées',last['permeable_entered']))
    if 'closed_sets' in state:
        measured=state['history'][-1]['time'] if state.get('history') else None
        rows.append(('Contours fermés observés',len(state['closed_sets'])))
    return dict(time=measured if observed_time is None else observed_time,rows=rows,
        note='Mesures des observateurs existants ; structures initiales exclues des nouveaux G/F. Ce ne sont pas des contrôles de dynamique.')
