import re
import logging

class ClubStorage():

    club = set()
    TEAM_PATTERN = '[A-zА-я -]+'

    def add_team(self, name):
        if re.match(self.TEAM_PATTERN, name):
            self.club.add(name)
            return '{} have been added'.format(name)
        else:
            return '{} has not correct format'.format(name)   


    def get_teams(self):
        if len(self.club) == 0:
            return 'list is empty'
        else:
            return '\n'.join(self.club)


    def delete_team(self, name):
        try:
            self.club.pop(name)
            return '{} have been removed'.format(name)
        except KeyError:
            return '{} is not exist'.format(name)


    def delete_all_teams(self):
        self.club.clear()