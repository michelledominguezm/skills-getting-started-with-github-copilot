## Plan: Add backend FastAPI tests in tests directory

TL;DR - Create a new top-level `tests/` folder and add pytest-based FastAPI endpoint tests for the backend API in `src/app.py`.

**Steps**
1. Create a new directory `tests/` at the repository root.
2. Add a new test file `tests/test_app.py`.
3. In `tests/test_app.py`, import `TestClient` from `fastapi.testclient` and `app` from `src.app`.
4. Add an `autouse` fixture that deep copies and restores `src.app.activities` before/after each test so mutable in-memory state does not leak across tests.
5. Add tests covering:
   - GET `/activities` returns expected activity structure and participant list.
   - POST `/activities/{activity_name}/signup` registers a new participant and updates activity data.
   - DELETE `/activities/{activity_name}/participants` removes an existing participant.
   - DELETE with a missing participant returns 404.
6. Structure each test using the AAA pattern: Arrange test data and client, Act via API request, Assert on response and state.
7. Optionally update `requirements.txt` to include `pytest` if the environment does not already install it.

**Relevant files**
- `/workspaces/skills-getting-started-with-github-copilot/src/app.py` — backend endpoints to test
- `/workspaces/skills-getting-started-with-github-copilot/pytest.ini` — existing pytest config
- `/workspaces/skills-getting-started-with-github-copilot/requirements.txt` — may need `pytest`

**Verification**
1. Run `pytest` from the repository root and confirm all new tests pass.
2. Confirm `tests/test_app.py` exists and is discovered by pytest.
3. Verify test isolation by ensuring repeated runs do not fail due to state leakage.

**Decisions**
- Use FastAPI's `TestClient` for backend API testing, since it is a standard and lightweight approach for this project.
- Keep tests separate from `src/` by placing them under the top-level `tests/` directory.
- Use a fixture to restore mutable in-memory activity data between tests.
