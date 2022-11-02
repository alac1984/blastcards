import pytest

from core.hashing import Hasher


@pytest.mark.unit
def test_hasher_verify_password():
    # Default passlib bcrypt cost factor is 12
    # Hash generated at https://bcrypt.online/?plain_text=senhapadrao&cost_factor=12
    assert Hasher.verify_password(
        "senhapadrao", "$2y$12$yGSZDO8K8btA3oktl.1u8ukQ7FonIfzItj9hku5W9cbu8lT1FhpFi"
    )


@pytest.mark.unit
def test_hasher_get_password_hash():
    hashed_password = Hasher.get_password_hash("senhapadrao")
    assert Hasher.verify_password("senhapadrao", hashed_password)
