# NOVA API

A small FastAPI service with MongoDB-backed user registration and login.

## Setup

1. Install Python 3.10 or newer and MongoDB.
2. From the project root, install the app and test dependencies:

   ```powershell
   python -m pip install -e ".[test]"
   ```

3. Start MongoDB locally, then run the API:

   ```powershell
   uvicorn app.main:app --app-dir src --reload
   ```

   Set `MONGODB_URI` if MongoDB is running at a different address. The default is
   `mongodb://localhost:27017/`.

4. Open <http://127.0.0.1:8000/docs> to try the API. Both `/register` and
   `/login` accept `username` and `password` as form fields.

## Run tests

```powershell
python -m pytest
```

## Git workflow

Use this workflow for changes in this repository. Replace `<short-description>`
with a brief, lowercase, hyphen-separated summary.

### 1. Create a branch

Start from an up-to-date `master` branch and create a focused branch:

```powershell
git switch master
git pull origin master
git switch -c <type>/<short-description>
```

Examples: `feature/password-reset`, `fix/login-validation`,
`docs/api-setup`.

### 2. Commit changes

Write commit messages using the Conventional Commits format:

```text
<type>(optional-scope): <imperative summary>
```

Common types:

- `feat`: add user-facing functionality
- `fix`: correct a bug
- `docs`: change documentation
- `test`: add or update tests
- `refactor`: restructure code without changing behavior
- `chore`: maintenance or tooling changes

Examples:

```text
feat(auth): add password reset endpoint
fix(login): reject invalid credentials
docs: explain local MongoDB setup
```

Keep commits focused. Before committing, run the relevant checks:

```powershell
python -m pytest
python -m ruff check src tests
git diff --check
```

### 3. Open a pull request

Push your branch and open a pull request with `master` as the base:

```powershell
git push -u origin <type>/<short-description>
```

In the pull request:

1. Use a clear title and describe what changed and why.
2. Include test results and link related issues, if any.
3. Request review from the appropriate teammate.
4. Address feedback with follow-up commits and push them to the same branch.
5. Wait for required approvals and automated checks to pass.

### 4. Resolve merge conflicts

Update your feature branch with the latest `master`:

```powershell
git fetch origin
git switch <type>/<short-description>
git merge origin/master
```

If Git reports conflicts:

1. Check `git status` to find conflicted files.
2. Open each file and choose or combine the intended changes. Remove conflict
   markers (`<<<<<<<`, `=======`, and `>>>>>>>`) and check the surrounding code.
3. Stage the resolved files and verify there are no remaining conflicts:

   ```powershell
   git add <resolved-file>
   git diff --name-only --diff-filter=U
   git diff --cached --check
   ```

   The first command stages the resolution; the second should print no paths.
4. Run tests and lint checks, then finish the merge and push the branch:

   ```powershell
   python -m pytest
   python -m ruff check src tests
   git commit
   git push
   ```

Git will provide a merge commit message when `git commit` is run. If the merge
was started by mistake, preserve any work you need before using
`git merge --abort` to cancel it.

### 5. Merge and clean up

After review and required checks pass, merge the pull request using the
repository's chosen merge method. Delete the feature branch when it is no longer
needed, then update your local `master`:

```powershell
git switch master
git pull origin master
```
