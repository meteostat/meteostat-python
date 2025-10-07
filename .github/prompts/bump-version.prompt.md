---
mode: 'agent'
description: 'Bump version prompt'
---

Bump the version of the Meteostat Python library.

New version number: ${input:version:Specify the new version number (e.g., 1.2.3)}

Update the following files:

- meteostat/__init__.py
- setup.py