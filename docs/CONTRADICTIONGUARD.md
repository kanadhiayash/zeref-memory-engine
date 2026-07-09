# ContradictionGuard

ContradictionGuard prevents Zeref from silently storing conflicting active memory
cards.

It currently treats active cards with the same normalized title and different
claims as high-severity conflicts. High-severity conflicts block guarded writes
until the user resolves or supersedes the older card.

Commands:

```bash
zeref contradictions scan memory/
zeref contradictions list
zeref contradictions show conflict_<id>
zeref contradictions resolve conflict_<id> --winner mem_2026_07_09_0001 --reason "User confirmed."
zeref contradictions archive conflict_<id>
```

Open conflicts are mirrored to `memory/CONFLICTS.md` for human arbitration.
