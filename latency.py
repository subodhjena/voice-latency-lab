"""Inspect synthetic cascade traces. No provider calls or real audio capture."""
import json
import math
from pathlib import Path


PAIRS = {
    "endpoint_ms": ("user_end", "turn_committed"),
    "llm_ttft_ms": ("llm_start", "first_token"),
    "tts_first_audio_ms": ("tts_text_ready", "tts_first_audio"),
    "client_queue_ms": ("audio_received", "playback_started"),
    "first_playback_ms": ("user_end", "playback_started"),
    "useful_playback_ms": ("user_end", "useful_playback"),
    "stop_ms": ("barge_in", "playback_stopped"),
}


def measure(trace):
    """All events must already use one normalized, monotonic clock domain.

    End-to-end intervals are direct boundary differences, never sums of spans.
    The synthetic harness observes user_end and playback; a server cannot
    independently observe either acoustic boundary in a real client.
    """
    events = trace["events"]
    times = {}
    clock = None
    previous = -1
    for event in events:
        name, timestamp, domain = event["name"], event["ms"], event["clock"]
        if not isinstance(timestamp, (int, float)) or isinstance(timestamp, bool):
            raise ValueError("Timestamp must be a finite number")
        if not math.isfinite(timestamp) or timestamp < previous or timestamp < 0:
            raise ValueError("Timestamps must be finite, nonnegative, and ordered")
        if not domain or (clock is not None and domain != clock):
            raise ValueError("Normalize clocks before analysis")
        if name in times:
            raise ValueError(f"Duplicate event: {name}")
        clock, previous = domain, timestamp
        times[name] = timestamp
    metrics = {}
    for metric, (start, end) in PAIRS.items():
        if start not in times or end not in times:
            raise ValueError(f"Missing boundary for {metric}")
        duration = times[end] - times[start]
        if duration < 0:
            raise ValueError(f"Reversed boundary for {metric}")
        metrics[metric] = duration
    # These constraints describe this fixture's output stream, not all architectures.
    for start, end in (("first_token", "tts_text_ready"),
                       ("tts_first_audio", "audio_received"),
                       ("playback_started", "useful_playback"),
                       ("playback_started", "barge_in")):
        if times[end] < times[start]:
            raise ValueError(f"Reversed output boundary: {start}, {end}")
    return metrics


def jitter_window_ms(before, after):
    """Mean residence time of samples emitted in this window, not a percentile.

    Snapshots must refer to the SAME inbound RTP stats object. Delay is the
    cumulative jitterBufferDelay in seconds, count is jitterBufferEmittedCount.
    """
    if before["id"] != after["id"]:
        raise ValueError("Stats object changed")
    for snapshot in (before, after):
        if any(not math.isfinite(snapshot[key]) or snapshot[key] < 0
               for key in ("delay_s", "count")):
            raise ValueError("Invalid cumulative counters")
    delay = after["delay_s"] - before["delay_s"]
    count = after["count"] - before["count"]
    if delay < 0 or count < 0:
        raise ValueError("Counters reset; start a new window")
    if count == 0:
        return None
    return 1000 * delay / count


if __name__ == "__main__":
    traces = json.loads(Path(__file__).with_name("traces.json").read_text())
    print("Synthetic timelines, milliseconds. Not a provider benchmark.")
    for trace in traces:
        print(f"\n{trace['id']}")
        for name, value in measure(trace).items():
            print(f"  {name}: {value:g}")
