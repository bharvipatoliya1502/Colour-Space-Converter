"""Matplotlib channel histogram helper."""
def channel_histogram_figure(yiq):
    import matplotlib
    matplotlib.use("Agg", force=True)
    from matplotlib.figure import Figure
    fig=Figure(figsize=(10,3))
    axes=fig.subplots(1,3)
    labels=("Y","I","Q")
    for i,ax in enumerate(axes):
        ax.hist(yiq[:,:,i].ravel(),bins=50)
        ax.set_title(f"{labels[i]} channel histogram")
        ax.set_xlabel("Channel value"); ax.set_ylabel("Pixel count")
    fig.tight_layout()
    return fig
