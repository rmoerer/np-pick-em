class Entry:
    
    def __init__(self, data, props):
        self.data = data
        self.props = props
        self.id = data['id']
        self.name = data['name']
        self.member = data['member']['displayName']
        self.member_id = data['member']['id']
        self.overall_score = data['score']['overallScore']
        self.percentile = data['score']['percentile']
        self.rank = data['score']['rank']
        self.wins = data['score']['record']['wins']
        self.losses = data['score']['record']['losses']
        self.score_by_week = {}
        self.picks = []

        self._fetch_score_by_week(data)
        self._fetch_picks(props, data)

    def __repr__(self):
        return 'Entry(%s, %s)' % (self.name, self.member)
    
    def _fetch_score_by_week(self, data):
        score_by_week = data['score']['scoreByPeriod']

        for key, value in score_by_week.items():
            self.score_by_week[key] = value['score']
    
    def _fetch_picks(self, props, data):
        if "picks" in data:
            picks = data['picks']
            self.picks = []
            for pick in picks:
                proposition = props.get_prop_by_id(pick['propositionId'])
                d = {'entry_id': self.id, 'entry_name': self.name, 'member': self.member, 'member_id': self.member_id}
                d.update(proposition)
                d['pick'] = props.get_team_name_by_id(pick['outcomesPicked'][0]['outcomeId'])
                d['result'] = pick['outcomesPicked'][0]['result']
                self.picks.append(d)
        else:
            self.picks = []
    
    def all_picks(self):
        '''Returns a list of dicts of all picks, sorted by date'''
        return sorted(self.picks, key=lambda k: k['date'])
    
    def picks_by_week(self, week):
        '''Returns a list of dicts for a specific week, sorted by date'''
        l = []
        for pick in self.picks:
            if pick['week'] == week:
                l.append(pick)

        return sorted(l, key=lambda k: k['date'])
