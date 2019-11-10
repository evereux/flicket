from pprint import PrettyPrinter

from application import db
from application.flicket.models.flicket_models import FlicketTicket, FlicketCategory, FlicketDepartment, FlicketStatus

# session = db.session
#
statii = FlicketStatus.query
departments = FlicketDepartment.query

pp = PrettyPrinter(indent=4)


def count_department_tickets(department, status):
    query = FlicketTicket.query.join(FlicketCategory).join(FlicketStatus).join(FlicketDepartment).filter(
        FlicketDepartment.department == department).filter(FlicketStatus.status == status)

    return query.count()


graph_dicts = []

for department in departments:

    graph_title = department.department
    graph_labels = []
    graph_values = []
    for status in statii:
        graph_labels.append(status.status)
        graph_values.append(count_department_tickets(graph_title, status.status))

    graph_dicts.append(
        dict(
            data=[
                dict(
                    labels=graph_labels,
                    values=graph_values,
                    type='pie'
                )
            ],
            layout=dict(
                title=graph_title
            )
        )
    )

pp.pprint(graph_dicts)
