# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import requests.auth

class uTorrentApi():

    # HTTP://[IP]:[PORT]/GUI/?ACTION=START&HASH=[TORRENT HASH]

    def __init__(self,ip:str,port:str,username:str,pwd:str):
        self._ip=ip
        self._port=port
        self._username=username
        self._pwd=pwd
        self._auth=requests.auth.HTTPBasicAuth(self._username,self._pwd)

    # def __do_action__(self,d:dict):
    #     """
    #     执行具体命令
    #     :param d: 包含所有参数的字典，参数见 http://help.utorrent.com/customer/en/portal/articles/1573952-actions---webapi
    #     从ACTION开始的所有参数
    #     :return: [response.status_code,response]
    #     """
    #


    def __do_action_core__(self,d:dict):
        """
        执行具体命令
        :param d: 包含所有参数的字典，参数见 http://help.utorrent.com/customer/en/portal/articles/1573952-actions---webapi
        从ACTION开始的所有参数
        :return: [response.status_code,response]
        """
        p=''
        if d:
            p='&'.join(['{0}={1}'.format(k,v) for k,v in d.items()])

        url='HTTP://{0}:{1}/GUI/?{2}'.format(self._ip,self._port,p)
        headers = {'Content-Type': "application/json"}
        rep=requests.get(url,auth=self._auth,cookies=self._cookies,headers=headers)
        return rep.status_code,rep

    def __action__(self,action:str,hash:str):
        return self.__do_action_core__({"ACTION":action,"HASH":hash})

    def start(self,hash:str):
        """
        启动指定的torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=START&HASH=[TORRENT HASH]
        This action tells BitTorrent to start the specified torrent job(s). Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__action__("START",hash)

    def stop(self,hash:str):
        """
        停止指定的torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=STOP&HASH=[TORRENT HASH]
        This action tells BitTorrent to stop the specified torrent job(s). Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__action__("STOP",hash)

    def pause(self,hash:str):
        """
        暂停指定的torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=PAUSE&HASH=[TORRENT HASH]
        This action tells BitTorrent to pause the specified torrent job(s). Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__action__("PAUSE",hash)

    def force_start(self,hash:str):
        """
        强制启动指定的torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=FORCESTART&HASH=[TORRENT HASH]
        This action tells BitTorrent to force the specified torrent job(s) to start. Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__action__("FORCESTART",hash)

    def un_pause(self,hash:str):
        """
        取消暂停指定的torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=UNPAUSE&HASH=[TORRENT HASH]
        This action tells BitTorrent to unpause the specified torrent job(s). Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__action__("UNPAUSE",hash)

    def re_check(self,hash:str):
        """
        重新检查指定的torrent作业的torrent内容
        HTTP://[IP]:[PORT]/GUI/?ACTION=RECHECK&HASH=[TORRENT HASH]
        This action tells BitTorrent to recheck the torrent contents for the specified torrent job(s). Multiple hashes may be specified to act on multiple torrent jobs.
        :param hash:
        :return:
        """
        return self.__action__("RECHECK",hash)

    def remove(self,hash:str):
        """
        从列表中删除指定的torrent作业
        该行动尊重“如果可能的话转移到垃圾箱”选项
        HTTP://[IP]:[PORT]/GUI/?ACTION=REMOVE&HASH=[TORRENT HASH]
        This action removes the specified torrent job(s) from the torrent jobs list. Multiple hashes may be specified to act on multiple torrent jobs. This action respects the option "Move to trash if possible".
        :param hash:
        :return:
        """
        return self.__action__("REMOVE",hash)

    def remove_data(self,hash:str):
        """
        从列表中删除指定的torrent作业，并从磁盘中删除相应的torrent内容（数据）
        该行动尊重“如果可能的话转移到垃圾箱”选项
        HTTP://[IP]:[PORT]/GUI/?ACTION=REMOVEDATA&HASH=[TORRENT HASH]
        This action removes the specified torrent job(s) from the torrent jobs list and removes the corresponding torrent contents (data) from disk. Multiple hashes may be specified to act on multiple torrent jobs. This action respects the option "Move to trash if possible".
        :param hash:
        :return:
        """
        return self.__action__("REMOVEDATA",hash)

    def set_prio(self,hash:str,priority,file_index):
        """
        此操作为torrent作业中的指定文件设置优先级。
        可能的优先级是由“getfiles”返回的值。
        每次调用此操作时只能指定一个优先级，但可指定多个文件。
        # 0 = Don't Download
        # 1 = Low Priority
        # 2 = Normal Priority
        # 3 = High Priority
        HTTP://[IP]:[PORT]/GUI/?ACTION=SETPRIO&HASH=[TORRENT HASH]&P=[PRIORITY]&F=[FILE INDEX]
        This action sets the priority for the specified file(s) in the torrent job. The possible priority levels are the values returned by "getfiles". A file is specified using the zero-based index of the file in the inside the list returned by "getfiles". Only one priority level may be specified on each call to this action, but multiple files may be specified.
        :param hash:
        :return:
        """
        return self.__do_action_core__({"ACTION":"SETPRIO","HASH":hash,"P":priority,"F":file_index})

    def add_url(self,url:str):
        """
        从给定的网址添加一个torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=ADD-URL&S=[TORRENT URL]
        This action adds a torrent job from the given URL. For servers that require cookies, cookies can be sent with the :COOKIE: method (see here). The string must be URL-encoded.
        :param hash:
        :return:
        """
        return self.__do_action_core__({"ACTION":"ADD-URL","s":url})

    def add_file(self):
        """
        从给定的网址添加一个torrent作业。
        HTTP://[IP]:[PORT]/GUI/?ACTION=ADD-FILE
        This action is different from the other actions in that it uses HTTP POST instead of HTTP GET to submit data to BitTorrent. The HTTP form must use an enctype of "multipart/form-data" and have an input field of type "file" with name "torrent_file" that stores the local path to the file to upload to BitTorrent.
        :param hash:
        :return:
        """
        raise NotImplementedError
        # return self.__do_action_core__({"ACTION":"ADD-FILE",})


class Action():
    @property
    def START(self):
        return 'START'
    @property
    def STOP(self):
        return 'STOP'
    @property
    def PAUSE(self):
        return 'PAUSE'
    @property
    def FORCESTART(self):
        return 'FORCESTART'
    @property
    def UNPAUSE(self):
        return 'UNPAUSE'
    @property
    def RECHECK(self):
        return 'RECHECK'
    @property
    def REMOVE(self):
        return 'REMOVE'
    @property
    def REMOVEDATA(self):
        return 'REMOVEDATA'
    @property
    def SETPRIO(self):
        return 'SETPRIO'
    @property
    def ADD_URL(self):
        return 'ADD-URL'
    @property
    def ADD_FILE(self):
        return 'ADD-FILE'