import pandas as pd
import pytest

from nbtext import urn_from_text, pure_urn, row_agg, col_agg

text_with_urns = """Test deg selv
id: 39577b6d249ec9eccbfa32bd1b4c7a1f
urn: URN:NBN:no-nb_digibok_2014051408028
Test i norsk for framandspråklege : mellomnivå : eksempeltest
id: 73ea67ce0a860467028374caf92d78fc
urn: URN:NBN:no-nb_digibok_2016010508155
Test av brukskvalitet : trafikkinfo Gardermoen
id: 1b627ca187f9b1b9ee40738db32333ce
urn: URN:NBN:no-nb_digibok_2010041205087"""


def test_urn_from_text():
    res = urn_from_text(text_with_urns)
    assert len(res) == 3
    assert res[0] == "2014051408028"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        # List of lists
        ([
            ["2014051408028", 'extra data'],
            ["2016010508155", 'extra data'],
            ["2010041205087", 'more extra data']
         ],
         ["2014051408028", "2016010508155", "2010041205087"]),
        # List of URNs
        (["2014051408028", "2016010508155", "2010041205087"],
         ["2014051408028", "2016010508155", "2010041205087"]),
        # Text
        (text_with_urns, ["2014051408028", "2016010508155", "2010041205087"]),
        # Other
        ({'key': 'value'}, [])
    ])
def test_pure_urn(test_input, expected):
    res = pure_urn(test_input)
    assert res == expected


def test_row_agg():
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [2, 3, 5]})
    expected = pd.DataFrame({'sum': [3, 5, 8]})
    assert row_agg(df).equals(expected)

    # Custom column name
    expected = pd.DataFrame({'total': [3, 5, 8]})
    assert row_agg(df, 'total').equals(expected)


def test_col_agg():
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [2, 3, 5]})
    expected = pd.DataFrame({'sum': [6, 10]}, index=['a', 'b'])
    assert col_agg(df).equals(expected)

    # Custom column name
    expected = pd.DataFrame({'total': [6, 10]}, index=['a', 'b'])
    assert col_agg(df, 'total').equals(expected)
