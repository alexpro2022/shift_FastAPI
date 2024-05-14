"""
from .views import VacancyView, Vacancy
from app.core.dependencies import engine


admin = Admin(
    engine,
    "💾 База данных ",
)
admin.add_view(VacancyView(Vacancy))
"""
