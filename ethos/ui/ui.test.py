from helper_functions import resolve_recents

r = resolve_recents("../userfiles/recents.json")

for entry in r:
    print(f"{entry['song']} - {entry['artist']}")