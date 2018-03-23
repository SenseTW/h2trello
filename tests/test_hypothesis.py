
import pytest
from sensetw.components.hypothesis import Hypothesis, Annotation, \
    annotation_to_card
import json
import os

with open(os.path.join(os.path.dirname(__file__), "annotation.json")) as fh:
    annotation_json = json.load(fh)


@pytest.fixture
def h():
    return Hypothesis(
        api_url="https://sense.tw/api",
        api_key="12345",
        title="",
        url="https://sense.tw/groups/8VnXgMY2/tai-wan-xin-chuang-gong-si")


def test_hypothesis_group_id(h):
    assert h.group_id == "8VnXgMY2"


def test_hypothesis_search_group_url(h):
    assert h.group_search_url().find(
            "https://sense.tw/api/search?group=8VnXgMY2") == 0


def test_hypothesis_annotation_to_card(h):
    c = annotation_to_card(Annotation.from_json(annotation_json))
    assert c.title == "政院推台灣AI行動計畫 四年至少360億元   財經焦點   產經   聯合新聞網"
    assert c.quote == "行政院科技會報執行秘書蔡志宏今（18）日表示，今年推動AI（人工智慧）的預算在90億元以上，預算來自科技預算以及前瞻基礎建設的數位建設；之後三年也保證預算在90億至100億元左右，相當於四年至少投入360億元。"
    assert c.source_url == "https://O.sense.tw/ljSw7iv9Eeilw3M5xviqxw"
    assert c.source_type == "外部意見"
    assert c.hypothesis_id == "ljSw7iv9Eeilw3M5xviqxw"
    assert c.tags == []
    assert c.comments == []


def test_annotation_from_json():
    a = Annotation.from_json(annotation_json)
    assert a.title == "政院推台灣AI行動計畫 四年至少360億元   財經焦點   產經   聯合新聞網"
    assert a.quote == "行政院科技會報執行秘書蔡志宏今（18）日表示，今年推動AI（人工智慧）的預算在90億元以上，預算來自科技預算以及前瞻基礎建設的數位建設；之後三年也保證預算在90億至100億元左右，相當於四年至少投入360億元。"
    assert a.uri == "https://udn.com/news/story/7238/2937685"
    assert a.link == "https://O.sense.tw/ljSw7iv9Eeilw3M5xviqxw"
    assert a.id == "ljSw7iv9Eeilw3M5xviqxw"
    assert a.tags == []
    assert a.text == ""


if __name__ == "__main__":
    pytest.run([__file__])
