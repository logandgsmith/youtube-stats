#!/usr/bin/env python3

import requests
import json
import config

class Member:
    """Represents a member and her page, subs, etc"""
    def __init__(self, name, chan_id):
        self.name = name
        self.chan_id = chan_id
        self.subs = self.scrape_subs()
        self.rank = 0

    def __eq__(self, other):
        return self.subs == other.subs

    def __lt__(self, other):
        return self.subs < other.subs

    def __gt__(self, other):
        return self.subs < other.subs

    def scrape_subs(self) -> int:
        """Scrapes the subs from YouTube APU"""
        res = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics'
                           + '&id=' + self.chan_id + '&key=' + config.api_key)
        if res.status_code != 200:
            return -1
        else:
            return int(res.json()['items'][0]['statistics']['subscriberCount'])

def main():
    holo_myth = [
        Member('Amelia Watson', 'UCyl1z3jo3XHR1riLFKG5UAg'),
        Member('Calliope Mori', 'UCL_qhgtOy0dy1Agp8vkySQg'),
        Member('Gura Gawr', 'UCoSrY_IQQVpmIRZ9Xf-y93g'),
        Member('Ina\'nis Ninomae', 'UCMwGHR0BTZuLsmjY_NT5Pwg'),
        Member('Kiara Takanashi', 'UCHsx4Hqa-1ORjQTh9TYDhww')
    ]

    holo_myth.sort(reverse=True)

    print('Current Sub Count Rankings for Hololive Myth')
    for member in holo_myth:
        print(f'{member.name} with {member.subs} subs')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
