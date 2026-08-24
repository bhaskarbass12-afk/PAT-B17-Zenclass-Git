import pytest
from Action_chain_task import Actionchain

URL = "https://jqueryui.com/droppable/"

@pytest.fixture
def bot():
    """Create the Actionchain object, open the page, yield it, then quit."""
    obj = Actionchain(url=URL)
    obj.get_url()
    yield obj
    obj.quit()

def test_page_opens_positive(bot):
    """POSITIVE: the correct jQuery UI page loads."""
    title = bot.get_title()
    assert "jQuery UI" in title

def test_drag_and_drop_positive(bot):
    """POSITIVE: dropping the white box on the yellow box shows 'Dropped!'."""
    result_text = bot.perform_drag_drop()
    assert "Dropped" in result_text

def test_drag_and_drop_negative(bot):
    """NEGATIVE: an incomplete drag should NOT trigger the drop."""
    result_text = bot.perform_invalid_drop()
    assert "Dropped" not in result_text