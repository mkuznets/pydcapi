# codegen

Generates `src/pydcapi/models` and `src/pydcapi/resources` from Adobe's discovery document and JSON schemas in `schemas/`.
It does not import `pydcapi`; the few lines of authentication it needs live in `download.py`.

```sh
uv sync --group codegen
uv run --group codegen python -m codegen generate   # schemas/ -> src/pydcapi/{models,resources}
uv run --group codegen python -m codegen download   # refresh schemas/ from the live API, needs IMS_SID
uv run --group codegen python -m codegen            # both
```

Run from the repository root. `download` reads `IMS_SID` (and optionally `AUX_SID`) from the environment or a `.env` file.

- `config.py` lists the schemas, resources and operations the generator skips, and the operations that return raw bytes.
- `patches.py` holds hand fixes applied to the schemas at generation time; upstream schemas are never edited.
- `templates/` renders the resource classes and the `Client`/`Response` protocols.
- Generated files must never be edited by hand. CI regenerates them and fails if the result differs from what is committed.
