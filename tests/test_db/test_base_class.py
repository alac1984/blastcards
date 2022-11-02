import pytest

from db.base_class import Base


@pytest.mark.unit
def test_base_class_instantiation():
    base = Base()
    assert base is not None


@pytest.mark.unit
def test_base_class_tablename():
    base = Base()
    assert base.__tablename__ == "tb_base"
