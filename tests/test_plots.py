import numpy as np
from matplotlib.figure import Figure
from app.plots import channel_histogram_figure
def test_histogram_returns_three_axes():
    fig=channel_histogram_figure(np.zeros((2,2,3)))
    assert isinstance(fig,Figure) and len(fig.axes)==3
