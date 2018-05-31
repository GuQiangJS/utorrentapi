# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import unittest
import time
from src.utorrentapi import uTorrentApi


class test_magnet(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(test_magnet, self).__init__(*args, **kwargs)
        self._magnet = 'magnet:?xt=urn:btih:fb7f7d8a416a69baff5c28743385096fea50ce45&dn=Red+Sparrow+2018+720p+BrRip+x264+-+PLAYNOW&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Fzer0day.ch%3A1337&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969 target='
        self._hash = 'fb7f7d8a416a69baff5c28743385096fea50ce45'
        self._api=uTorrentApi('localhost', '12345', 'admin', '111111')

    def setUp(self):
        torrents = self._api.get_list()
        for t in torrents:
            self._api.remove_data(t.hash)

    def test_add_remove_magnet(self):
        code, rep = self._api.add_url(self._magnet)
        r = self._api.get_list()
        torrents = r['torrents']
        self.assertTrue(torrents)
        self.assertEqual(1,len(torrents))
        self.assertEqual(torrents[0][0],self._hash.upper())
        self._api.remove_data(self._hash)
        r = self._api.get_list()
        torrents = r['torrents']
        self.assertFalse(torrents)
        self.assertEqual(0,len(torrents))

    def test_set_status(self):
        self._api.add_url(self._magnet)
        t=self.__get_first_torrent__()
        time.sleep(1)
        print(t[21])
        self._api.pause(t[0])
        t=self.__get_first_torrent__()
        time.sleep(1)
        print(t[21])
        self._api.un_pause(t[0])
        t=self.__get_first_torrent__()
        time.sleep(1)
        print(t[21])
        # 状态正则
        # (.*?)(\d{1,3}\.\d{1,3}) %

class test_torrent(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        import requests

        super(test_torrent, self).__init__(*args, **kwargs)
        self._api=uTorrentApi('localhost', '12345', 'admin', '111111')
        self._torrent_url='http://rarbg.is/download.php?id=1zdq2ae&f=In.Darkness.2018.1080p.WEB-DL.DD5.1.H264-FGT-[rarbg.to].torrent'
        self._torrent_content=requests.get(self._torrent_url).content

    def setUp(self):
        torrents = self._api.get_list()
        for t in torrents:
            self._api.remove_data(t.hash)

    def test_add_and_get_files(self):
        self._api.add_file(self._torrent_content)
        time.sleep(1)
        torrents=self._api.get_list()
        self.assertIsNotNone(torrents)
        files=self._api.get_file_list(torrents[0].hash)
        self.assertEqual(3,len(files))
        self.assertEqual('English.srt',files[0].name)
        self.assertEqual('In.Darkness.2018.1080p.WEB-DL.DD5.1.H264-FGT.mkv',files[1].name)
        self.assertEqual('RARBG.txt',files[2].name)
        self.assertEqual(2,files[1].priority)
        self._api.set_priority(torrents[0].hash,0,0)
        time.sleep(1)
        files=self._api.get_file_list(torrents[0].hash)
        self.assertEqual(0,files[0].priority)

if __name__ == '__main__':
    unittest.main()
