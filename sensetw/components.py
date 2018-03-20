
from sensetw import Card
import re
import requests


class Hypothesis:
    """
    A Hypothesis group with annotations on a topic.
    """

    def __init__(self, api_url, api_key, title, url):
        self.api_url = api_url
        self.api_key = api_key
        self.title = title
        self.url = url

    def annotations(self):
        return [1]

    @property
    def group_id(self):
        group_re = re.compile("//sense.tw/groups/(.*?)/")
        r = group_re.search(self.url)
        return r.group(1)

    @property
    def request_headers(self):
        return {
            "Authorization": "Bearer {api_key}".format(api_key=self.api_key)
        }

    def group_search_url(self):
        return self.api_url + "/search?group={group_id}".format(group_id=self.group_id)

    def rows_to_annotations(self, data_rows):
        return data_rows

    def annotations(self, agent=None):
        """
        Get annotations from the Hypothesis group.
        """
        if agent is None:
            agent = requests
        response = agent.get(self.group_search_url(),
                             headers=self.request_headers)
        data = response.json()
        return self.rows_to_annotations(data["rows"])

    def extract_quote(self, targets):
        if len(targets) == 0:
            return None

        def extract_exact(selectors):
            if len(selectors) == 0:
                return None
            if selectors[0]["type"] == "TextQuoteSelector":
                return selectors[0]["exact"]
            else:
                return extract_exact(selectors[1:])

        if "selector" not in targets[0]:
            return self.extract_quote(targets[1:])
        exact = extract_exact(targets[0]["selector"])
        if exact is not None:
            return exact
        else:
            return self.extract_quote(targets[1:])

    def extract_source_type(self, uri):
        external_keywords = [
            "facebook", "ithome.com.tw", "udn.com", "storm.mg", "cw.com.tw", "cna.com.tw",
            "teema.org.tw"]
        official_keywords = [
            "gov", "gov.tw", "itsa.gov.tw"]
        for k in external_keywords:
            if k in uri:
                return "外部意見"
        for k in official_keywords:
            if k in uri:
                return "政府與研究報告"
        return "其它"

    def annotation_to_card(self, ann):
        title = ann["document"]["title"][0] if "title" in ann["document"] else ""
        quote = self.extract_quote(ann["target"])
        source_url = ann["links"]["incontext"] if "incontext" in ann["links"] else ""
        source_type = self.extract_source_type(ann["uri"])
        tags = ann["tags"]
        hypothesis_id = ann["id"]

        card = Card(
            title=title, quote=quote, source_url=source_url, source_type=source_type,
            tags=tags, hypothesis_id=hypothesis_id)

        return card


class Trello:

    def __init__(self, api_url, api_key, token, title, url):
        self.api_url = api_url
        self.api_key = api_key
        self.token = token
        self.title = title
        self.url = url
        self._board_cache = {}

    def _request_board(self, objects, agent=None):
        if objects in self._board_cache:
            return self._board_cache[objects]
        if agent is None:
            agent = requests
        response = agent.get(
            self.api_url + "/boards/" + self.board_id + "/" + objects,
            params=self.request_params)
        self._board_cache[objects] = response.json()
        return self._board_cache[objects]

    def get_lists(self, agent=None):
        lists = self._request_board("lists")
        return {li["name"][8:]: li["id"] for li in lists
                if li["name"][:8] == "Inbox - "}

    def get_labels(self, agent=None):
        labels = self._request_board("labels")
        return {la["name"]: la["id"] for la in labels}

    def card_to_trello_card(self, card, labels=None, list_id=None):
        trello_name = "【{title}】{quote} {tags}".format(
            title=card.title,
            quote=card.quote,
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

    def post(self, card, labels=None, list_id=None, agent=None):
        if agent is None:
            agent = requests
        params = {}
        params.update(self.request_params)
        params.update(self.card_to_trello_card(card, labels=labels, list_id=list_id))
        response = agent.post(self.api_url + "/cards", params=params)
        return response.text

    @property
    def board_id(self):
        board_re = re.compile("//trello.com/b/(.*?)/")
        r = board_re.search(self.url)
        return r.group(1)

    @property
    def request_params(self):
        return {"key": self.api_key, "token": self.token}
