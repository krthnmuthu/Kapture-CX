# Part A Writeup

## Assumptions Made
- For language mismatch, I assumed Hindi should contain non-ASCII characters (Devanagari). This is simplistic but works for this dataset.
- Garbled text is detected by high ratio of non-letter characters (>30%). This might reject valid Hinglish with numbers/emojis, but it's a reasonable heuristic.
- Only the listed quality issues were injected and checked, but I added checks for all turns empty after cleaning.

## Hardest Issue to Detect
Language mismatch was hardest because it's subjective. I used a simple ASCII check, but a better way would be to use a language detection library like langdetect.

## Scaling to 100,000 Conversations
- Use pandas or Dask for data processing instead of loading all into memory.
- Parallelize cleaning with multiprocessing.
- For language detection, use a proper ML model or API.
- Add more robust validation, perhaps with regex for garbled text.
- Store data in a database or use streaming for large files.