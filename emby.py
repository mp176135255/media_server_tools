from network import network
import json


class emby:
    host = None
    userid = None
    key = None
    headers = None
    err = None
    client = None


    def __init__(self, host : str, userid : str, key : str) -> None:
        """
        :param host
        :param userid
        :param key
        """
        self.host = host
        self.userid = userid
        self.key = key
        self.headers = {'Content-Type':'application/json'}
        self.client = network(maxnumconnect=10, maxnumcache=20)
    

    def get_items(self, parentid : str = ''):
        """
        获取项目列表
        :param parentid 父文件夹ID
        :return True or False, items
        """
        items = {}
        try:
            if len(parentid):
                url = '{}/emby/Users/{}/Items?ParentId={}&api_key={}'.format(self.host, self.userid, parentid, self.key)
            else:
                url = '{}/emby/Users/{}/Items?api_key={}'.format(self.host, self.userid, self.key)
            p, err = self.client.get(url)
            if p == None:
                self.err = err
                return False, items
            if p.status_code != 200:
                self.err = p.text
                return False, items
            items = json.loads(p.text)
            return True, items
        except Exception as result:
            self.err = "异常错误：{}".format(result)
            return False, items

    def get_items_count(self):
        """
        获取项目数量
        :return True or False, iteminfo
        """
        iteminfo = {}
        try:
            url = '{}/emby/Items/Counts?api_key={}'.format(self.host, self.key)
            p, err = self.client.get(url)
            if p == None:
                self.err = err
                return False, iteminfo
            if p.status_code != 200:
                self.err = p.text
                return False, iteminfo
            iteminfo = json.loads(p.text)
            return True, iteminfo
        except Exception as result:
            self.err = "异常错误：{}".format(result)
            return False, iteminfo

    def get_item_info(self, itemid : str):
        """
        获取项目
        :param itemid 项目ID
        :return True or False, iteminfo
        """
        iteminfo = {}
        try:
            url = '{}/emby/Users/{}/Items/{}?Fields=ChannelMappingInfo&api_key={}'.format(self.host, self.userid, itemid, self.key)
            p, err = self.client.get(url)
            if p == None:
                self.err = err
                return False, iteminfo
            if p.status_code != 200:
                self.err = p.text
                return False, iteminfo
            iteminfo = json.loads(p.text)
            return True, iteminfo
        except Exception as result:
            self.err = "异常错误：{}".format(result)
            return False, iteminfo

    def set_item_info(self, itemid : str, iteminfo):
        """
        更新项目
        :param iteminfo 项目信息
        :return True or False, iteminfo
        """
        try:
            url = '{}/emby/Items/{}?api_key={}'.format(self.host, itemid, self.key)
            data = json.dumps(iteminfo)
            p, err = self.client.post(url=url, headers=self.headers, data=data)
            if p == None:
                self.err = err
                return False, iteminfo
            if p.status_code != 200 and p.status_code != 204:
                self.err = p.text
                return False
            return True
        except Exception as result:
            self.err = "异常错误：{}".format(result)
            return False

    def set_item_image(self, itemid : str, imageurl : str):
        """
        更新项目图片
        :param imageurl 图片URL
        :return True or False
        """
        try:
            url = '{}/emby/Items/{}/Images/Primary/0/Url?api_key={}'.format(self.host, itemid, self.key)
            data = json.dumps({'Url': imageurl})
            p, err = self.client.post(url=url, headers=self.headers, data=data)
            if p == None:
                self.err = err
                return False
            if p.status_code != 200 and p.status_code != 204:
                self.err = p.text
                return False
            return True
        except Exception as result:
            self.err = "异常错误：{}".format(result)
            return False