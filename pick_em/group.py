import requests
from .propositions import Propositions
from .entry import Entry

class Group:
    
    def __init__(self, year, challenge_id, group_id):
        self.year = year
        self.challenge_id = challenge_id
        self.group_id = group_id
        self.entries = []
        self._fetch_pick_em()
        self._fetch_group()
    
    def __repr__(self):
        return "Group(%s, %i)" % (self.name, self.year)
    
    def _fetch_pick_em(self):
        '''Fetches pick'em info for a given year'''
        # fetch json
        url = f'https://gambit-api.fantasy.espn.com/apis/v1/challenges/{self.challenge_id}'
        headers = {
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
                }
        params = (('platform', 'chui'),)
        response = requests.get(url, headers=headers, params=params)
        
        # if bad response, raise error
        response.raise_for_status()
        
        # get current scoring period
        data = response.json()
        # self.year = 
        self.week = data['currentScoringPeriod']['id']
    
    def _fetch_group(self):
        '''Fetches data for a specified pick;em group.'''
        # fetch json
        url = f"https://gambit-api.fantasy.espn.com/apis/v1/challenges/{self.challenge_id}/groups/{self.group_id}"
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            }
        params = (('platform', 'chui'),)
        response = requests.get(url, headers=headers, params=params)

        # if bad response, raise error
        response.raise_for_status()

        # parse relevant group data
        data = response.json()
        self.data = data # this is here for now to make it easy to explore json data
        self.name = data['groupSettings']['name']
        self.propositions = Propositions(self.challenge_id, self.year)
        self._fetch_entries(data, self.propositions)
    
    def _fetch_entries(self, data, props):
        '''Fetches entry data for each entry in group and creates list of Entry objects'''
        self.entries = []
        entries_data = data['entries']
        for entry in entries_data:
            self.entries.append(Entry(entry, self.propositions))
    
    def get_games(self):
        '''Returns all games for a given year'''
        return self.propositions.get_all_props()
    
    def get_week_games(self, week):
        '''Returns list of dicts of games for a given week'''
        return self.propositions.get_week_props(week)
    
    def get_current_games(self):
        '''Fetches games and game info for current scoring period (week)'''
        return self.propositions.get_week_props(self.week)