from pathlib import Path
import json
root=Path(__file__).resolve().parent
sheet=json.loads((root/'authored-sheet-snapshot.json').read_text())
target=root/'beat_sheet.regenerated.json'
target.write_text(json.dumps(sheet,indent=2)+'\n')
print(target)
