# Example Public Source Catalogue

These are example endpoints, not promises of current availability, terms or
eligible work locations. Verify the provider's access rules/attribution. No
candidate data or authentication is sent by the collector. Change this private
copy deliberately; do not infer intent from the companies listed here.

| ID | Name | Adapter | URL | Lane | Cadence hours |
| --- | --- | --- | --- | --- | --- |
| openai | OpenAI | ashby | https://api.ashbyhq.com/posting-api/job-board/openai | personal-employment | 24 |
| anthropic | Anthropic | greenhouse | https://boards-api.greenhouse.io/v1/boards/anthropic/jobs?content=true | personal-employment | 24 |
| relevanceai | Relevance AI | ashby | https://api.ashbyhq.com/posting-api/job-board/relevanceai | personal-employment | 24 |
| openrouter | OpenRouter | ashby | https://api.ashbyhq.com/posting-api/job-board/openrouter | personal-employment | 24 |
| runpod | Runpod | ashby | https://api.ashbyhq.com/posting-api/job-board/runpod | personal-employment | 24 |
| cohere | Cohere | ashby | https://api.ashbyhq.com/posting-api/job-board/cohere | personal-employment | 24 |
| baseten | Baseten | ashby | https://api.ashbyhq.com/posting-api/job-board/baseten | personal-employment | 24 |
| e2b | E2B | ashby | https://api.ashbyhq.com/posting-api/job-board/e2b | personal-employment | 24 |
| remotive | Remotive | remotive | https://remotive.com/api/remote-jobs | personal-employment | 24 |
| remoteok | Remote OK | remoteok | https://remoteok.com/api | personal-employment | 24 |
| wwr | We Work Remotely | rss | https://weworkremotely.com/remote-jobs.rss | personal-employment | 24 |
| arbeitnow | Arbeitnow | arbeitnow | https://www.arbeitnow.com/api/job-board-api | personal-employment | 24 |
| freelancermap | Freelancermap | browser | https://www.freelancermap.de/projekte | personal-contract/company-project | 24 |
| malt | Malt | browser | https://www.malt.com/ | personal-contract/company-project | 168 |
| austender | AusTender | browser | https://www.tenders.gov.au/ | company-tender | 168 |
| buy-nsw | buy NSW | browser | https://buy.nsw.gov.au/opportunities | company-tender | 168 |

Browser rows require actual host inspection and their own coverage checkpoint;
the Python collector skips them. An HTTP-200 homepage is not an opportunity scan.
