# Hexagonal Pyramid Projection CAD Submission

This repository contains a first-angle Engineering Graphics projection for a hexagonal pyramid with base side 25 mm and axis length 50 mm. The final position keeps one base edge on H.P., inclines the axis at 30° to H.P., and keeps the axis parallel to V.P.

## Output files

- `projection.dxf` — primary downloadable AutoCAD-compatible DXF artifact in millimetres.
- `hexagonal_pyramid_projection.dxf` — descriptive-name copy of the same AutoCAD-compatible DXF drawing in millimetres.
- `hexagonal_pyramid_projection.lsp` — AutoLISP routine that recreates the drawing geometry, layers, labels, and dimensions.
- `hexagonal_pyramid_projection.scr` — AutoCAD script that recreates the drawing geometry, layers, labels, and dimensions.
- `verification.json` — Mathematical verification of side length, axis length, axis inclination, axis parallelism to V.P., projected vertex coordinates, and visible/hidden edge sets.
- `generate_projection.py` — Deterministic generator used to create the drawing and verification files.

Native DWG creation is not included because this environment does not provide a licensed DWG writer. The DXF is intended to open directly in AutoCAD and can be saved as DWG from AutoCAD.

## Construction notes

The simple position is selected with the pyramid axis perpendicular to H.P. and one hexagonal base edge on H.P. The solid is then tilted about that same base edge using the change-of-position method. The hinge edge is perpendicular to V.P.; therefore, during tilting, the axis moves in a plane parallel to V.P. and remains parallel to V.P. in the final position.

The final drawing includes only the final front view and final top view, separated by the X-Y reference line in first-angle projection.
