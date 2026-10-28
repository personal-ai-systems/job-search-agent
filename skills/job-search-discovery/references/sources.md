# Reading Job Boards Without A Browser

Prefer structured public endpoints. Availability and schema must be checked;
a documented endpoint does not prove a particular board slug works.

## Greenhouse

```
https://boards-api.greenhouse.io/v1/boards/{slug}/jobs
```

Returns `{"jobs": [...]}`. Each job has `title`, `absolute_url`, and `location.name` (a human string such as `Sydney, Australia` or `London, UK; Remote-Friendly, United States`). Location strings are frequently multi-valued with `;` or `|` separators - split them before matching.

## Ashby

```
https://api.ashbyhq.com/posting-api/job-board/{slug}
```

Returns `{"jobs": [...]}`. Each job has `title`, `jobUrl`, and a flat `location` string. Ashby location strings sometimes encode region rather than city (`Remote - APAC`, `Remote / APAC`, `Remote (US)`), so match on region tokens as well as city names.

## Other ATS worth trying

- **Lever**: `https://api.lever.co/v0/postings/{slug}?mode=json` - returns an array with `text`, `categories.location`, `hostedUrl`.
- **Workable**: `https://apply.workable.com/api/v1/widget/accounts/{slug}` - varies by tenant.
- **Recruitee / Teamtailor / Personio**: usually no clean public JSON; fall back to the careers page.

A company missing from Greenhouse and Ashby has not stopped hiring. It has a different ATS or a different slug. Try the two or three obvious slug spellings, then the company's own careers page, then record it as unresolved rather than as "no openings".

## What The Endpoints Do Not Give You

- Salary when omitted. Inspect compensation fields when present; do not infer
  omitted values from market rates.
- Whether the role accepts an Australian-based candidate when the location says `Remote`.
- Whether the posting is still open despite being listed. Ashby and Greenhouse both list jobs that reject on submit.
- Seniority in a comparable form across companies.

Treat all four as unknowns to be resolved by reading the actual posting, and say so rather than flattening them into an assumption.

## Real Failure Modes Seen

- **Slug mismatch.** `modal-labs`, `modallabs` and `modal` all failed for Modal; the board exists under none of them. Record and move on rather than retrying variations indefinitely.
- **Region token instead of city.** `Remote - APAC` will not match a `Sydney|Melbourne|Australia` regex. Match region tokens too.
- **Empty board is not a blocked board.** `{"jobs": []}` from a valid slug means the board exists and is empty. A 404 or a non-JSON body means unreadable. These are different facts and must be reported differently.
- **Aggregators duplicate employer boards.** SEEK and LinkedIn will show the same requisition as the employer's Ashby page, often with a different title format. Deduplicate on the employer's own requisition where it exists.

## Rate And Politeness

Respect provider terms, attribution and limits. The catalogue bounds frequency;
it does not grant unlimited crawl permission. Identify the reader honestly;
never change identity to bypass a 403. Record failures with increasing backoff.
