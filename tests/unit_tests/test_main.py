"""
async def test_lifespan(monkeypatch, mock_async_session) -> None:
    from tests.fixtures.db_config import test_engine
    from app import main
    monkeypatch.setattr(main, "engine", test_engine)
    async with lifespan("") as user:  # override_get_async_session
        # assert user is not None
        check_user(user)
"""
