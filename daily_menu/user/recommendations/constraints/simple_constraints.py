from datetime import datetime

from user.recommendations.constraints.base_constraint import BaseConstraint


class TodayMenus(BaseConstraint):
    def filter(self, query):
        return query.filter(day=datetime.today())

