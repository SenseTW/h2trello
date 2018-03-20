
import pytest
from sensetw.components import Hypothesis, Trello


@pytest.fixture
def h():
    return Hypothesis(
        api_url="https://sense.tw/api",
        api_key="12345",
        title="",
        url="https://sense.tw/groups/8VnXgMY2/tai-wan-xin-chuang-gong-si")


@pytest.fixture
def t():
    return Trello(
        api_url="https://api.trello.com/1",
        api_key="foobarbaz",
        token="helloworld",
        title="",
        url="https://trello.com/b/Lo01hfDB/ai-foobarbaz")


def test_hypothesis_group_id(h):
    assert h.group_id == "8VnXgMY2"


def test_hypothesis_search_group_url(h):
    assert h.group_search_url() == "https://sense.tw/api/search?group=8VnXgMY2"


def test_hypothesis_annotation_to_card(h):
    c = h.annotation_to_card({"updated": "2018-03-20T05:14:37.723143+00:00", "group": "8VnXgMY2", "target": [{"source": "https://udn.com/news/story/7238/2937685", "selector": [{"conformsTo": "https://tools.ietf.org/html/rfc3236", "type": "FragmentSelector", "value": "story_body_content"}, {"endContainer": "/div[3]/div[11]/div[1]/div[2]/div[1]/div[1]/p[2]", "startContainer": "/div[3]/div[11]/div[1]/div[2]/div[1]/div[1]/p[2]", "type": "RangeSelector", "startOffset": 0, "endOffset": 105}, {"type": "TextPositionSelector", "end": 8075, "start": 7970}, {"exact": "行政院科技會報執行秘書蔡志宏今（18）日表示，今年推動AI（人工智慧）的預算在90億元以上，預算來自科技預算以及前瞻基礎建設的數位建設；之後三年也保證預算在90億至100億元左右，相當於四年至少投入360億元。", "prefix": "acity:0,transition:\"none\"}); }  ", "type": "TextQuoteSelector", "suffix": "行政院科技會報今天在行政院會中報告台灣AI行動計畫，計畫期間從2"}]}], "links": {
                             "json": "https://sense.tw//api/annotations/ljSw7iv9Eeilw3M5xviqxw", "html": "https://sense.tw//a/ljSw7iv9Eeilw3M5xviqxw", "incontext": "https://O.sense.tw/ljSw7iv9Eeilw3M5xviqxw"}, "tags": [], "text": "", "created": "2018-03-20T05:14:37.723143+00:00", "uri": "https://udn.com/news/story/7238/2937685", "flagged": False, "user_info": {"display_name": None}, "moderation": {"flagCount": 0}, "user": "acct:pm5@ggv.tw", "hidden": False, "document": {"title": ["政院推台灣AI行動計畫 四年至少360億元 | 財經焦點 | 產經 | 聯合新聞網"]}, "id": "ljSw7iv9Eeilw3M5xviqxw", "permissions": {"read": ["group:8VnXgMY2"], "admin": ["acct:pm5@ggv.tw"], "update": ["acct:pm5@ggv.tw"], "delete": ["acct:pm5@ggv.tw"]}})
    assert c.title == "政院推台灣AI行動計畫 四年至少360億元 | 財經焦點 | 產經 | 聯合新聞網"
    assert c.quote == "行政院科技會報執行秘書蔡志宏今（18）日表示，今年推動AI（人工智慧）的預算在90億元以上，預算來自科技預算以及前瞻基礎建設的數位建設；之後三年也保證預算在90億至100億元左右，相當於四年至少投入360億元。"
    assert c.source_url == "https://O.sense.tw/ljSw7iv9Eeilw3M5xviqxw"
    assert c.source_type == "外部意見"
    assert c.hypothesis_id == "ljSw7iv9Eeilw3M5xviqxw"
    assert c.tags == []


def test_trello_board_id(t):
    assert t.board_id == "Lo01hfDB"


def test_trello_authorization(t):
    assert t.api_key == "foobarbaz"
    assert t.token == "helloworld"



if __name__ == "__main__":
    pytest.run([__file__])
