# Oikonomia Hardware Acceleration Benchmarks (AWS F2 Substrate)

Automated synthetic stress harness and empirical audit telemetry for the Oikonomia bare-metal FPGA appliance deployed on AWS EC2 `f2.6xlarge` (Xilinx UltraScale+).

---

## 1. Verified Hardware Benchmarks

Telemetry recorded directly from physical Xilinx UltraScale+ silicon (`0000:34:00.0`) under single-tenant PCIe isolation:

| Workload / Engine | Metric Verified | Substrate / Transport Layer | Verification Status |
| :--- | :--- | :--- | :--- |
| **Quant / HFT Risk Gate** | **170 ns P50** (289 ns P99 \| 380 ns P99.9) | Physical PCIe BAR0 (`0x1d0f:0xf010`) | Kernel Bypass Verified |
| **Direct Bus MMIO Write** | **164.50 ns** per posted write | PCIe Gen3 x16 Root Complex (`resource0`) | Zero OS Jitter Verified |
| **Consequence Governance** | **84.0 ns Preemption** (21 cycles @ 250 MHz) | Hardware Drop Shunt (`agfi-037dec8eb7fe5504d`) | SEC 15c3-5 Audit Verified |
| **Monotonic Anti-Replay** | **401 Unauthorized** on stale epoch | Stateful Hardware Nonce Register | Anti-Replay Verified |
| **TOCTOU Mutation Shunt** | **403 Forbidden** (84 ns circuit break) | Hardware SHA-256 Digest Comparator | Zero Packet Leak Verified |
| **Bilateral Netting Engine** | **1.12 µs** (Variance: 0.0) | Deterministic Equilibrium Operator | Real-Time Clearing Verified |
| **Zero-Copy DMA Voxel Screen** | **102.22 µs** on 4,096-byte coordinate blocks | 512-bit AXI4-Stream DMA (`agfi-0b55f06c15a385187`) | Zero OOM Crashes Verified |
| **GenAI Sequence Reduction** | **28.6 ms @ 32k tokens** (0.0 MB KV-Cache) | Fixed-Topology Systolic Manifold (`0xf001`) | Strict O(1) Memory Verified |
| **Thermal & Power Envelope** | **9 Watts steady-state** (`Vccint`) | Physical Internal Voltage Rail Sensor | Ultra-Low Power Verified |
| **16-CH Saturated Line Rate** | **14.95M ops/sec** across 16 pinned channels | Multi-Channel Hardware Interconnect (BAR2) | Line Rate Verified |

---

## 2. Zero-Touch VPC Reproduction (15-Minute Diligence)

The appliance is distributed as an immutable Golden AMI. Systems and quantitative infrastructure teams can reproduce these telemetry logs inside their own secure AWS VPC without external network dependencies:

### Step 1: Launch Appliance
```bash
aws ec2 run-instances \
  --region us-east-1 \
  --image-id ami-01d1583512f1afb46 \
  --instance-type f2.6xlarge \
  --key-name your-ssh-key \
  --security-group-ids sg-xxxxxx \
  --subnet-id subnet-xxxxxx
```

### Step 2: Run Embedded Verification Suites
SSH into your target instance and execute the native compiled C++ audit harnesses:

```bash
# 1. Audit bare-metal kernel bypass latency (170 ns P50 / 84ns drop shunt)
sudo taskset -c 2 ./test_quant_kernel_bypass

# 2. Audit SEC Rule 15c3-5 consequence governance & anti-replay matrix
./oikonomia_test_matrix.sh

# 3. Audit raw PCIe BAR0 physical bus MMIO write/read distribution
sudo taskset -c 2 ./unified_silicon_audit

# 4. Audit zero-copy direct memory access (102.2µs on 4KB voxel streaming)
sudo taskset -c 2 ./zero_copy_silicon
```

---

## 3. Architecture & Interface Latency Tiers

| Interface Tier | Transport & Calling Mechanism | P50 (Median) | P90 | P99 (Tail) | Determinism / Jitter Profile |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Kernel-Bypass Core** | Direct Register Write Engine (`test_quant`) | **170 ns** | 245 ns | 289 ns | Deterministic hardware gate |
| **Posted Bus Write** | Direct PCIe Root Complex (`unified_audit`) | **164.50 ns** | 164.50 ns | 165.10 ns | 0% OS thread contention |
| **Silicon MMIO Wire** | Direct PCIe TLP Non-Posted Read (BAR2) | **970 ns** | 1.020 µs | 1.091 µs | Physical bus turnaround bound |
| **In-Process Driver** | C-ABI Shared Object (`liboikonomia.so`) | **1.649 µs** | 1.810 µs | 2.050 µs | Zero OS context switch |
| **Zero-Copy Socket** | Raw Binary IPC (`/tmp/oikonomia.sock`) | **19.770 µs** | 24.650 µs | 33.670 µs | 13.90 µs spread (Bypasses network stack) |
| **16-CH Saturated Line** | 16 Pinned Worker Threads (1.6M Ops) | **1.070 µs** | 1.072 µs | 1.085 µs | 14.95M aggregate ops/sec saturation |

---

## 4. Institutional Diligence & Evaluation Keys

For complete register maps (`0x50048102000-0x50048102f80`), target AGFI IDs, or to stage a dedicated single-tenant enclave trial inside your AWS account:

* **Golden AMI Artifact:** `ami-01d1583512f1afb46` (`Oikonomia-F2-Golden-Silicon-v1.0`, us-east-1)
* **Quant Risk Substrate (`0xf010`):** `agfi-037dec8eb7fe5504d`
* **BioPharma Voxel Substrate (`0xf000`):** `agfi-0b55f06c15a385187`
* **Sub-Linear AI Substrate (`0xf001`):** `agfi-06f1443d0618b212e`
* **Baseline Diligence AGFI:** `agfi-0ae6493e8ec0d01d9`
* **Direct Point of Contact:** contact@oikonomia-platform.com
