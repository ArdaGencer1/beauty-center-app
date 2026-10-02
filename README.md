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

## Validation
Run the lightweight ARC geometry check before loading the script:

```sh
python tests/validate_plant3d_arcs.py
```

The validator scans each direct three-point `_.ARC` command and fails if the
three points are malformed or collinear.

## Notes and limitations
- The script uses basic AutoCAD commands (`LINE`, `ARC`, `CIRCLE`, `TEXT`, `PLINE`),
  so you can edit coordinates and labels as needed.
- This is a clean starter template, not a standards-validated instrument diagram.
- The generated objects are basic AutoCAD entities, not intelligent Plant 3D P&ID
  components, line groups, tags, or database-linked equipment.
- The validator is a static check for the three-point ARC definitions only; it does
  not replace executing the script in the target AutoCAD Plant 3D version and
  drawing environment.
- Script behavior can still depend on active AutoCAD settings such as the current
  text style and command prompting, so test it in a clean drawing/template before
  using it as a production starting point.
