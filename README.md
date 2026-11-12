# EdgeStream AI

> **Ultra-Low-Resource Edge Computer Vision & Multimodal Event Engine.**  
> *Zero-GPU motion and activity analysis for streaming video feeds (phone cameras, RTSP, and embedded IoT).*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![Zero-Dependency](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)]()
[![Memory Usage](https://img.shields.io/badge/RAM-%3C15MB-brightgreen.svg)]()

---

## 🎯 Overview

Most computer vision pipelines require CUDA-accelerated hardware or heavy tensor dependencies (`torch`, `cv2`) exceeding several hundred megabytes. On low-power edge nodes (Raspberry Pi Zero, solar-powered agricultural gateways, budget smartphones), running these models leads to device overheating and battery drain.

**EdgeStream AI** is an ultra-lean computer vision framework written in standard Python. It uses grid subsampling, differential luminance analysis, and spatio-temporal clustering to detect events, intruder motion, and physical boundary crossings in under 5ms per frame on a single low-power CPU core.

---

## ⚡ Key Highlights

- **< 15 MB RAM Consumption**: Runs cleanly on embedded boards alongside other services.
- **Pure Standard Library**: No OpenCV or external wheel requirements.
- **Webhook Event Dispatching**: Dispatches JSON alerts instantly to Telegram, Webhooks, or local message brokers.
- **Drop-in Phone Camera Integration**: Works seamlessly with `phone-stream` feeds.

---

## 🚀 Usage

```bash
git clone https://github.com/abenih/edge-stream-ai.git
cd edge-stream-ai
./bin/edge-stream-ai simulate --threshold 0.12
```

---

## 📄 License
MIT License. Created by [Susan (Abenezer)](https://satiralabs.com) at SatiraLabs.
