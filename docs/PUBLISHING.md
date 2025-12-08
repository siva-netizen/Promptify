# How to Publish Promptify

## Prerequisites
*   **PyPI Account**: Register at [pypi.org](https://pypi.org/).
*   **Build Tools**: Install `build` and `twine`.

```bash
pip install build twine
```

## 1. Build the Package
Generate the distribution files (source archive and wheel) in the `dist/` directory.

```bash
# Clean previous builds
rm -rf dist/

# Build
python -m build
```

## 2. Test Locally
Unzip and check the build, or install it locally.

```bash
pip install dist/promptify-0.1.0-py3-none-any.whl
```
Run `promptify --help` to verify.

## 3. Publish to PyPI
Upload the package to the Python Package Index.

```bash
python -m twine upload dist/*
```
You will be prompted for your API token (username: `__token__`).

## 4. Install from PyPI
Once published, anyone can install it via:

```bash
pip install promptify
```

## Development Install (Editable)
For local development where changes are reflected immediately:

```bash
pip install -e .
```
