# Oikonomia Hardware Acceleration Benchmarks (AWS F2 Substrate)

Automated synthetic stress harness and empirical audit telemetry for the Oikonomia FPGA appliance deployed on AWS EC2 `f2.6xlarge` (Xilinx UltraScale+).

---

## 1. Verified Hardware Benchmarks

| Workload / Engine | Metric Verified | Substrate / Transport | Verification Status |
| :--- | :--- | :--- | :--- |
| **Quant / HFT Risk** | **240 ns P50** (380 ns P99.9) | Physical Xilinx UltraScale+ FPGA (`0000:34:00.0`) | Kernel Bypass Verified |
| **PCIe Bus Round-Trip** | **1.22 µs P50** (11 ns Tail Jitter) | Direct PCIe TLP Non-Posted Read (BAR2) | Hardware Bound Verified |
| **Throughput Line Rate** | **14.95M ops/sec** | 16 Pinned Hardware Channels (BAR2) | Saturated Line Rate Verified |
| **GenAI Inference** | **8,797x Speedup** at 32k tokens | 512-bit AXI4-Stream (`f2.6xlarge`) | Strict O(1) Memory Verified |
| **BioPharma Docking** | **0.762 ms** per spatial evaluation | 512-bit AXI-Stream direct to HBM | Zero OOM Crashes Verified |
| **Consequence Governance** | **84.0 ns** Preemption (21 cycles @ 250 MHz) | PCIe BAR0 MMIO (`sts_eval_aix_982347102934_okm`) | SEC 15c3-5 Audit Verified |

---

## 2. Zero-Touch VPC Reproduction (15-Minute Diligence)

The appliance is distributed as an immutable Golden AMI. Systems and infrastructure teams can reproduce these telemetry logs inside their own secure VPC without external data ingress.

### Step 1: Launch Appliance

```bash
aws ec2 run-instances \
  --region us-east-1 \
  --image-id ami-06e581f3a6d6c3e32 \
  --instance-type f2.6xlarge \
  --key-name your-ssh-key \
  --security-group-ids sg-xxxxxx \
  --subnet-id subnet-xxxxxx
```

### Step 2: Run Embedded Verification Suites

SSH into your target instance and execute the audit harnesses:

```bash
# 1. Audit bare-metal kernel bypass latency (240 ns P50 / 380 ns P99.9)
sudo ./test_quant_kernel_bypass

# 2. Audit SEC Rule 15c3-5 consequence governance & 84ns preemption
./oikonomia_test_matrix.sh

# 3. Audit O(1) LLM scaling at 32,768 tokens (8,797x divergence speedup)
python3 extreme_llm_scaling.py
```

---

## 3. Architecture & Interface Latency Tiers

| Interface Tier | Calling Mechanism | P50 (Median) | P90 | P99 (Tail) | Determinism / Jitter Profile |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Silicon MMIO Wire** | Direct PCIe TLP Non-Posted Read (BAR2) | 1.220 µs | 1.220 µs | 1.231 µs | 11 ns spread (Physical PCIe bound) |
| **Kernel-Bypass Core** | Direct Register Write Engine | 240 ns | 245 ns | 251 ns | Deterministic hardware gate |
| **In-Process Driver** | C-ABI Shared Object (`liboikonomia.so`) | 1.649 µs | 1.810 µs | 2.050 µs | 401 ns spread (Zero OS context switch) |
| **Zero-Copy Socket** | Raw Binary IPC (`/tmp/oikonomia.sock`) | 19.770 µs | 24.650 µs | 33.670 µs | 13.90 µs spread (Bypasses network stack) |
| **16-CH Saturated Line** | 16 Pinned Worker Threads (1.6M Ops) | 1.070 µs | 1.072 µs | 1.085 µs | 14.95M aggregate ops/sec saturation |

---

## 4. Institutional Diligence & Evaluation Keys

For complete register maps (BAR2 `0x50048102000–0x50048102f80`), AGFI IDs (`agfi-0ae6493e8ec0d01d9`), or to obtain a 14-day zero-cost software evaluation license, contact: `contact@oikonomia-platform.com`.
