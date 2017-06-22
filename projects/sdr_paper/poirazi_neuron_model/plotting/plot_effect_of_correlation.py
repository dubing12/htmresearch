# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2016, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

# This uses plotly to create a nice looking graph of average false positive
# error rates as a function of N, the dimensionality of the vectors.  I'm sorry
# this code is so ugly.

import plotly.plotly as py
from plotly.graph_objs import *
import os
from scipy import stats
import numpy

plotlyUser = os.environ['PLOTLY_USERNAME']
plotlyAPIKey = os.environ['PLOTLY_API_KEY']


py.sign_in(plotlyUser, plotlyAPIKey)


# Calculated error values

correlations2000 = []
errors2000 = []
with open("../correlation_results_a32_n2000_s20.txt", "rb") as f:
  for line in f:
    [correlation, fp, total] = map(float, line.split(","))
    correlations2000.append(correlation)
    errors2000.append(fp/total)

correlations4000 = []
errors4000 = []
with open("../correlation_results_a32_n4000_s20.txt", "rb") as f:
  for line in f:
    [correlation, fp, total] = map(float, line.split(","))
    correlations4000.append(correlation)
    errors4000.append(fp/total)

correlationsa64 = []
errorsa64 = []
with open("../correlation_results_a64_n4000_s40.txt", "rb") as f:
  for line in f:
    [correlation, fp, total] = map(float, line.split(","))
    correlationsa64.append(correlation)
    errorsa64.append(fp/total)


mean_errors2000, bin_ends2000, _ = stats.binned_statistic(correlations2000, errors2000, bins = 10)
bin_midpoints2000 = [numpy.mean([bin_ends2000[i], bin_ends2000[i+1]]) for i in range(len(bin_ends2000) - 1)]

mean_errors4000, bin_ends4000, _ = stats.binned_statistic(correlations4000, errors4000, bins = 10)
bin_midpoints4000 = [numpy.mean([bin_ends4000[i], bin_ends4000[i+1]]) for i in range(len(bin_ends4000) - 1)]


mean_errorsa64, bin_endsa64, _ = stats.binned_statistic(correlationsa64, errorsa64, bins = 10)
bin_midpointsa64 = [numpy.mean([bin_endsa64[i], bin_endsa64[i+1]]) for i in range(len(bin_endsa64) - 1)]


trace1 = Scatter(
    y=errors2000,
    x=correlations2000,
    mode = "markers",
    marker=Marker(
      symbol="octagon",
      size=12,
      color="rgb(0, 0, 0)",
    ),
    name="a=32, n=2000"
)

trace2 = Scatter(
    y=mean_errors2000,
    x=bin_midpoints2000,
    mode = "markers+lines",
    marker=Marker(
      symbol="octagon",
      size=12,
      color="rgb(255, 0, 0)",
    ),
    name="a=32, n=2000"
)

trace3 = Scatter(
    y=errors4000,
    x=correlations4000,
    mode = "markers",
    marker=Marker(
      symbol="octagon",
      size=12,
      color="rgb(0, 0, 255)",
    ),
    name="a=32, n=2000"
)

trace4 = Scatter(
    y=mean_errors4000,
    x=bin_midpoints4000,
    mode = "lines+markers",
    marker=Marker(
      symbol="octagon",
      size=12,
      color="rgb(0, 0, 255)",
    ),
    name="a=32, n=2000"
)

trace5 = Scatter(
    y=errorsa64,
    x=correlationsa64,
    mode = "markers",
    marker=Marker(
      symbol="octagon",
      size=12,
      color="rgb(0, 0, 255)",
    ),
    name="a=32, n=2000"
)

trace6 = Scatter(
    y=mean_errorsa64,
    x=bin_midpointsa64,
    mode = "lines+markers",
    marker=Marker(
      symbol="octagon",
      size=12,
      color="rgb(0, 255, 0)",
    ),
    name="a=32, n=2000"
)

data = Data([trace2, trace4, trace6])

layout = Layout(
    title='',
    showlegend=False,
    autosize=False,
    width=855,
    height=700,
    xaxis=XAxis(
        title='Pattern correlation (r)',
        titlefont=Font(
            family='',
            size=26,
            color=''
        ),
        tickfont=Font(
            family='',
            size=16,
            color=''
        ),
        exponentformat="none",
        dtick=0.1,
        showline=True,
        range=[0,0.15],
    ),
    yaxis=YAxis(
        title='Accuracy',
        autorange=True,
        type='log',
        exponentformat='power',
        titlefont=Font(
            family='',
            size=26,
            color=''
        ),
        tickfont=Font(
            family='',
            size=12,
            color=''
        ),
        showline=True,
    ),
    annotations=Annotations([
      Annotation(
            x=16988,
            y=0.1143,
            xref='x',
            yref='paper',
            text='$a = 64$',
            showarrow=False,
            font=Font(
                family='',
                size=16,
                color=''
            ),
            align='center',
            textangle=0,
            bordercolor='',
            borderwidth=1,
            borderpad=1,
            bgcolor='rgba(0, 0, 0, 0)',
            opacity=1
        ),
      Annotation(
            x=17103,
            y=0.259,
            xref='x',
            yref='paper',
            text='$a = 128$',
            showarrow=False,
            font=Font(
                family='',
                size=16,
                color=''
            ),
            align='center',
            textangle=0,
            bordercolor='',
            borderwidth=1,
            borderpad=1,
            bgcolor='rgba(0, 0, 0, 0)',
            opacity=1
        ),
      Annotation(
            x=17132,
            y=0.411,
            xref='x',
            yref='paper',
            text='$a = 256$',
            showarrow=False,
            font=Font(
                family='',
                size=16,
                color=''
            ),
            align='center',
            textangle=0,
            bordercolor='',
            borderwidth=1,
            borderpad=1,
            bgcolor='rgba(0, 0, 0, 0)',
            opacity=1
        ),
      Annotation(
            x=16845,
            y=0.933,
            xref='x',
            yref='paper',
            text='$a = \\frac{n}{2}$',
            showarrow=False,
            font=Font(
                family='',
                size=16,
                color=''
            ),
            align='center',
            textangle=0,
            bordercolor='',
            borderwidth=1,
            borderpad=1,
            bgcolor='rgba(0, 0, 0, 0)',
            opacity=1
        ),
    ]),)

fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)
print "url=",plot_url
figure = py.get_figure(plot_url)
py.image.save_as(figure, 'images/effect_of_n.png', scale=4)
