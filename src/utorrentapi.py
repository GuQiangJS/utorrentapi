# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import requests.auth
from lxml import html


class uTorrentApi():

    # HTTP://[IP]:[PORT]/GUI/?ACTION=START&HASH=[TORRENT HASH]

    def __init__(self, ip: str, port: str, username: str, pwd: str):
        """
        初始化
        :param ip: uTorrent WebUI IP地址
        :param port: uTorrent WebUI 端口
        :param username: uTorrent WebUI 用户名
        :param pwd: uTorrent WebUI 密码
        """
        self._ip = ip
        self._port = port
        self._username = username
        self._pwd = pwd
        self._auth = (self._username, self._pwd)
        self._token, self._cookies = self.__get_token__()

    def __get_base_url__(self, ip: str, port: str):
        return 'http://{0}:{1}/gui/'.format(self._ip, self._port)

    def __get_token__(self):
        url = self.__get_base_url__(self._ip, self._port) + 'token.html'

        token = -1
        cookies = -1

        try:
            response = requests.get(url, auth=self._auth)

            token = -1

            if response.status_code == 200:
                xtree = html.fromstring(response.content)
                token = xtree.xpath('//*[@id="token"]/text()')[0]
                guid = response.cookies['GUID']
            else:
                token = -1

            cookies = dict(GUID=guid)

        except requests.ConnectionError as error:
            token = 0
            cookies = 0
            print(error)
        except:
            print('error')

        return token, cookies

    # def __do_action__(self,d:dict):
    #     """
    #     执行具体命令
    #     :param d: 包含所有参数的字典，参数见 http://help.utorrent.com/customer/en/portal/articles/1573952-actions---webapi
    #     从ACTION开始的所有参数
    #     :return: [response.status_code,response]
    #     """
    #

    def __do_action_core__(self, path):
        """
        执行具体命令
        :param path:
        :return: [response.status_code,response]
        """
        # p = ''
        # if d:
        #     p = '&'.join(['{0}={1}'.format(k, v) for k, v in d.items() if k not in ['action', 'token']])
        #
        # url = '{url}?action={action}&token={token}&{params}'.format(url=self.__get_base_url__(self._ip, self._port),
        #                                                             params=p, action=d['action'], token=self._token)
        headers = {'Content-Type': "application/json"}
        rep = requests.get('{url}?{path}'.format(url=self.__get_base_url__(self._ip, self._port), path=path),
                           auth=self._auth, cookies=self._cookies, headers=headers)
        return rep.status_code, rep

    def __action__(self, action: str, hash: str):
        return self.__do_action_core__({"action": action, "hash": hash})

    def start(self, hash: str):
        """
        启动指定的torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=START&HASH=[TORRENT HASH]
        This action tells BitTorrent to start the specified torrent job(s). Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__do_action_core__('action=start&token={token}&hash={hash}'.format(token=self._token, hash=hash))

    def stop(self, hash: str):
        """
        停止指定的torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=STOP&HASH=[TORRENT HASH]
        This action tells BitTorrent to stop the specified torrent job(s). Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__do_action_core__('action=stop&token={token}&hash={hash}'.format(token=self._token, hash=hash))

    def pause(self, hash: str):
        """
        暂停指定的torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=PAUSE&HASH=[TORRENT HASH]
        This action tells BitTorrent to pause the specified torrent job(s). Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__do_action_core__('action=pause&token={token}&hash={hash}'.format(token=self._token, hash=hash))

    def force_start(self, hash: str):
        """
        强制启动指定的torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=FORCESTART&HASH=[TORRENT HASH]
        This action tells BitTorrent to force the specified torrent job(s) to start. Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__do_action_core__(
            'action=forcestart&token={token}&hash={hash}'.format(token=self._token, hash=hash))

    def un_pause(self, hash: str):
        """
        取消暂停指定的torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=UNPAUSE&HASH=[TORRENT HASH]
        This action tells BitTorrent to unpause the specified torrent job(s). Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__do_action_core__('action=unpause&token={token}&hash={hash}'.format(token=self._token, hash=hash))

    def re_check(self, hash: str):
        """
        重新检查指定的torrent作业的torrent内容
        HTTP://[IP]:[PORT]/GUI/?ACTION=RECHECK&HASH=[TORRENT HASH]
        This action tells BitTorrent to recheck the torrent contents for the specified torrent job(s). Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__do_action_core__('action=recheck&token={token}&hash={hash}'.format(token=self._token, hash=hash))

    def remove(self, hash: str):
        """
        从列表中删除指定的torrent作业
        该行动尊重“如果可能的话转移到垃圾箱”选项
        HTTP://[IP]:[PORT]/GUI/?ACTION=REMOVE&HASH=[TORRENT HASH]
        This action removes the specified torrent job(s) from the torrent jobs list. Multiple hashes may be specified to act on multiple torrent jobs. This action respects the option "Move to trash if possible".
        :param hash:
        :return:
        """
        return self.__do_action_core__('action=remove&token={token}&hash={hash}'.format(token=self._token, hash=hash))

    def remove_data(self, hash: str):
        """
        从列表中删除指定的torrent作业，并从磁盘中删除相应的torrent内容（数据）
        该行动尊重“如果可能的话转移到垃圾箱”选项
        HTTP://[IP]:[PORT]/GUI/?ACTION=REMOVEDATA&HASH=[TORRENT HASH]
        This action removes the specified torrent job(s) from the torrent jobs list and removes the corresponding torrent contents (data) from disk. Multiple hashes may be specified to act on multiple torrent jobs. This action respects the option "Move to trash if possible".
        :param hash:
        :return:
        """
        return self.__do_action_core__(
            'action=removedata&token={token}&hash={hash}'.format(token=self._token, hash=hash))

    # def set_prio(self, hash: str, priority, file_index):
    #     """
    #     此操作为torrent作业中的指定文件设置优先级。
    #     可能的优先级是由“getfiles”返回的值。
    #     每次调用此操作时只能指定一个优先级，但可指定多个文件。
    #     # 0 = Don't Download
    #     # 1 = Low Priority
    #     # 2 = Normal Priority
    #     # 3 = High Priority
    #     HTTP://[IP]:[PORT]/GUI/?ACTION=SETPRIO&HASH=[TORRENT HASH]&P=[PRIORITY]&F=[FILE INDEX]
    #     This action sets the priority for the specified file(s) in the torrent job. The possible priority levels are the values returned by "getfiles". A file is specified using the zero-based index of the file in the inside the list returned by "getfiles". Only one priority level may be specified on each call to this action, but multiple files may be specified.
    #     :param hash:
    #     :return:
    #     """
    #     return self.__do_action_core__({"action": "SETPRIO", "HASH": hash, "P": priority, "F": file_index})

    def add_url(self, url: str):
        """
        从给定的网址添加一个torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=ADD-URL&S=[TORRENT URL]
        This action adds a torrent job from the given URL. For servers that require cookies, cookies can be sent with the :COOKIE: method (see here). The string must be URL-encoded.
        :param hash:
        :return:
        """
        return self.__do_action_core__('action=add-url&token={token}&s={str}'.format(token=self._token, str=url))

    def add_file(self, s):
        """
        从给定的网址添加一个torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=ADD-FILE
        This action is different from the other actions in that it uses HTTP POST instead of HTTP GET to submit data to BitTorrent. The HTTP form must use an enctype of "multipart/form-data" and have an input field of type "file" with name "torrent_file" that stores the local path to the file to upload to BitTorrent.
        :param file: 种子文件内容流
        :return:
        """
        result = []

        url = 'list=1&token=' + self._token
        headers = {
            'Content-Type': "multipart/form-data"
        }

        files = {'torrent_file': s}

        try:
            if files:
                response = requests.post(
                    '{url}?action=add-file&token={token}'.format(url=self.__get_base_url__(self._ip, self._port),
                                                                 token=self._token), files=files, auth=self._auth,
                    cookies=self._cookies)
                if response.status_code == 200:
                    result = response.json()
                    print('file added')
                else:
                    print(response.status_code)
            else:
                print('file not found')

            pass
        except requests.ConnectionError as error:
            print(error)
        except Exception as e:
            print(e)

        return result

    def get_list(self):
        """
        获取当前所有的任务集合。
        :return: torrent 实例集合
        """
        torrents = []
        try:
            status, response = self.__do_action_core__('list=1&token=' + self._token)
            if status == 200:
                torrents = response.json()
            else:
                print(response.status_code)

        except requests.ConnectionError as error:
            print(error)
        except:
            print('error')

        return [torrent(t) for t in torrents['torrents']] if torrents and torrents['torrents'] else []

    def get_file_list(self, hash: str):
        """
        获取指定任务的文件列表
        :param hash:
        :return: 正常获取时返回 torrent_file 集合。否则返回 None
        """
        prop = None
        if not hash:
            return None
        status, prop = self.__do_action_core__(
            'action=getfiles&token={token}&hash={hash}'.format(token=self._token, hash=hash))
        if status == 200:
            res = prop.json()
            if res and res['files']:
                return [torrent_file(f) for f in res['files'][1]]
        else:
            return None
        return None

    def set_priority(self, hash: str, fileindex, priority):
        """
        此操作为torrent作业中的指定文件设置优先级。
        可能的优先级是由“getfiles”返回的值。
        每次调用此操作时只能指定一个优先级。
        :param hash:
        :param fileindex:
        :param priority:
        # 0 = Don't Download
        # 1 = Low Priority
        # 2 = Normal Priority
        # 3 = High Priority
        :return:
        """
        status, response = self.__do_action_core__(
            'action=setprio&token={token}&hash={hash}&p={priority}&f={index}'.format(token=self._token, hash=hash, index=fileindex,
                                                                                     priority=priority))

        files = []

        if status == 200:
            files = response.json()
        else:
            print(response.status_code)

        return files


class torrent_file():
    """
    种子中的文件
    """

    def __init__(self, t):
        if not t:
            raise ValueError
        self._name = t[0]
        self._size = t[1]
        self._downloaded = t[2]
        self._priority = t[3]

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size

    @property
    def download(self):
        return self._downloaded

    @property
    def priority(self):
        """
        优先级
        0 = Don't Download
        1 = Low Priority
        2 = Normal Priority
        3 = High Priority
        :return:
        """
        return self._priority


class torrent():
    """
    种子类型
    根据 uTorrentApi.get_list 中返回的集合中的元素创建实例。
    """

    def __init__(self, t: []):
        if not t or len(t) != 29:
            raise ValueError
        self._name = t[2]
        self._hash = t[0]
        self._status_str = t[21]
        self._path = t[26]
        self._data = t

    @property
    def data(self):
        """
        原始数据。uTorrentApi.get_list 中返回的集合中的元素
        :return:
        """
        return self._data

    @property
    def name(self):
        return self._name

    @property
    def hash(self):
        return self._hash

    @property
    def status_str(self):
        """
        状态字符串
        :return:
        """
        return self._status_str

    @property
    def path(self):
        """
        保存路径
        example: 'Queued 0.0 %'
        :return:
        """
        return self._path
