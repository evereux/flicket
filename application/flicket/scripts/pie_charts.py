#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import json

import plotly

from application.flicket.models.flicket_models import FlicketCategory
from application.flicket.models.flicket_models import FlicketDepartment
from application.flicket.models.flicket_models import FlicketStatus
from application.flicket.models.flicket_models import FlicketTicket


def count_department_tickets(department, status):
    query = FlicketTicket.query. \
        join(FlicketCategory). \
        join(FlicketStatus). \
        join(FlicketDepartment). \
        filter(FlicketDepartment.department == department). \
        filter(FlicketStatus.status == status)

    return query.count()


def create_pie_chart_dict():
    """

    :return:
    """

    statii = FlicketStatus.query
    departments = FlicketDepartment.query

    graphs = []

    for department in departments:

        graph_title = department.department
        graph_labels = []
        graph_values = []
        for status in statii:
            graph_labels.append(status.status)
            graph_values.append(count_department_tickets(graph_title, status.status))

        # append graphs if have values.
        if any(graph_values):
            graphs.append(
                dict(
                    data=[
                        dict(
                            labels=graph_labels,
                            values=graph_values,
                            type='pie',
                            marker=dict(
                                colors=['darkorange', 'darkgreen', 'green', 'lightgreen']
                            ),
                            sort=False
                        )
                    ],
                    layout=dict(
                        title=graph_title,
                        autosize=True,
                        margin=dict(
                            b=0,
                            t=40,
                            l=0,
                            r=0
                        ),
                        height=400,

                    ),
                )
            )

    ids = [f'Graph {i}' for i, _ in enumerate(graphs)]
    graph_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return ids, graph_json
