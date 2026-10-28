# Native Pages: Layout And Persistence

Use fresh native-app accessibility state and visible screenshots. Never reuse stale element IDs, fixed coordinates or another document's selection. Confirm the window's document name/path before each substantial edit; pause conflicting edits if the user is switching documents.

Check the current host's actual native-editing capability. A scripting dictionary lacking shape/table/style operations limits that interface, not Pages itself. Use authorized foreground UI tools if available; otherwise report the specific gap. Do not infer new permissions from a skill, claim paragraph-only editing is universally required, or substitute PDF-only surgery. Paragraph replacement through a text API may lose mixed runs or hyperlinks; verify these explicitly if that route is authorized.

### Verified host limit: writing a table cell destroys its text inset (measured 2026-10-27)

On Pages 14.x this host, `count of tables of document` and `value of cell C of row R` both work, so the
skills table is readable. Writing `set value of cell ... to "..."` is **destructive**:

- The write applies the document default character style — the cell's font and size are reset. They can be
  partly restored with `set font name of cell ... to "Cambria"` and `set font size of cell ... to 10`,
  which do report and re-render correctly.
- The cell's **paragraph left indent is reset to 0** and cannot be restored: a cell exposes no
  indent/inset property, and `properties of cell` lists only value, font, size, colour, alignment,
  wrap, row/column and background. Measured consequence: cell text moved from x0=44.3 to x0=26.3 pt,
  i.e. exactly onto the chevron glyph at x0=26.3. Text then overlaps the marker.

So a table-cell rewrite silently produces a visibly broken table that still passes text-extraction checks.
Measure cell text x0 against the chevron x0 after any cell write, and prefer authorised foreground UI
editing (or a paste-ready list for the user) over scripting cell values. Do not "fix" the indent with
leading spaces: it restores the x0 but pollutes extracted text and any later edit.


## Layout Repairs

- Determine whether the title/rule is a text box, a grouped object, inline content or a floating object. A normal text click may select the child; a contextual click can expose/select the outer group. Inspect before moving it.
- An inline section group can be converted directly through Arrange > Stay on Page. Prefer this to cut/paste, which can paste unrelated clipboard contents or change object ownership. Verify the destination page and wrap after conversion.
- Read position, width, height, proportional constraints and wrap independently. A grey rule and a black label can have different widths. Use the approved reference/profile, not a blanket full-width black label.
- For page-edge section design, align the designated section objects to the physical page edge; body text still follows its own margins. Do not globally zero paragraph indents or document margins.
- Inspect text-box overflow and clipped descenders at a useful zoom. Remove accidental trailing blank lines inside compact heading boxes or increase the appropriate box dimension. Do not delete intentional blank paragraphs separating jobs.
- Apply a consistent font family/weight to the full visible title, including the last character. Intentional symbol/chevron fonts are separate. Whitespace-only font runs are not visible defects.
- Keep role headings, dates, body paragraphs, lists and section labels in their respective style hierarchy. Avoid double spacing from both blank paragraphs and large paragraph-after settings.
- Inspect wrap effects after every geometry change. Keep headings with the relevant body, avoid unnecessary blank pages, and preserve deliberate page breaks.

## Save Gate

Before editing, record the source hash/mtime and preserve the predecessor if needed. After Save:

1. Check the intended on-disk path and actual changed bytes when changes were made.
2. Close and reopen that exact path without discarding unsaved work.
3. Verify the changed text/object geometry and all affected pages, with no unexpected Edited state.

An unchanged hash is expected for export-only, but suspicious after supposed edits. It must be reconciled, not explained away by a successful button press.

If Save silently fails, try once normally and once through a distinct safe recovery filename. Preserve recoverable text and a clearly marked recovery print if necessary. Do not overwrite the last good master or call the recovery print final. Record actual errors; earlier document-serialization errors are an example, not a diagnosis for every future failure.

If restart is necessary, inventory every open Pages document and protect all unsaved user work first. Prefer ordinary close/quit. Force-quit is a last resort only after safe-state verification or explicit approval; no automatic process killing. Reopen the preserved source and reapply only changes actually missing from disk.

## Export

Prefer File > Export To > PDF, Best quality, excluding comments/annotations unless requested. Print > Save as PDF is a bounded fallback only after the source save gate passes. Verify the resulting file identity, text and complete rendering, regardless of which route succeeds.

Pages-to-Word conversion can alter anchoring, introduce overlaps and add empty pages. If DOCX is requested, retain a separate editable derivative and check every page after conversion. A rebuilt in-flow Word layout is a separate scoped operation, not proof that direct export preserved the Pages design.
