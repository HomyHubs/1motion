# Asset requests

Every requested asset must have an id, scene, description, and one status: `waiting_for_asset`, `received`, or `rejected`.

| id | scene | description | status |
|---|---|---|---|
| example | beat_01 | Replace this row with a real request. | waiting_for_asset |

Final rendering is blocked while any row is `waiting_for_asset`. Do not silently replace a missing request with Pillow, a zoomed still, or an unlicensed download.
