# Compiled Inspection Reports — P-101B (Boiler Feed Pump B)

**Asset Tag:** P-101B
**Service:** Boiler Feed Water — Deaerator to HP Steam Generator
**Type:** Multistage centrifugal boiler feed water pump, horizontal, 6-stage, between-bearings, API 610 type BB4
**Rated (BEP) Flow:** 240 m³/h
**Minimum Continuous Stable Flow:** 72 m³/h (30% of BEP)
**Rated Differential Head:** 1,180 m
**Driver:** 900 kW, 2-pole squirrel cage induction motor, 2,970 rpm nominal
**Mechanical Seal Arrangement:** API 682 Plan 23 (recirculation from seal chamber through a seal cooler and back to the seal chamber)
**Bearings:** Radial — hydrodynamic sleeve; Thrust — tilting pad, Kingsbury type
**Associated Instrumentation:** TE-101B (inboard/outboard bearing temperature), VE-101B (casing/shaft vibration), PT-101 (discharge pressure), FT-101 (flow), PDI-S14 (suction strainer differential pressure), MOV-118 (minimum-flow recirculation valve)
**Suction Line Protection:** Suction Strainer S-14
**Parallel / Related Equipment (reference only):** P-101A (parallel BFW pump), P-102 (condensate transfer), E-301 (LP feedwater heater), V-201 (knockout drum)

**Document compiled:** 2026-07-21
**Compiled by:** Rotating Equipment / Reliability Section

---

## 1. STATUTORY INSPECTION STATUS — ACTION OVERDUE

Periodic inspection of rotating machinery in critical boiler feed water service is governed by the site's OISD-based mechanical integrity programme. Under **OISD-STD-128 (Inspection of Unfired Pressure Vessels and Rotating Equipment), Clause 6.4 — Periodic Inspection of Pumps in Critical Service**, and as carried into the site inspection schedule under **OISD-GDN-206 Clause 5.2** for hydrocarbon-and-utility critical rotating machinery, pumps in this category require a **documented statutory periodic inspection at intervals not exceeding 12 months**. The inspection scope, paraphrased from the standard, requires: verification of casing and pressure-boundary integrity, foundation and holding-down bolt condition, coupling guard and guarding compliance, seal and seal-support system integrity, verification of protective trips and alarms, and confirmation that the recirculation/minimum-flow protection is functional.

| Item | Value |
|---|---|
| Required interval | 12 months, not to exceed |
| Last statutory OISD periodic inspection performed | **2019-03-11** |
| Next inspection was due | 2020-03-11 |
| Date of this compilation | 2026-07-21 |
| **Elapsed since last statutory inspection** | **~7 years 4 months** |
| **Status** | **OVERDUE — NON-COMPLIANT** |

Notes on why the record shows this gap: the 2020 inspection window fell during the extended outage deferral; the 2021 and 2022 windows were logged as "deferred — awaiting turnaround slot" in the maintenance system without a formal deferral risk assessment being closed out. The 2023 seal failure (see separate incident report) generated a corrective work order but that work order was closed as *breakdown maintenance*, **not** as a statutory periodic inspection, and therefore did not reset the OISD clock. Condition-monitoring (PdM) inspections from 2025 onward, recorded in Sections 3–7 below, are **routine predictive maintenance activities and do not satisfy the statutory requirement.** The statutory inspection remains outstanding as of this compilation date.

**Recommendation:** Raise a priority-1 compliance work order. The statutory inspection cannot be closed on running-machine data alone — it requires the pump to be opened for pressure-boundary verification and requires functional proof-testing of MOV-118 and the TE-101B / PT-101 trip loops.

---

## 2. Inspection Record Index

| Ref | Date | Type | Machine state | Outcome summary |
|---|---|---|---|---|
| INS-2019-0311 | 2019-03-11 | **OISD statutory periodic inspection** | Shut down, opened | Satisfactory. Last compliant statutory record. |
| INS-2023-0817 | 2023-08-17 | Post-failure teardown inspection | Shut down, dismantled | Seal and thrust bearing failure. See incident report. |
| INS-2025-0409 | 2025-04-09 | PdM — vibration + thermography | Running | ISO 20816 Zone B. Minor upward trend noted. |
| INS-2025-1112 | 2025-11-12 | PdM — vibration + thermography | Running | Zone B, upper. Bearing housing temps rising. |
| INS-2026-0318 | 2026-03-18 | PdM — vibration, thermography, alignment | Running / brief stop | Zone C on outboard radial. Alignment within tolerance. |
| INS-2026-0630 | 2026-06-30 | PdM — vibration + thermography, focused | Running | **Zone C, deteriorating.** Recirculation flow suspect. |

---

## 3. Vibration Analysis (VE-101B and portable data collection)

Data collected with a portable dual-channel analyser, accelerometer stud-mounted on bearing housings, 3,200 lines resolution, 0–1,000 Hz baseband plus a 0–200 Hz zoom around 1× and 2× running speed. Running speed 2,965 rpm = **49.4 Hz (1×)**. Vane pass frequency at 7 vanes = **345.9 Hz**.

Severity assessed against **ISO 20816-3** (superseding ISO 10816-3) for Group 1 machines, rigid support, using broadband RMS velocity in the 10–1,000 Hz band. Zone boundaries paraphrased: Zone A is newly commissioned condition; Zone B is acceptable for unrestricted long-term operation; Zone C is unsatisfactory for continuous operation — suitable only for a limited period pending corrective opportunity; Zone D is severe enough to cause damage. For this machine class the A/B boundary sits at 2.8 mm/s RMS, B/C at 4.5 mm/s RMS, and C/D at 7.1 mm/s RMS.

### 3.1 Broadband velocity trend (mm/s RMS, 10–1,000 Hz)

| Date | Inboard radial H | Inboard radial V | Outboard radial H | Outboard radial V | Thrust / axial | ISO 20816-3 Zone |
|---|---|---|---|---|---|---|
| 2019-03-11 (post-inspection baseline) | 1.6 | 1.4 | 1.9 | 1.7 | 1.1 | A |
| 2023-08-14 (3 days pre-failure) | 3.9 | 3.6 | 5.8 | 5.1 | 6.4 | C / approaching D |
| 2025-04-09 | 2.4 | 2.2 | 3.1 | 2.8 | 1.9 | B |
| 2025-11-12 | 3.0 | 2.7 | 4.2 | 3.8 | 2.6 | B (upper) |
| 2026-03-18 | 3.5 | 3.1 | 4.9 | 4.4 | 3.3 | **C** |
| 2026-06-30 | 3.8 | 3.4 | 5.4 | 4.7 | 4.1 | **C** |

### 3.2 Spectral description — INS-2026-0630 (outboard radial horizontal, worst point)

- **1× (49.4 Hz):** 1.9 mm/s. Moderate, stable across the last three surveys. Not the dominant component. Residual unbalance judged acceptable.
- **2× (98.8 Hz):** 0.7 mm/s. Low. No indication of significant misalignment, consistent with the alignment check in Section 6.
- **Vane pass 7× (345.9 Hz):** 1.4 mm/s, up from 0.6 mm/s in April 2025. A rising vane pass amplitude with sidebands spaced at 1× is characteristic of increased hydraulic interaction between impeller vanes and diffuser/volute tongue. This is what is expected when the pump is forced away from BEP toward low flow, where the incidence angle on the vane inlet becomes strongly mismatched.
- **Broadband random energy, 5–25 Hz sub-synchronous region:** elevated, non-discrete, raised noise floor with an ill-defined hump between roughly 0.4× and 0.8× running speed. This "haystack" signature is the classic indicator of **internal recirculation at low flow** — the recirculating vortex at the impeller eye and at the discharge tips produces broadband, non-periodic excitation rather than a discrete order.
- **High-frequency demodulated envelope (500–5,000 Hz), inboard sleeve bearing:** no discrete bearing defect tones (sleeve bearings do not generate them), but an elevated overall envelope level of 0.29 g consistent with reduced oil film thickness and increased metal-to-metal micro-contact.
- **Thrust/axial channel:** the axial level of 4.1 mm/s with a strong 1× axial component is significant. Rising axial vibration on a multistage BFW pump correlates with axial thrust imbalance, which itself worsens as the pump moves left of BEP because the balance device / balance drum leak-off geometry is designed around a design-point pressure profile.

**Interpretation:** the vibration signature is *not* that of a mechanical defect such as unbalance, misalignment, looseness, or a rolling-element bearing fault. It is a **hydraulic signature consistent with sustained operation below the minimum continuous stable flow of 72 m³/h.** The corroborating process evidence is that FT-101 has been logging periods in the 55–68 m³/h band on hot afternoons, and PDI-S14 across S-14 has been trending upward toward 0.6 bar against a 0.5 bar alarm and a clean value near 0.2 bar.

---

## 4. Infrared Thermography

Camera: LWIR microbolometer, 640×480, calibrated 2026-01, emissivity set 0.95 on painted housings and 0.87 on bare machined surfaces, reflected apparent temperature compensated. Surveys taken at steady load, machine thermally soaked ≥ 4 h.

| Date | Ambient °C | IB bearing housing °C | OB bearing housing °C | Thrust bearing housing °C | Seal chamber °C | Seal cooler outlet °C | Motor DE bearing °C | Motor NDE bearing °C | Motor frame °C |
|---|---|---|---|---|---|---|---|---|---|
| 2025-04-09 | 29 | 61 | 63 | 66 | 71 | 48 | 54 | 51 | 68 |
| 2025-11-12 | 24 | 67 | 70 | 74 | 79 | 55 | 57 | 53 | 71 |
| 2026-03-18 | 33 | 74 | 78 | 81 | 88 | 62 | 60 | 56 | 74 |
| 2026-06-30 | 41 | 81 | 86 | 89 | 97 | 71 | 63 | 59 | 78 |

Alarm reference values are inconsistent between documents and this needs resolving: the **operating manual states a bearing temperature alarm of 85 °C**, while the **vendor datasheet states 90 °C alarm and 100 °C trip**. The 2026-06-30 outboard reading of 86 °C exceeds the operating manual alarm and sits between the two documented thresholds. Additionally, comparison against a portable pyrometer indicates **TE-101B reads approximately 5% high**, so the DCS indication should be interpreted with that offset in mind — this discrepancy is recorded in operator shift notes and has not been formally corrected in the instrument loop file.

Qualitative observations:
- Thermal gradient across the seal cooler on 2026-06-30 was only 26 K against a design 40 K, indicating **cooler fouling on the Plan 23 loop** and reduced heat removal from the seal chamber.
- The outboard bearing housing shows a hotter pattern on the lower half, consistent with reduced oil film and load concentration rather than with an external heat source.
- Motor bearings and motor frame are unremarkable and track ambient. The motor is not the source of the heat.
- No hot spots found on the coupling guard, foundation, or baseplate.

**Interpretation:** the temperature rise is being driven from the **process/hydraulic side**, not the electrical side. Low flow means low mass flow available to carry away the pump's absorbed power; the energy that is not converted to useful head is dissipated into the liquid in the casing (churn heating), which raises seal chamber and bearing housing temperatures. Fouling of the Plan 23 seal cooler compounds this by reducing the ability to reject that heat.

---

## 5. Mechanical Seal Inspection

Arrangement: single cartridge seal, balanced, stationary springs, silicon carbide vs. carbon primary faces, with **API 682 Plan 23** flush — a closed-loop recirculation from the seal chamber, driven by a pumping ring, through a seal cooler and back to the seal chamber. Plan 23 is the correct selection for hot boiler feed water because it cools the same small volume of liquid repeatedly rather than continuously injecting hot product, but it is entirely dependent on the cooler and on the pumping ring seeing adequate flow.

| Date | Leakage | Seal chamber temp °C | Cooler ΔT (K) | Faces | Notes |
|---|---|---|---|---|---|
| 2019-03-11 | Nil, dry gland | 68 | 41 | New at 2018 overhaul, as-new | Satisfactory |
| 2023-08-17 | Gross — failed | — | 9 (cooler fouled) | Carbon face heat-checked, SiC face crazed, drive lugs fretted | Failed. Replaced. |
| 2025-04-09 | Nil visible, slight vapour wisp at gland | 71 | 23 | Not opened | Monitor |
| 2026-03-18 | Occasional weeping, ~2 drops/min at start-up, clears when hot | 88 | 19 | Not opened | Cooler cleaning recommended |
| 2026-06-30 | Weeping persists, light salt/scale deposit at gland face | 97 | 18 | Not opened | **Cooler cleaning overdue. Seal chamber approaching flash margin concern.** |

Concern: as seal chamber temperature climbs, the margin between local liquid temperature and the saturation temperature at seal chamber pressure narrows. If the liquid flashes across the seal faces, the faces lose their lubricating film and dry-run damage follows quickly. The 2023 failure showed exactly this signature. The current trend is moving in the same direction.

---

## 6. Bearing Inspection and Lubrication

| Date | Oil condition | Water in oil (ppm) | Particle count ISO 4406 | Fe (ppm) | Sn/Pb (ppm) | Notes |
|---|---|---|---|---|---|---|
| 2025-04-09 | Clear, bright | 180 | 18/16/13 | 4 | <1 | Normal |
| 2025-11-12 | Clear, faint haze | 340 | 19/17/13 | 7 | 2 | Watch |
| 2026-03-18 | Slight darkening | 520 | 20/18/14 | 12 | 5 | Oil change recommended |
| 2026-06-30 | Darkened, mild varnish odour | 690 | 20/18/15 | 19 | **11** | **Babbitt wear indicated. Act.** |

The appearance and rise of tin and lead in the oil is the significant finding — those are babbitt constituents, and their presence indicates the white metal bearing surfaces are being worn. Combined with the elevated envelope energy in Section 3.2 and the housing temperatures in Section 4, this points to a **reduced oil film thickness caused by elevated oil temperature**, which is itself a consequence of the elevated bearing housing temperature. Oil viscosity falls sharply with temperature; below a critical film thickness, asperity contact begins and babbitt is shed.

Thrust bearing: no direct inspection since 2023. Given the rising axial vibration and the known sensitivity of multistage BFW pump axial thrust to off-design operation, the tilting pads should be inspected at the next opportunity — which should be combined with the overdue statutory inspection.

---

## 7. Alignment Check (INS-2026-0318)

Method: dual laser shaft alignment, reverse-indicator equivalent, cold readings taken with subsequent thermal growth offsets applied per vendor thermal growth data.

| Parameter | Measured | Tolerance (2,970 rpm) | Result |
|---|---|---|---|
| Vertical angular | 0.03 mm/100 mm | 0.05 mm/100 mm | Pass |
| Horizontal angular | 0.02 mm/100 mm | 0.05 mm/100 mm | Pass |
| Vertical offset | 0.04 mm | 0.06 mm | Pass |
| Horizontal offset | 0.03 mm | 0.06 mm | Pass |
| Soft foot (max) | 0.03 mm | 0.05 mm | Pass |
| Coupling condition | Flexible element intact, no fretting | — | Pass |
| Foundation / grout | No cracking, no bolt looseness, torque checked | — | Pass |
| Pipe strain check | Suction and discharge flange movement on unbolting < 0.05 mm | 0.05 mm | Pass (marginal on suction) |

Alignment and foundation are sound and are **not** contributing to the current condition. This is an important negative finding: it removes the most common mechanical explanations and reinforces the hydraulic/process explanation.

---

## 8. Overall Assessment and Recommendations

**Condition summary:** P-101B is operating in ISO 20816-3 **Zone C** with a vibration signature dominated by low-flow hydraulic excitation (broadband sub-synchronous energy, rising vane pass with 1× sidebands, rising axial). Bearing housing and seal chamber temperatures are rising year-on-year and season-on-season, oil analysis shows the onset of babbitt wear, and the Plan 23 seal cooler is fouled to less than half its design duty. Mechanical fundamentals — alignment, balance, foundation, coupling, motor — are all sound.

**The chain of causation supported by these records:**
1. S-14 suction strainer is fouling; PDI-S14 has risen from a clean ~0.2 bar toward ~0.6 bar against a 0.5 bar alarm.
2. Restricted suction reduces available flow to P-101B, and MOV-118 minimum-flow recirculation is not reliably opening to make up the shortfall — operators report it sticks, particularly in summer.
3. The pump therefore spends time below its 72 m³/h minimum continuous stable flow. Absorbed power that cannot leave as useful hydraulic work is dissipated into the liquid — churn heating — and into the bearings.
4. TE-101B trends upward, seal chamber temperature climbs, oil film thins, and vibration rises.

**Recommendations, in priority order:**

| # | Action | Priority | Owner |
|---|---|---|---|
| 1 | Raise and execute the **overdue OISD statutory periodic inspection**. Compliance gap of ~7 years since 2019-03-11. | 1 — Immediate | Inspection Engineer |
| 2 | Clean / backflush S-14 and restore PDI-S14 to ≤ 0.25 bar. Verify mesh integrity. | 1 — Immediate | Maintenance Planner |
| 3 | Stroke-test and overhaul MOV-118. Confirm it opens fully and reliably at the low-flow setpoint and does not stick at high ambient. | 1 — Immediate | Instrument/Valves |
| 4 | Clean the Plan 23 seal cooler; restore ΔT to ≥ 35 K. | 2 — Within 2 weeks | Maintenance |
| 5 | Change bearing oil, fit a desiccant breather, resample at 500 h. | 2 — Within 2 weeks | Lubrication |
| 6 | Calibrate TE-101B and formally document the ~5% high reading offset. Resolve the 85 °C vs 90 °C/100 °C alarm/trip discrepancy between the operating manual and the datasheet in a single controlled document. | 2 — Within 1 month | Instrumentation |
| 7 | Inspect thrust bearing pads at the next shutdown, combined with item 1. | 3 — Next opportunity | Rotating Equipment |
| 8 | Increase PdM survey frequency to monthly until vibration returns to Zone B. | 3 — Ongoing | Reliability |

**Fitness for service:** P-101B may continue to operate under Zone C conditions only with increased surveillance and only until the corrective opportunity above is taken. If broadband velocity reaches 7.1 mm/s RMS (Zone C/D boundary), or if TE-101B indicates sustained operation above the datasheet 90 °C alarm after correcting for the known instrument offset, the pump should be taken off line and the load transferred to P-101A.

---

*Compiled from work orders, PdM route data, oil analysis certificates, and inspection field notes. Related documents: strainer S-14 maintenance history; 2023 P-101B seal failure incident report; BFW pump lessons learned; operator shift handover log.*
