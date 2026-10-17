# Sources and claim boundaries

Read on 17 October 2026. Links are primary papers, specifications, official documentation, or firsthand engineering accounts. Living documentation is not an archived snapshot. No claim is made that the example ran on the website archive date.

## LiveKit turn detection

- Source: [LiveKit turn detection](https://livekit.com/blog/turn-detection-voice-agents-vad-endpointing-model-based-detection).
- Version/date: 2026-02-21.
- Read: VAD, endpointing, semantic completion and interruptions; guide body.
- Use and limits: These are distinct decisions; no default delay or vendor benchmark is adopted.

## LiveKit pipeline latency

- Source: [LiveKit pipeline latency](https://kb.livekit.io/articles/4490830410-how-can-i-reduce-latency-in-voice-pipeline-agents-using-stt-tts-and-llm).
- Version/date: Live documentation, retrieved 2026-10-17.
- Read: Full short knowledge-base article.
- Use and limits: Network placement can affect the route; vendor guidance is not an independent comparative benchmark.

## WebRTC statistics

- Source: [WebRTC statistics](https://www.w3.org/TR/webrtc-stats/#dom-rtcinboundrtpstreamstats-jitterbufferdelay).
- Version/date: Living specification, retrieved 2026-10-17.
- Read: RTCInboundRtpStreamStats: totalProcessingDelay, estimatedPlayoutTimestamp, jitterBufferDelay, jitterBufferEmittedCount.
- Use and limits: Cumulative residence divided by emitted samples is an average; our window-difference arithmetic is an inference, not a percentile or acoustic measurement.

## FireRedChat v1

- Source: [FireRedChat v1](https://arxiv.org/html/2509.06502v1).
- Version/date: 2025-09-08.
- Read: Architecture, turn controller, evaluation sections 3.1 to 3.3.
- Use and limits: Barge-in, end-of-turn and latency are evaluated separately. Hardware, internal models, datasets and measurement boundaries limit generalization. We did not run their models.

## Stivers et al.

- Source: [Stivers et al.](https://doi.org/10.1073/pnas.0903616106).
- Version/date: 2009-06-30 issue.
- Read: Abstract, response timing context, table 1 and discussion, original six-page paper via Cognition and Culture PDF mirror.
- Use and limits: Ten-language question-response study; no universal voice-product latency target follows from it.

