# Photograph And Section Geometry

Use the selected approved reference and current private style profile. Do not redesign a resume to compensate for an editing-tool limitation. Inspect and repair the native source, then export; a PDF-only correction leaves the next edit broken.

## Photograph

- Separate the original image dimensions, the displayed frame and the crop/mask. A copied header can already contain a stretched photo. Check the source pixels rather than judging only the face thumbnail.
- Preserve image proportions. Either size the frame to the original ratio or use a proportional fill with an intentional crop matching the reference. Never independently stretch width and height to fill the frame. A square frame is valid only when the image is cropped rather than squeezed into it.
- In Pages, inspect Image > Edit Mask and the available proportional sizing controls. Change the frame/mask without scaling the face; retain the reference's head size, crop and alignment. Discover actual host controls rather than inventing an API or relying on fixed coordinates.
- For DOCX, resolve the drawing's image relationship to its actual media file. Compare pixel width/height with `wp:extent`, picture transform `a:xfrm/a:ext`, and crop `a:srcRect`. An uncropped portrait displayed at 1:1 is stretched. With cropping, compare the remaining image ratio, not the original alone; rotation and grouped transforms also need inspection. Keep outer and inner drawing extents consistent when repairing a Word-native source.
- For example, a 996 x 1280 uncropped source has width/height 0.778. Displaying it at 3 x 3 cm widens it by about 28.5%; at a retained 3 cm height, proportional width is about 2.334 cm. This is an example, not a required photo size. Prefer the approved reference crop.
- Re-render and inspect the face at useful zoom and the full header at normal scale. Check that photo resizing did not shift the name, role, icons or contact column.

## Main Section Banners

Treat Profile, Selected Highlights, Employment History and Additional Supporting Information as the same main-section style. Role/company headings are a different style.

1. Identify the actual representation: grouped shapes, text box, table or shaded paragraph. Inspect the parent and children independently. Grey rule, black label and label text are three geometry/style concerns, not one object to stretch indiscriminately.
2. For the approved page-edge design, the grey rule begins at the physical left page edge and runs across the page. The black label also starts at that edge but retains its narrower reference width; it is NOT a full-width black band. Body text retains its own side margins. Use current profile measurements; an older margin-aligned repair is superseded when the user approves page-edge banners.
3. In Pages, select the outer group when needed; inspect Arrange position, size, wrap and anchoring. If an inline group prevents positioning, the verified route on this host was Arrange > Stay on Page. Confirm page and wrap after conversion. Then adjust the grey child width and black-label position/size separately. Do not stretch the entire group and thereby scale typography or the label. Do not zero document margins to move a decorative object.
4. Give the label enough height for its complete text. Remove accidental internal trailing blank paragraphs where appropriate. Check descenders, last letters, duplicate label objects and hidden overlapping copies. Recheck in exported PDF, not just the editor selection outline.
5. A normal Word shaded paragraph occupies the text area: `left=0` means the body margin, not the physical page edge. Replacing just one banner with paragraph shading and a magic right indent does not reproduce a positioned template. For a Word-native layout, use consistent template-compatible positioned geometry and verify each section after rendering. Do not silently replace a Pages master with an imported DOCX rebuild.
6. Measure each banner independently on every page. Record rule x/width, label x/width/height and label font/size against the reference. Keep user-approved intentional page breaks. A correct Profile does not prove Employment History or Supporting Information correct.

## Text And Spacing Repairs

- Match the established role/body/section font hierarchy, including isolated final letters. Preserve intentional symbol fonts and blue chevrons. Do not copy arbitrary first-run formatting from another paragraph as proof that a reconstructed heading has the right style.
- Preserve user-adjusted job spacing. Do not globally delete blank paragraphs, clear all page breaks or apply keep-with-next to every paragraph; these operations can introduce fresh pagination defects. Target the exact boundary and verify adjacent pages.
- After reflow, do not address jobs by stale paragraph indexes. Locate unique text/structure, check expected match counts and reconcile the content diff. Preserve mixed runs and links when replacing text.
- Read the Pages table-cell inset warning in `native-pages.md` before modifying the Skills grid. A successful cell-value write can destroy both font and paragraph inset while text extraction still passes.
- If the render is correct but extracted words contain ligature substitutions, the verified recovery on this host was the native Pages Ligature > Use None setting followed by export and two-parser comparison. Apply only to the affected scope, preserve symbol styling and verify again; a fresh export alone is not proof of repair.

## Acceptance And Another Agent's Work

Inspect all rendered pages beside the approved reference at matching scale, plus enlarged header/banner crops. Check photo ratio/crop, complete title, every main banner, body grid, bullets/indents, job spacing, date alignment, breaks and duplicate objects. Source save/reopen and PDF export identity remain separate gates.

Heading substring checks, five pages, a minimum line count, file modification time and a clean font audit do not test photo proportions or background alignment. Do not relax text comparisons by stripping all punctuation merely to hide corruption. Record visual findings separately from machine findings and explain unresolved limitations.

When inspecting another active owner, copy the current source/PDF to task assets with timestamps/hashes, inspect those copies and leave the live source untouched. Identify which revision was reviewed. Update the installed skill without restarting the host or changing its model/permissions. A running agent must explicitly reread the updated entrypoint and relevant references; files on disk do not prove its current context refreshed. Do not message that owner without applicable user authorization.
