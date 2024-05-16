import pytest

from app.models.models import Salary, User

parametrize = pytest.mark.parametrize(
    "model, attrs",
    (
        (User, ["salary"]),
        (Salary, ["id", "value", "inc_date", "user_id", "user"]),
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
    d = model()._asdict()
    assert isinstance(d, dict)
    relation_fields = ("salary", "user")
    for attr_name in attrs:
        if attr_name in relation_fields:
            # relation fields shoud not be in the dict:
            with pytest.raises(KeyError):
                d[attr_name]
        else:
            d[attr_name]


# attr_name, attr_type
ID = ("id", "UUID")
VALUE = ("value", "NUMERIC(8, 2)")
INC_DATE = ("inc_date", "DATE")
USER_ID = ("user_id", "CHAR(36)")


@pytest.mark.parametrize("model, attrs", ((Salary, [ID, VALUE, INC_DATE, USER_ID]),))
def test_model_columns_types(model, attrs) -> None:
    for attr_name, col_type in attrs:
        col = getattr(model, attr_name)
        assert str(col.type) == col_type, str(col)
