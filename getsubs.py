#!/usr/bin/env python3

__version__ = 'youtube-stats v0.2.0'

import argparse
import config
import csv
import requests

from datetime import datetime
from pytz import timezone

class Group:
    """Represent a group for comparison"""
    def __init__(self, name, members=None):
        self.name = name

        if members is None:
            self.members = []
        else:
            self.members = members

class Member:
    """Represents a member of a group's page, subs, etc"""
    def __init__(self, chan_id):
        self.res = requests.get(
                'https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics'
                           + '&id=' + chan_id + '&key=' + config.api_key
        )

        if self.res.status_code != 200:
            return

        self.name = self.res.json()['items'][0]['snippet']['title']
        self.chan_id = chan_id
        self.subs = int(self.res.json()['items'][0]['statistics']['subscriberCount'])
        self.rank = 0

    def __eq__(self, other):
        return self.subs == other.subs

    def __lt__(self, other):
        return self.subs < other.subs

    def __gt__(self, other):
        return self.subs < other.subs
    
def show_rankings(group):
    """Sorts the group and prints their ranking"""
    group.members.sort(reverse=True)

    print(f'Current Sub Count Rankings for {group.name}:')

    for member in group.members:
        if member.subs < 1000000:
            print(f'{member.name} with {member.subs // 1000}K subs')
        else:
            print(f'{member.name} with {member.subs / 1000000:.2f}M subs')

def main():
    tz = timezone('US/Eastern')

    # Parse Arguments
    parser = argparse.ArgumentParser(description='Record and analyze information about groups of YouTubers')
    parser.add_help = True
    parser.add_argument('path', nargs='?', default='./', help='Path to output .csv')
    parser.add_argument('-r', '--rankings', action='store_true', help='Display rankings on screen')
    parser.add_argument('-n', '--no-logging', action='store_true', help='Don\'t log to file')
    parser.add_argument('--version', action='version', version=__version__)
    flags = parser.parse_args()

    holo_myth_members = []
    with open('example_channels.txt') as channel_list:
        channels = channel_list.readlines()
        for chan_id in channels:
           holo_myth_members.append(Member(chan_id))

    # Create a group from the HoloEN Members
    holo_myth = Group('HoloLive Myth', holo_myth_members)

    # Display ranks in order if needed
    if flags.rankings:
        show_rankings(holo_myth)

    # Write to a .csv file
    if not flags.no_logging:
       with open(flags.path + 'holo-en-stats.csv', 'a', newline='') as log_file:
           writer = csv.writer(log_file)
           date = [datetime.now(tz)]
           writer.writerow(date + [member.subs for member in holo_myth.members])

if __name__ == '__main__':
    main()
