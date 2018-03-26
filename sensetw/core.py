
import re


class Card(object):
    _fields = [
        "title", "quote", "source_url", "source_type", "tags", "comments",
        "hypothesis_id", "trello_id",
    ]

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            if field not in self._fields:
                raise TypeError(
                    '"{field}" is not an allowed field'.format(field=field))
            if not self._check_field(field, value):
                raise ValueError(
                    '"{field}" field has invalid value'.format(field=field))
        self.__dict__.update(kwargs)

    def __setattr__(self, name, value):
        if not self._check_field(name, value):
            raise ValueError(
                '"{field}" field has invalid value'.format(field=name))
        object.__setattr__(self, name, value)

    def _check_field(self, field, value):
        if field == "source_type":
            return value in ["外部意見", "政府與研究報告", "其它"]
        if field == "tags":
            return isinstance(value, list)
        if field == "comments":
            return isinstance(value, list)
        if field == "trello_id":
            return isinstance(value, str) and len(value) <= 32
        if field == "hypothesis_id":
            return isinstance(value, str) and len(value) <= 32
        return True


class Mapping(object):
    _fields = [
        "hypothesis_url", "hypothesis_title", "trello_url", "trello_title",
    ]

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            if field not in self._fields:
                raise TypeError(
                    '"{field}" is not an allowed field'.format(field=field))
        self.__dict__.update(kwargs)

    @property
    def hypothesis_group_id(self):
        group_re = re.compile("//sense.tw/groups/(.*?)/")
        r = group_re.search(self.hypothesis_url)
        return r.group(1)

    @property
    def trello_board_id(self):
        board_re = re.compile("//trello.com/b/(.*?)/")
        r = board_re.search(self.trello_url)
        return r.group(1)

    @property
    def id(self):
        return self.hypothesis_group_id + ":" + self.trello_board_id
