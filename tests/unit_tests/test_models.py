import pytest

from app.models.models import Salary, User

parametrize = pytest.mark.parametrize(
    "model, attrs",
    (
        (User, ("id", "salary")),
        (Salary, ("id", "value", "inc_date", "user_id", "user")),
    ),
)


@parametrize
def test_model_attr(model, attrs) -> None:
    for attr_name in attrs:
        assert hasattr(model, attr_name)


@parametrize
def test_model_repr(model, attrs) -> None:
    representation = repr(model())
    for attr_name in attrs:
        assert representation.find(attr_name) != -1


@parametrize
def test_asdict(model, attrs) -> None:
    obj = model()._asdict()
    assert isinstance(obj, dict)
    relation_fields = ("salary", "user")
    for attr in attrs:
        if attr in relation_fields:
            # relation fields shoud not be in the dict:
            with pytest.raises(KeyError):
                obj[attr]
        else:
            obj[attr]
