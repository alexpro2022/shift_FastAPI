"""
from app.models.models import Vacancy


class VacancyView(ModelView):
    model = Vacancy
    fields = (
        "id",
        "title",
        TextAreaField(
            "description",
        ),
    )
"""
