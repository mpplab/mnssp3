# -*- coding: utf-8 -*-
"""Main module."""


import sys
import matplotlib.pyplot as plt

import numpy as np
from matplotlib.patheffects import RendererBase
from matplotlib import transforms
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FormatStrFormatter
from .utils import despine
from .colorschemes import default_colorschemes
from matplotlib.lines import Line2D

from .format_utils import process_data


class Scale(RendererBase):
    """Scale alphabets using affine transformation"""

    def __init__(self, sx, sy=None):
        self._sx = sx
        self._sy = sy

    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        affine = affine.identity().scale(self._sx, self._sy) + affine
        renderer.draw_path(gc, tpath, affine, rgbFace)


def _setup_plt():
    plt.rcParams['savefig.dpi'] = 120
    plt.rcParams['figure.dpi'] = 120
    plt.rcParams['figure.autolayout'] = False
    plt.rcParams['figure.figsize'] = 12, 8
    plt.rcParams['axes.labelsize'] = 18
    plt.rcParams['axes.titlesize'] = 20
    plt.rcParams['font.size'] = 16
    plt.rcParams['lines.linewidth'] = 2.0
    plt.rcParams['lines.markersize'] = 8
    plt.rcParams['legend.fontsize'] = 14


def _setup_font(fontfamily='Arial', fontsize=12):
    """Setup font properties"""

    #_setup_plt()
    font = FontProperties()
    font.set_size(fontsize)
    font.set_weight('bold')
    font.set_family(fontfamily)
    return font


def setup_axis(ax,
               axis='x',
               majorticks=10,
               minorticks=5,
               xrotation=0,
               yrotation=0):
    """Setup axes defaults"""

    major_locator = MultipleLocator(majorticks)
    major_formatter = FormatStrFormatter('%d')
    minor_locator = MultipleLocator(minorticks)
    if axis == 'x':
        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_major_formatter(major_formatter)
        ax.xaxis.set_minor_locator(minor_locator)

    elif axis == 'y':
        ax.yaxis.set_major_locator(major_locator)
        ax.yaxis.set_major_formatter(major_formatter)
        ax.yaxis.set_minor_locator(minor_locator)
    elif axis == 'both':
        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_major_formatter(major_formatter)
        ax.yaxis.set_minor_locator(minor_locator)
        ax.yaxis.set_major_locator(major_locator)
        ax.yaxis.set_major_formatter(major_formatter)
        ax.yaxis.set_minor_locator(minor_locator)
    ax.tick_params(which='major', width=2, length=10)
    ax.tick_params(which='minor', width=1, length=6)


def _draw_text_data_coord(height_matrix,
                          ax,
                          fontfamily,
                          colorscheme='classic',
                          scalex=1,
                          draw_axis=False,
                          debug=False):
    fig = ax.get_figure()
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    fontsize = (height / 1.7) * 72.0 / fig.dpi  #/72.0
    font = _setup_font(fontsize=fontsize, fontfamily=fontfamily)
    trans_offset = transforms.offset_copy(
        ax.transData, fig=fig, x=1, y=0, units='points')
    if not isinstance(colorscheme, dict):
        colorscheme = default_colorschemes[colorscheme]

    for xindex, xcol in enumerate(height_matrix):
        yshift = 0
        total_shift = 0
        total_score = 0
        for basechar, basescore in xcol:
            txt = ax.text(
                xindex + 1,
                0,
                basechar,
                transform=trans_offset,
                fontsize=fontsize,
                color=colorscheme[basechar],
                ha='center',
                va='baseline',
                family='monospace',
                #va='baseline',
                fontproperties=font, )
            txt.set_path_effects([Scale(1.0, basescore)])
            fig.canvas.draw()
            window_ext = txt.get_window_extent(
                txt._renderer)  #(fig.canvas.renderer) #txt._renderer)
            if basescore > 0.3:
                yshift = window_ext.height * basescore  #- fontsize/10# fontsize/4#/1.20 #*.85 #* fig.dpi/72.0
            else:
                yshift = window_ext.height * basescore  # - fontsize/11# fontsize/4#/1.20 #*.85 #* fig.dpi/72.0

            total_score += basescore

            if debug:
                ax.axhline(
                    y=total_score, color='r', linstyle='dashed', linewidth=1)
            trans_offset = transforms.offset_copy(
                txt._transform, fig=fig, y=yshift, units='dots')
        trans_offset = transforms.offset_copy(
            ax.transData, fig=fig, x=1, y=0, units='dots')
    if not draw_axis:
        ax.axis('off')


def _draw_text_display_coord(height_matrix,
                             ax,
                             fontfamily,
                             colorscheme='classic',
                             scalex=1,
                             is_protein=False,
                             draw_axis=False):
    xshifts_list = []
    fig = ax.get_figure()
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    fontsize = (height / 1.7) * 72.0 / fig.dpi
    font = _setup_font(fontsize=fontsize, fontfamily=fontfamily)
    xshift = 160
    xshifts_list.append(xshift)
    trans_offset = transforms.offset_copy(
        ax.transData, fig=fig, x=xshift, y=0, units='dots')
    ax.trans_offsets = [trans_offset]
    if not isinstance(colorscheme, dict):
        colorscheme = default_colorschemes[colorscheme]
    for xindex, xcol in enumerate(height_matrix):
        yshift = 0
        total_shift = 0
        total_score = 0
        for basechar, basescore in xcol:
            txt = ax.text(
                0,
                0,
                basechar,
                transform=trans_offset,
                fontsize=fontsize,
                color=colorscheme[basechar],
                va='baseline',
                family='monospace',
                ha='center',
                fontproperties=font)

            txt.set_path_effects([Scale(scalex, basescore)])
            fig.canvas.draw()
            window_ext = txt.get_window_extent(
                txt._renderer)  #(fig.canvas.renderer) #txt._renderer)
            if basescore > 0.3:
                yshift = window_ext.height * basescore  # - fontsize/10# fontsize/4#/1.20 #*.85 #* fig.dpi/72.0
            else:
                yshift = window_ext.height * basescore  # - fontsize/11# fontsize/4#/1.20 #*.85 #* fig.dpi/72.0

            total_score += basescore
            trans_offset = transforms.offset_copy(  #ax.transData,
                txt._transform,
                fig=fig,
                y=yshift,
                #x=xshift,
                units='dots')
        if is_protein:
            trans_offset1 = transforms.offset_copy(
                ax.transData,
                fig=fig,
                x=xshift + (window_ext.width * (scalex - 2) + 10 *
                            (scalex - 2)),
                y=0,
                units='dots')

        else:
            trans_offset1 = transforms.offset_copy(
                ax.transData, fig=fig, x=xshift, y=0, units='dots')
        xshift += window_ext.width * scalex + 10 * scalex
        xshifts_list.append(xshift)

        trans_offset = transforms.offset_copy(
            ax.transData, fig=fig, x=xshift, y=0, units='dots')
        if draw_axis:
            line = Line2D(
                [0, 0], [0, -0.1],
                transform=trans_offset1,
                linewidth=2,
                clip_on=False,
                color='black')
            ax.add_line(line)
            if xindex < len(height_matrix) - 1:
                line = Line2D(
                    [0, 1], [0, 0],
                    transform=trans_offset1,
                    linewidth=0.5,
                    clip_on=False,
                    color='black')
                ax.add_line(line)
            ax.text(
                0, -0.2, str(xindex + 1), transform=trans_offset1, ha='center')
            ax.trans_offsets.append(trans_offset1)

    ax.set_xticks([])
    ax.set_xticklabels([])
    return xshifts_list


def draw_protein(data,
                 ax,
                 data_type='bits',
                 seq_type='dna',
                 yaxis='bits',
                 colorscheme='classic',
                 fontfamily='Arial',
                 scalex=3):
    #ax.set_xticks(range(1, len(data)*3 + 1))
    if yaxis == 'probability':
        ax.set_yticks(list(range(0, 2)))
    elif yaxis == 'bits':
        ax.set_yticks(list(range(0, 3)))

    #ax.set_xticklabels(range(1, len(data) + 1), rotation=90)
    setup_axis(ax, 'y', majorticks=1, minorticks=0.1)

    _draw_text_display_coord(
        data, ax, fontfamily, colorscheme, scalex=scalex, is_protein=True)


def draw_logo(data,
              data_type='bits',
              seq_type='dna',
              yaxis='bits',
              colorscheme='classic',
              nrow=1,
              ncol=1,
              padding=0,
              draw_range=None,
              coordinate_type='data',
              draw_axis=False,
              fontfamily='Arial',
              debug=False,
              ax=None):
    """Draw sequence logo

    Parameters
    ----------

    data : str or dict or matrix

    data_type : str
        Options : 'msa', 'meme', 'jaspar', 'counts', 'pwm', 'pfm', 'ic'

    yaxis : str
        Type of plot. Options : 'probability', 'bits'

    colorscheme : str
        Colorschemes. Options for DNA : basepairing/classic.
                      AA : hydrophobicity, chemistry

    nrow : int
        Total nrows in column. This doesn't work with 'data' type dict

    ncol : int
        Total nrows in column. This doesn't work with 'data' type dict

    """
    if yaxis not in ['probability', 'bits']:
        sys.stderr.write(
            'yaxis can be {}, got {}\n'.format(['probability', 'bits'], yaxis))
        sys.exit(1)
    if not ax:
        fig, axarr = plt.subplots(nrow, ncol, squeeze=False)
        fig.set_size_inches(((len(data) + 1) * ncol, 3 * nrow))
        ax = axarr[0, 0]
    else:
        fig = ax.get_figure()
        axarr = np.array([[ax]])
        ax.set_xticks(list(range(1, len(data) + 1)))

        ax.set_xticklabels(list(range(1, len(data) + 1)), rotation=90)
        pfm, ic = process_data(data, data_type=data_type, seq_type=seq_type)
        if yaxis == 'probability':
            xshifts_list = _draw_text_data_coord(
                pfm, ax, fontfamily, colorscheme, draw_axis=draw_axis)
        else:
            xshifts_list = _draw_text_data_coord(
                ic, ax, fontfamily, colorscheme, draw_axis=draw_axis)
        #ax.axis('off')
        #despine(
        #    ax=ax,
        #    trim=False,
        #    top=True,
        #    right=True,
        #    bottom=True,
        #    offset=0)
        return

    #ax.set_xticks(range(1, len(data) + 1))
    if draw_axis:
        ax.set_xticks(list(range(len(data))))
        if yaxis == 'probability':
            ax.set_yticks(list(range(0, 2)))
        elif yaxis == 'bits':
            ax.set_yticks(list(range(0, 3)))

        #ax.set_xticklabels(range(1, len(data) + 1), rotation=90)
        setup_axis(ax, 'y', majorticks=1, minorticks=0.1)
    else:
        ax.axis('off')

    if data_type != 'bits':
        pfm, ic = process_data(data, data_type=data_type, seq_type=seq_type)
    else:
        ic = data
        pfm = data

    if draw_range:
        #    ic = np.array(ic)
        ic = ic[draw_range[0]:draw_range[1]]
        pfm = pfm[draw_range[0]:draw_range[1]]
    if coordinate_type == 'data':
        ax = axarr[0, 0]
        ax.set_xticks(list(range(1, len(data) + 1)))

        ax.set_xticklabels(list(range(1, len(data) + 1)), rotation=90)
        if yaxis == 'probability':
            xshifts_list = _draw_text_data_coord(
                pfm, ax, fontfamily, colorscheme, draw_axis=draw_axis)
        else:
            xshifts_list = _draw_text_data_coord(
                ic, ax, fontfamily, colorscheme, draw_axis=draw_axis)
    else:
        if yaxis == 'probability':
            xshifts_list = _draw_text_display_coord(
                pfm, ax, fontfamily, colorscheme, draw_axis=draw_axis)
        else:
            xshifts_list = _draw_text_display_coord(
                ic, ax, fontfamily, colorscheme, draw_axis=draw_axis)

    for i in range(nrow):
        for j in range(ncol):
            if i == j == 0:
                despine(
                    ax=axarr[i, j],
                    trim=False,
                    top=True,
                    right=True,
                    bottom=True)
                continue
            despine(
                ax=axarr[i, j],
                trim=False,
                top=True,
                right=True,
                bottom=True,
                offset=00)
            axi = axarr[i, j]
            #axi.get_shared_x_axes().join(axi, ax)
            #axi.set_xticklabels([])
            #ax.set_xticklabels(range(1, len(data) + 1), rotation=90)
    return fig, axarr
