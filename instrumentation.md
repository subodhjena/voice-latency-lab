# Instrumentation worksheet

For each event, record the observer and clock domain before computing intervals.

| Event | Proposed observer | Important limitation |
| --- | --- | --- |
| User speech end | Controlled capture or labeled client audio | Silence detection is an estimate, not known intent |
| Turn committed | Turn controller | May follow earlier transcription work |
| Model start / first token | Agent process | Excludes earlier waits |
| Text ready / first audio | TTS caller | Text buffering is separate from provider startup |
| Audio received | Client | Does not establish playback |
| Playback started / stopped | Client renderer, validated against capture | Device and acoustic delay may remain |
| Useful playback | Labeled response segment | Acknowledgment and task answer are different |
| Barge-in | Labeled user speech onset | False interruptions need separate review |

Link session, turn, response, chunk sequence, and cancellation identifiers. Keep
raw local timestamps and document any cross-clock mapping with its error bounds.
The analyzer rejects clock-label mismatches but cannot prove that normalization
was performed correctly.

Retain timeouts, missing playback, failed turns, and abandoned turns as explicit
outcomes. Do not encode a missing duration as zero. For a live system, analyze
each response stream rather than collapsing multiple interruptions into one pair.

Record endpoint and interruption accuracy alongside time. Review pauses,
self-corrections, long numbers, background speech, device routes, tool calls, and
network conditions with the actual intended users. The fixtures here do not
measure any of those populations.
