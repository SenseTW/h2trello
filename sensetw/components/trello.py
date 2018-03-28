
import re
import requests
from sensetw.core import Card

trello_name_quote_limit = 128


class Trello:

    def __init__(self, api_url, api_key, token, title, url):
        """
        A Trello board with lists, labels, and cards.

        * `api_url` - Trello API endpoint.  For example <https://api.trello.com/1>.
        * `url` -  Board URL.  For example <https://trello.com/b/3pXCXxlW/>.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.token = token
        self.title = title
        self.url = url
        self._board_cache = {}

    def _objects_api(self, objects):
        return self.api_url + "/boards/" + self.board_id + "/" + objects

    def _request_board(self, objects, agent=None):
        if objects in self._board_cache:
            return self._board_cache[objects]
        if agent is None:
            agent = requests
        response = agent.get(self._objects_api(objects),
                             params=self.request_params)
        self._board_cache[objects] = response.json()
        return self._board_cache[objects]

    def get_lists(self, agent=None):
        lists = self._request_board("lists")
        return {li["name"][8:]: li["id"] for li in lists
                if li["name"][:8] == "Inbox - "}

    def create_lists(self, agent=None):
        if agent is None:
            agent = requests
        existing = self.get_lists(agent)
        count = 0
        for li in Card.source_types:
            if li not in existing:
                params = {}
                params.update(self.request_params)
                params.update({
                    "id": self.board_id,
                    "name": "Inbox - {li}".format(li=li),
                    "pos": "bottom",
                })
                response = agent.post(self._objects_api("lists"),
                                      params=params)
                count = count + 1
        if count > 0:
            self._board_cache.pop("lists")
        return count

    def create_labels(self, agent=None):
        if agent is None:
            agent = requests
        existing = self.get_labels(agent)
        count = 0
        for la in Card.source_types:
            if la not in existing:
                params = {}
                params.update(self.request_params)
                params.update({
                    "id": self.board_id,
                    "name": la,
                    "color": Card.source_type_colors[la],
                })
                response = agent.post(self._objects_api("labels"),
                                      params=params)
                count = count + 1
        if count > 0:
            self._board_cache.pop("labels")
        return count

    def get_labels(self, agent=None):
        labels = self._request_board("labels")
        return {la["name"]: la["id"] for la in labels}

    def card_to_trello_card(self, card, labels=None, list_id=None):
        quote = card.quote if card.quote is not None else ""
        if len(quote) > trello_name_quote_limit:
            quote = quote[:trello_name_quote_limit] + "⋯⋯"
        trello_name = "【{title}】{quote} {tags}".format(
            title=card.title,
            quote=quote,
            tags=" ".join(["#" + tag for tag in card.tags])
        )
        trello_desc = "\n".join(
            ["> " + line for line in card.quote.split("\n")]) \
            if card.quote is not None else ""
        trello_card = {
            "name": trello_name,
            "desc": trello_desc,
            "urlSource": card.source_url,
        }
        if labels is not None:
            trello_card["idLabels"] = ",".join(labels)
        if list_id is not None:
            trello_card["idList"] = list_id
        return trello_card

    def comment_params(self, card):
        params = {}
        params.update(self.request_params)
        params.update({"id": card.trello_id})
        tasks = [{**params, **{"text": text}} for text in card.comments]
        return tasks

    def post(self, card, labels=None, list_id=None, agent=None):
        if agent is None:
            agent = requests
        params = {}
        params.update(self.request_params)
        params.update(self.card_to_trello_card(
            card, labels=labels, list_id=list_id))
        response = agent.post(self.api_url + "/cards", params=params)
        result = response.json()
        card.trello_id = result["id"]
        comment_params = self.comment_params(card)
        for task in comment_params:
            url = self.api_url + "/cards/" + card.trello_id + "/actions/comments"
            response = agent.post(url, params=task)
        return card.trello_id

    @property
    def board_id(self):
        board_re = re.compile("//trello.com/b/(.*?)/")
        r = board_re.search(self.url)
        return r.group(1)

    @property
    def request_params(self):
        return {"key": self.api_key, "token": self.token}
