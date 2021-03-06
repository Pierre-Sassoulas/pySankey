# -*- coding: utf-8 -*-
r"""
Produces simple Sankey Diagrams with matplotlib.
@author: Anneya Golob & marcomanz & pierre-sassoulas & jorwoods & vgalisson
                      .-.
                 .--.(   ).--.
      <-.  .-.-.(.->          )_  .--.
       `-`(     )-'             `)    )
         (o  o  )                `)`-'
        (      )                ,)
        ( ()  )                 )
         `---"\    ,    ,    ,/`
               `--' `--' `--'
                |  |   |   |
                |  |   |   |
                '  |   '   |
"""

import logging
import warnings
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

LOGGER = logging.getLogger(__name__)


class PySankeyException(Exception):
    """ Generic PySankey Exception. """


class NullsInFrame(PySankeyException):
    pass


class LabelMismatch(PySankeyException):
    pass


def check_data_matches_labels(labels, data, side):
    """Check whether or not data matches labels.

    Raise a LabelMismatch Exception if not."""
    if len(labels) > 0:
        if isinstance(data, list):
            data = set(data)
        if isinstance(data, pd.Series):
            data = set(data.unique().tolist())
        if isinstance(labels, list):
            labels = set(labels)
        if labels != data:
            msg = "\n"
            if len(labels) <= 20:
                msg = "Labels: " + ",".join(labels) + "\n"
            if len(data) < 20:
                msg += "Data: " + ",".join(data)
            raise LabelMismatch(
                "{0} labels and data do not match.{1}".format(side, msg)
            )


def sankey(
    left,
    right,
    leftWeight=None,
    rightWeight=None,
    colorDict=None,
    leftLabels=None,
    rightLabels=None,
    aspect=4,
    rightColor=False,
    fontsize=14,
    figureName=None,
    closePlot=False,
    figSize=None,
    ax=None,
):
    """
    Make Sankey Diagram showing flow from left-->right

    Inputs:
        left = NumPy array of object labels on the left of the diagram
        right = NumPy array of corresponding labels on the right of the diagram
            len(right) == len(left)
        leftWeight = NumPy array of weights for each strip starting from the
            left of the diagram, if not specified 1 is assigned
        rightWeight = NumPy array of weights for each strip starting from the
            right of the diagram, if not specified the corresponding leftWeight
            is assigned
        colorDict = Dictionary of colors to use for each label
            {'label':'color'}
        leftLabels = order of the left labels in the diagram
        rightLabels = order of the right labels in the diagram
        aspect = vertical extent of the diagram in units of horizontal extent
        rightColor = If true, each strip in the diagram will be be colored
                    according to its left label
        figSize = tuple setting the width and height of the sankey diagram.
            Defaults to current figure size
        ax = optional, matplotlib axes to plot on, otherwise uses current axes.
    Output:
        ax : matplotlib Axes
    """
    ax, leftLabels, leftWeight, rightLabels, rightWeight = init_values(
        ax,
        closePlot,
        figSize,
        figureName,
        left,
        leftLabels,
        leftWeight,
        rightLabels,
        rightWeight,
    )
    plt.rc("text", usetex=False)
    plt.rc("font", family="serif")
    dataFrame = create_datadrame(left, leftWeight, right, rightWeight)
    # Identify all labels that appear 'left' or 'right'
    allLabels = pd.Series(
        np.r_[dataFrame.left.unique(), dataFrame.right.unique()]
    ).unique()
    LOGGER.debug("Labels to handle : %s", allLabels)
    leftLabels, rightLabels = identify_labels(dataFrame, leftLabels, rightLabels)
    colorDict = create_colors(allLabels, colorDict)
    ns_l, ns_r = determine_widths(dataFrame, leftLabels, rightLabels)
    # Determine positions of left label patches and total widths
    leftWidths, topEdge = _get_positions_and_total_widths(dataFrame, leftLabels, "left")
    # Determine positions of right label patches and total widths
    rightWidths, topEdge = _get_positions_and_total_widths(
        dataFrame, rightLabels, "right"
    )
    # Total vertical extent of diagram
    xMax = topEdge / aspect
    draw_vertical_bars(
        ax, colorDict, fontsize, leftLabels, leftWidths, rightLabels, rightWidths, xMax
    )
    plot_strips(
        ax,
        colorDict,
        dataFrame,
        leftLabels,
        leftWidths,
        ns_l,
        ns_r,
        rightColor,
        rightLabels,
        rightWidths,
        xMax,
    )
    if figSize is not None:
        plt.gcf().set_size_inches(figSize)
    save_image(figureName)
    if closePlot:
        plt.close()
    return ax


def save_image(figureName):
    if figureName is not None:
        fileName = "{}.png".format(figureName)
        plt.savefig(fileName, bbox_inches="tight", dpi=150)
        LOGGER.info("Sankey diagram generated in '%s'", fileName)


def identify_labels(dataFrame, leftLabels, rightLabels):
    # Identify left labels
    if len(leftLabels) == 0:
        leftLabels = pd.Series(dataFrame.left.unique()).unique()
    else:
        check_data_matches_labels(leftLabels, dataFrame["left"], "left")
    # Identify right labels
    if len(rightLabels) == 0:
        rightLabels = pd.Series(dataFrame.right.unique()).unique()
    else:
        check_data_matches_labels(rightLabels, dataFrame["right"], "right")
    return leftLabels, rightLabels


def init_values(
    ax,
    closePlot,
    figSize,
    figureName,
    left,
    leftLabels,
    leftWeight,
    rightLabels,
    rightWeight,
):
    deprecation_warnings(closePlot, figSize, figureName)
    if ax is None:
        ax = plt.gca()
    if leftWeight is None:
        leftWeight = []
    if rightWeight is None:
        rightWeight = []
    if leftLabels is None:
        leftLabels = []
    if rightLabels is None:
        rightLabels = []
    # Check weights
    if len(leftWeight) == 0:
        leftWeight = np.ones(len(left))
    if len(rightWeight) == 0:
        rightWeight = leftWeight
    return ax, leftLabels, leftWeight, rightLabels, rightWeight


def deprecation_warnings(closePlot, figSize, figureName):
    warn = []
    if figureName is not None:
        msg = "use of figureName in sankey() is deprecated"
        warnings.warn(msg, DeprecationWarning)
        warn.append(msg[7:-14])
    if closePlot is not False:
        msg = "use of closePlot in sankey() is deprecated"
        warnings.warn(msg, DeprecationWarning)
        warn.append(msg[7:-14])
    if figSize is not None:
        msg = "use of figSize in sankey() is deprecated"
        warnings.warn(msg, DeprecationWarning)
        warn.append(msg[7:-14])
    if warn:
        LOGGER.warning(
            " The following arguments are deprecated and should be removed: %s",
            ", ".join(warn),
        )


def determine_widths(dataFrame, leftLabels, rightLabels):
    # Determine widths of individual strips
    ns_l = defaultdict()
    ns_r = defaultdict()
    for leftLabel in leftLabels:
        leftDict = {}
        rightDict = {}
        for rightLabel in rightLabels:
            leftDict[rightLabel] = dataFrame[
                (dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)
            ].leftWeight.sum()
            rightDict[rightLabel] = dataFrame[
                (dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)
            ].rightWeight.sum()
        ns_l[leftLabel] = leftDict
        ns_r[leftLabel] = rightDict
    return ns_l, ns_r


def draw_vertical_bars(
    ax, colorDict, fontsize, leftLabels, leftWidths, rightLabels, rightWidths, xMax
):
    # Draw vertical bars on left and right of each  label's section & print label
    for leftLabel in leftLabels:
        ax.fill_between(
            [-0.02 * xMax, 0],
            2 * [leftWidths[leftLabel]["bottom"]],
            2 * [leftWidths[leftLabel]["bottom"] + leftWidths[leftLabel]["left"]],
            color=colorDict[leftLabel],
            alpha=0.99,
        )
        ax.text(
            -0.05 * xMax,
            leftWidths[leftLabel]["bottom"] + 0.5 * leftWidths[leftLabel]["left"],
            leftLabel,
            {"ha": "right", "va": "center"},
            fontsize=fontsize,
        )
    for rightLabel in rightLabels:
        ax.fill_between(
            [xMax, 1.02 * xMax],
            2 * [rightWidths[rightLabel]["bottom"]],
            2 * [rightWidths[rightLabel]["bottom"] + rightWidths[rightLabel]["right"]],
            color=colorDict[rightLabel],
            alpha=0.99,
        )
        ax.text(
            1.05 * xMax,
            rightWidths[rightLabel]["bottom"] + 0.5 * rightWidths[rightLabel]["right"],
            rightLabel,
            {"ha": "left", "va": "center"},
            fontsize=fontsize,
        )


def create_colors(allLabels, colorDict):
    # If no colorDict given, make one
    if colorDict is None:
        colorDict = {}
        palette = "hls"
        colorPalette = sns.color_palette(palette, len(allLabels))
        for i, label in enumerate(allLabels):
            colorDict[label] = colorPalette[i]
    else:
        missing = [label for label in allLabels if label not in colorDict.keys()]
        if missing:
            msg = (
                "The colorDict parameter is missing values for the following labels : "
            )
            msg += "{}".format(", ".join(missing))
            raise ValueError(msg)
    LOGGER.debug("The colordict value are : %s", colorDict)
    return colorDict


def create_datadrame(left, leftWeight, right, rightWeight):
    # Create Dataframe
    if isinstance(left, pd.Series):
        left = left.reset_index(drop=True)
    if isinstance(right, pd.Series):
        right = right.reset_index(drop=True)
    dataFrame = pd.DataFrame(
        {
            "left": left,
            "right": right,
            "leftWeight": leftWeight,
            "rightWeight": rightWeight,
        },
        index=range(len(left)),
    )
    if len(dataFrame[(dataFrame.left.isnull()) | (dataFrame.right.isnull())]):
        raise NullsInFrame("Sankey graph does not support null values.")
    return dataFrame


def plot_strips(
    ax,
    colorDict,
    dataFrame,
    leftLabels,
    leftWidths,
    ns_l,
    ns_r,
    rightColor,
    rightLabels,
    rightWidths,
    xMax,
):
    # Plot strips
    for leftLabel in leftLabels:
        for rightLabel in rightLabels:
            labelColor = leftLabel
            if rightColor:
                labelColor = rightLabel
            if (
                len(
                    dataFrame[
                        (dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)
                    ]
                )
                > 0
            ):
                # Create array of y values for each strip, half at left value,
                # half at right, convolve
                ys_d = np.array(
                    50 * [leftWidths[leftLabel]["bottom"]]
                    + 50 * [rightWidths[rightLabel]["bottom"]]
                )
                ys_d = np.convolve(ys_d, 0.05 * np.ones(20), mode="valid")
                ys_d = np.convolve(ys_d, 0.05 * np.ones(20), mode="valid")
                ys_u = np.array(
                    50 * [leftWidths[leftLabel]["bottom"] + ns_l[leftLabel][rightLabel]]
                    + 50
                    * [rightWidths[rightLabel]["bottom"] + ns_r[leftLabel][rightLabel]]
                )
                ys_u = np.convolve(ys_u, 0.05 * np.ones(20), mode="valid")
                ys_u = np.convolve(ys_u, 0.05 * np.ones(20), mode="valid")

                # Update bottom edges at each label so next strip starts at the
                # right place
                leftWidths[leftLabel]["bottom"] += ns_l[leftLabel][rightLabel]
                rightWidths[rightLabel]["bottom"] += ns_r[leftLabel][rightLabel]
                ax.fill_between(
                    np.linspace(0, xMax, len(ys_d)),
                    ys_d,
                    ys_u,
                    alpha=0.65,
                    color=colorDict[labelColor],
                )
    ax.axis("off")


def _get_positions_and_total_widths(df, labels, side):
    """ Determine positions of label patches and total widths"""
    widths = defaultdict()
    for i, label in enumerate(labels):
        labelWidths = {}
        labelWidths[side] = df[df[side] == label][side + "Weight"].sum()
        if i == 0:
            labelWidths["bottom"] = 0
            labelWidths["top"] = labelWidths[side]
        else:
            bottomWidth = widths[labels[i - 1]]["top"]
            weightedSum = 0.02 * df[side + "Weight"].sum()
            labelWidths["bottom"] = bottomWidth + weightedSum
            labelWidths["top"] = labelWidths["bottom"] + labelWidths[side]
            topEdge = labelWidths["top"]
        widths[label] = labelWidths
        LOGGER.debug("%s position of '%s' : %s", side, label, labelWidths)

    return widths, topEdge
