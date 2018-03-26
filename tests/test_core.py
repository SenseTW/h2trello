
import pytest
from sensetw import Card, Mapping


def test_basics():
    c = Card(
        hypothesis_id="12345",
        title="科技部啟動半導體射月計畫　促成人工智慧終端(AI Edge)產業鏈技術躍升",
        quote="本計畫的總體目標將以挑戰2022年智慧終端(AI Edge)關鍵技術極限，開發應用於各類終端裝置上的AI晶片。不同於雲端數據中心具有強大運算功能的人工智慧，智慧終端的AI技術需具備簡化、低功耗、及通訊射頻功能的深度推理架構，甚至能於終端裝置上具有深度學習的能力。",
        source_url="https://O.sense.tw/zzE6YCdEEeil_FeHqIHjFg",
        tags=[],
        source_type="外部意見",
        comments=[])

    assert c.source_url == "https://O.sense.tw/zzE6YCdEEeil_FeHqIHjFg"
    assert c.source_type == "外部意見"


def test_mapping():
    m = Mapping(hypothesis_url="https://sense.tw/groups/12345/",
                trello_url="https://trello.com/b/Lo01hfDB/")
    assert m.hypothesis_group_id == "12345"
    assert m.trello_board_id == "Lo01hfDB"
    assert m.id == "12345:Lo01hfDB"


if __name__ == "__main__":
    pytest.run([__file__])
