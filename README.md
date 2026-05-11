# beauty-center-app

This repository now includes an AutoCAD Plant 3D script template that draws an
approximate process flow / P&ID-style diagram matching the user-provided sketch.

## File
- `plant3d_pfd_template.scr`

## How to run in AutoCAD Plant 3D
1. Open a drawing in AutoCAD Plant 3D.
2. Type `SCRIPT` in the command line.
3. Select `plant3d_pfd_template.scr`.
4. The geometry and text labels will be drawn automatically.

## Notes
- The script uses basic AutoCAD commands (`LINE`, `ARC`, `CIRCLE`, `TEXT`, `PLINE`),
  so you can edit coordinates and labels as needed.
- This is a clean starter template, not a standards-validated instrument diagram.
