"""Plotting."""
import logging

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

try:
    import contextily as cx
except ImportError:
    cx = None

from . import settings


def plot_temperature_map(  # noqa: C901
    ts_gdf,
    *,
    dt=None,
    ax=None,
    cmap=None,
    legend=None,
    legend_position=None,
    legend_size=None,
    legend_pad=None,
    title=None,
    add_basemap=None,
    attribution=None,
    subplot_kws=None,
    plot_kws=None,
    set_title_kws=None,
    add_basemap_kws=None,
    append_axes_kws=None,
):
    """
    Plot a map of station measurements.

    Parameters
    ----------
    ts_gdf : geopandas.GeoDataFrame
        Geo-data frame with a time series of temperature measurements.
    dt : str or datetime, optional
        String or datetime instance representing the instant to be plotted. The value
        must match a column of `ts_gdf`. If None, the first column (other than
        `geometry`) is used.
    ax : `matplotlib.axes.Axes` instancd, optional
        Plot in given axis. If None creates a new figure.
    cmap : str or `matplotlib.colors.Colormap` instance, optional
        Colormap of the plot. If None, the value from `settings.PLOT_CMAP` is used.
    legend : bool, optional
        Whether a legend should be added to the plot. If None, the value from
        `settings.PLOT_LEGEND` is used.
    legend_position : str {"left", "right", "bottom", "top"}, optional
        Position of the legend axes, passed to
        `mpl_toolkits.axes_grid1.axes_divider.AxesDivider.append_axes`. If None, the
        value from `settings.PLOT_LEGEND_POSITION` is used.
    legend_size : numeric or str, optional
        Size of the legend axes, passed to
        `mpl_toolkits.axes_grid1.axes_divider.AxesDivider.append_axes`. If None, the
        value from `settings.PLOT_LEGEND_SIZE` is used.
    legend_pad : numeric or str, optional
        Padding between the plot and legend axes, passed to
        `mpl_toolkits.axes_grid1.axes_divider.AxesDivider.append_axes`. If None, the
        value from `settings.PLOT_LEGEND_PAD` is used.
    title : bool or str, optional
        Whether a title should be added to the plot. If True, the timestamp of the
        snapshot (geo-data frame column) is used. It is also possible to pass a string
        so that it is used as title label (instead of the timestamp). If None, the value
        from `settings.PLOT_TITLE` is used.
    add_basemap : bool, optional
        Whether a basemap should be added to the plot using `contextily.add_basemap`. If
        None, the value from `settings.PLOT_ADD_BASEMAP` is used.
    attribution : str or bool, optional
        Attribution text for the basemap source, added to the bottom of the plot, passed
        to `contextily.add_basemap`. If False, no attribution is added. If None, the
        value from `settings.PLOT_ATTRIBUTION` is used.
    subplot_kws, plot_kws, set_title_kws, add_basemap_kws, append_axes_kws : dict, \
                                                                             optional
        Keyword arguments passed to `matplotlib.pyplot.subplots`,
        `geopandas.GeoDataFrame.plot`, `matplotlib.axes.Axes.set_title`,
        `contextily.add_basemap` and
        `mpl_toolkits.axes_grid1.axes_divider.AxesDivider.append_axes` respectively.

    Returns
    -------
    ax : `matplotlib.axes.Axes`
        Axes with the plot drawn onto it.
    """
    # if no column is provided, we plot the "first" column other than "geometry"
    if dt is None:
        dt = ts_gdf.columns.drop("geometry")[0]

    # subplots arguments
    if ax is None:
        if subplot_kws is None:
            subplot_kws = {}
        fig, ax = plt.subplots(**subplot_kws)
    # plot arguments
    if plot_kws is None:
        _plot_kws = {}
    else:
        _plot_kws = plot_kws.copy()
    # _plot_kws = {key: plot_kws[key] for key in plot_kws}
    if cmap is None:
        cmap = _plot_kws.pop("cmap", settings.PLOT_CMAP)
    if legend is None:
        legend = _plot_kws.pop("legend", settings.PLOT_LEGEND)

    # plot
    if legend:
        divider = make_axes_locatable(ax)
        if legend_position is None:
            legend_position = settings.PLOT_LEGEND_POSITION
        if legend_size is None:
            legend_size = settings.PLOT_LEGEND_SIZE
        if append_axes_kws is None:
            _append_axes_kws = {}
        else:
            _append_axes_kws = append_axes_kws.copy()
        if legend_pad is None:
            legend_pad = _append_axes_kws.pop("pad", settings.PLOT_LEGEND_PAD)
        _plot_kws["cax"] = divider.append_axes(
            legend_position, legend_size, pad=legend_pad, **_append_axes_kws
        )
    ts_gdf.plot(column=dt, cmap=cmap, ax=ax, legend=legend, **_plot_kws)
    if title is None:
        title = settings.PLOT_TITLE
    if title:
        if title is True:
            title_label = dt
        elif isinstance(title, str):
            title_label = title
        if set_title_kws is None:
            set_title_kws = {}
        ax.set_title(title_label, **set_title_kws)

    # basemap
    if add_basemap is None:
        add_basemap = settings.PLOT_ADD_BASEMAP
    if add_basemap:
        if cx is None:
            logging.warning(
                """
The `add_basemap=True` option requires the contextily package. You can install it using
conda or pip. See https://github.com/geopandas/contextily.
"""
            )

        # add_basemap arguments
        if add_basemap_kws is None:
            _add_basemap_kws = {}
        else:
            _add_basemap_kws = add_basemap_kws.copy()
        # _add_basemap_kws = {key: add_basemap_kws[key] for key in add_basemap_kws}
        if attribution is None:
            attribution = _add_basemap_kws.pop("attribution", settings.PLOT_ATTRIBUTION)
        # add basemap
        cx.add_basemap(
            ax=ax,
            crs=ts_gdf.crs,
            attribution=attribution,
            **_add_basemap_kws,
        )

    return ax
