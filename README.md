# A voice assistant has more than one latency problem

Analyze synthetic voice event timelines without confusing model startup, turn commitment, useful playback, and interruption. Includes an interval jitter-buffer calculation.

This is the runnable companion to [the article](https://subodhjena.com/blog/a-voice-assistant-has-more-than-one-latency-problem). Website MDX is the canonical article; [article.md](article.md) is a deliberate GitHub-readable snapshot. Code and fixtures are canonical here. Research and the examples were prepared on 17 October 2026; the website uses the author-approved archive spacing.

## Reproduce

Python 3.11 or later, standard library only. No API keys, packages, or network access. Verified locally on Python 3.14.5.

```bash
python3 -m unittest -v
python3 latency.py
```

Compare stdout with [sample-output.txt](sample-output.txt). The tests exercise failure paths as well as the expected result. All fixtures are synthetic.

## Scope and limits

The analyzer assumes a normalized monotonic clock shared by fixture events. It does not synchronize clocks, capture audio, transcribe speech, call models, or measure real users. Each trace has one response and one interruption. A playback boundary is a synthetic harness observation, not an acoustic measurement. The jitter helper requires snapshots from the same inbound RTP stats object; changed objects and decreasing counters invalidate the window.

## Supporting material

- [Source notes](references.md), with versions and claim boundaries.
- [Recorded output](sample-output.txt).
- [Article snapshot](article.md).

The tests validate this demonstration, not production readiness. Source papers and documentation remain under their original licenses. Original example code and article text in this repository use the [MIT license](LICENSE).
