import requests
import datetime as dt

class Propositions:
    '''Instance for season propositions'''
    def __init__(self, challenge_id, year):
        self.challenge_id = challenge_id
        self.year = year
        self.teams_dict = {}
        self._fetch_propositions()
    
    def _fetch_propositions(self):
        '''Fetches and cleans/flattens propositions so that propositions are in a format
        that is easily converted to a dataframe'''

        # fetch proposition json
        url = "https://fantasy.espn.com/apis/v1/propositions?challengeId=" + str(self.challenge_id)
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            }
        params = (('platform', 'chui'),)
        response = requests.get(url, headers=headers, params=params)

        # raise error if bad response
        response.raise_for_status()
        
        self.data = props = response.json()
        
        # iterate through props and create props dict and team ids dict
        d = {}
        for prop in props:
            # teams dict
            self.teams_dict[prop['possibleOutcomes'][0]['id']] = prop['possibleOutcomes'][0]['name']
            self.teams_dict[prop['possibleOutcomes'][1]['id']] = prop['possibleOutcomes'][1]['name']
            
            d[prop['id']] = {
                'prop_id': prop['id'],
                'year': self.year,
                'date': dt.datetime.fromtimestamp(prop['date']/1000),
                'week': prop['scoringPeriodId'],
                'team1': prop['possibleOutcomes'][0]['name'],
                'team2': prop['possibleOutcomes'][1]['name'],
                'spread': prop.get('spread'),
                'team1_pick_pct': self.get_pick_pct(prop['possibleOutcomes'][0]['choiceCounters']),
                'team2_pick_pct': self.get_pick_pct(prop['possibleOutcomes'][1]['choiceCounters']),
                'score1': prop['possibleOutcomes'][0].get('score'),
                'score2': prop['possibleOutcomes'][1].get('score'),
                'winner': self.teams_dict[prop['correctOutcomes'][0]] if prop['correctOutcomes'] else None,
                'spread_winner': self.teams_dict[prop['correctOutcomeOverrides']['SPREAD']] if 'correctOutcomeOverrides' in prop else None
            }
        
        self.props = d

    def get_all_props(self):
        '''Returns a python list of all props sorted by the date the game is played'''
        return sorted(self.props.values(), key=lambda k: k['date'])
    
    def get_week_props(self, week):
        '''Returns python list of propositions for a given week'''
        l = []
        for prop in self.props.values():
            if prop['week'] == week:
                l.append(prop)
        return sorted(l, key=lambda k: k['date'])

    def get_prop_by_id(self, id):
        '''Returns prop dict for specified id'''
        return self.props[id]
    
    def get_team_name_by_id(self, id):
        return self.teams_dict[id]
    
    def get_pick_pct(self, data):
        for i in data:
            if i['scoringFormatId'] == 3:
                return i['percentage']
        return None

