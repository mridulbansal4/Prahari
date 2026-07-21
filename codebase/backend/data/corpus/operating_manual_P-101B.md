# Operating Manual — Boiler Feed Pump `P-101B`
## Document No. OM-BFW-101B Rev. 6
**Unit:** 100 — Boiler Feed Water
**Applies to:** `P-101B` (Boiler Feed Pump B). Parallel unit `P-101A` is covered by OM-BFW-101A; the two manuals are identical except for tag numbers and the shared-header sequencing caution in Section 10.
**P&ID:** PID-BFW-002 Rev. 4 | **Datasheet:** DS-ROT-101B Rev. 3
**Audience:** Panel operators, field operators, shift supervisors
**Status:** CONTROLLED COPY — FIELD USE

---

## 1. Introduction and Machine Overview

`P-101B` is a six-stage, between-bearings, ring-section centrifugal boiler feed pump delivering deaerated feed water from deaerator DA-100 to the economiser inlets of Boilers B-01 and B-02. It draws from the common suction header through isolation valve `HV-115` and suction strainer `S-14`, and discharges through check valve `NRV-117` into the common discharge header shared with `P-101A`.

Key protective features that operators must understand before running this machine:

- **Minimum-flow recirculation** via `MOV-118`, which returns feed water to DA-100 through restriction orifice `RO-119` whenever discharge flow measured by `FT-101` falls toward the pump's minimum continuous stable flow of **72 m³/h**.
- **Mechanical seal flush** on **API 682 Plan 23**, a closed-loop circulation through seal cooler `SC-101B`.
- **Bearing temperature monitoring** at `TE-101B` and **vibration monitoring** at `VE-101B`.
- **Suction strainer differential** indicated locally and in the DCS by `PDI-S14`.

The machine is high-energy. At 820 m rated head and 652 kW absorbed at duty, the pump converts a very large amount of shaft power into fluid energy; when that energy has nowhere to go — that is, when flow is restricted — it is dissipated as heat inside the casing. Almost every abnormal-temperature scenario on this machine traces back to a flow problem, not to a lubrication or cooling problem.

---

## 2. Pre-Start Checks

Complete the following in order. Sign the shift checklist.

**2.1 Isolation and line-up**
1. Confirm suction isolation `HV-115` is FULLY OPEN and locked open. A throttled suction valve is the single most common cause of premature seal and bearing distress on this pump.
2. Confirm discharge isolation `HV-120` is CLOSED or cracked open per the start method selected in Section 3.
3. Confirm `MOV-118` is OPEN (fail-open position; confirm limit switch indication at the panel, not just the DCS icon).
4. Confirm the balance line from the balance drum back to the suction is open and unobstructed.
5. Confirm casing and suction line vents are used to fully vent and prime the pump. There must be a continuous solid column of water from DA-100 to the pump. Vent until steady liquid flow with no steam or gas is observed.

**2.2 Strainer and suction condition**
6. Read `PDI-S14`. A clean element at normal flow reads approximately **0.2 bar**. If `PDI-S14` reads above **0.5 bar**, raise a work request before starting; do not accept the reading as normal drift.
7. Confirm DA-100 level via `LT-100` is at or above 55 % and DA-100 pressure is at normal operating value. Low deaerator pressure or level directly erodes NPSH available at the pump suction.
8. Confirm knockout drum `V-201` level is normal and `LCV-201` is controlling. Carryover from `V-201` degrades pegging steam quality to DA-100 and can depress deaerator pressure.

**2.3 Lubrication and cooling**
9. Confirm bearing lube oil reservoir level is between the sight-glass marks. Oil is ISO VG 32 turbine grade; do not top up with any other grade.
10. Start the auxiliary lube oil pump. Confirm bearing header pressure reaches 1.5 barg and oil supply temperature stabilises at 45 °C ± 3 °C.
11. Confirm cooling water is flowing to oil cooler `OC-101B` and to seal cooler `SC-101B`. Feel both return lines; a cold return line on `SC-101B` with the pump running means the Plan 23 loop is not circulating.
12. Confirm the lube oil filter differential is below its changeout value.

**2.4 Instrumentation**
13. Confirm `TE-101B`, `VE-101B`, `PT-101`, `FT-101`, and `PDI-S14` are all reading live and are not in a forced, bypassed, or inhibited state in the DCS. Any inhibit must be logged and time-limited.
14. Confirm no standing alarms on the machine.

**2.5 Mechanical**
15. Confirm coupling guard is fitted and secure.
16. Confirm no leakage at the seal gland. If the gland has been disturbed, confirm the maintenance record shows the gland bolts were tightened to the correct torque in a diagonal pattern. **Note:** the equipment datasheet specifies **45 N·m** for the M12 gland bolts; the maintenance SOP (SOP-MNT-207) currently specifies 55 N·m. This discrepancy is an open Management of Change item. Until it is closed, record the value actually used in the job record.
17. Hand-bar the rotor one full revolution if the pump has been idle more than 72 hours. It must turn freely.

---

## 3. Startup Sequence

Start against a closed or nearly closed discharge with the recirculation path proven open. The recirculation line, not the discharge line, carries the pump during the first moments of running.

1. Verify `MOV-118` is OPEN and its limit switch confirms the open position.
2. Verify `HV-115` open, `HV-120` closed.
3. Confirm auxiliary lube oil pump running and bearing oil pressure healthy.
4. Start motor `M-101B`. Observe the ammeter. Starting current should decay to no-load within 6–8 seconds.
5. Within 10 seconds of reaching speed, confirm `PT-101` shows discharge pressure rising toward shutoff head (approximately 92 barg equivalent at shutoff; expect 88–95 barg with `HV-120` closed).
6. Confirm `FT-101` registers recirculation flow of approximately 72–82 m³/h through `MOV-118`. **If `FT-101` does not register flow within 20 seconds, trip the pump immediately.** The machine is running at true shutoff and is heating the casing inventory at several degrees per minute.
7. Open `HV-120` slowly, over not less than 60 seconds, bringing the pump into the discharge header. Watch `PT-101` settle toward header pressure and `FT-101` rise.
8. As discharge flow rises above 72 m³/h, `FIC-101` will begin to modulate `MOV-118` closed. Confirm the valve strokes. Confirm the valve position feedback changes — do not accept a demand signal alone as evidence of movement.
9. When total flow exceeds approximately 105 m³/h, `MOV-118` should be fully closed. Confirm the recirculation line downstream of `RO-119` cools down over the following 10–15 minutes.
10. Stop the auxiliary lube oil pump only after bearing temperatures at `TE-101B` have stabilised and the main shaft-driven oil supply is proven.
11. Log start time, `PDI-S14`, `TE-101B` both ends, and `VE-101B` at 15 minutes and at 1 hour after start.

---

## 4. Normal Operating Parameters

| Parameter | Instrument | Normal | Acceptable range |
|---|---|---|---|
| Discharge flow | `FT-101` | 240 m³/h | 168 – 288 m³/h (preferred region) |
| Discharge pressure | `PT-101` | 78 barg | 74 – 84 barg |
| Suction pressure | — | 1.35 bar a | ≥ 1.20 bar a |
| Strainer differential | `PDI-S14` | 0.2 bar | ≤ 0.5 bar |
| Bearing temperature DE/NDE | `TE-101B` | 58 – 72 °C | ≤ 85 °C |
| Vibration | `VE-101B` | ≤ 2.3 mm/s RMS | ≤ 4.5 mm/s RMS (ISO 20816-3 Zone B) |
| Seal chamber temperature | — | 62 °C | ≤ 80 °C |
| Lube oil supply temperature | — | 45 °C | 42 – 48 °C |
| Motor current | — | 68 A | ≤ 82 A |
| `MOV-118` position at full load | — | CLOSED | — |

Operators should treat the **72 m³/h minimum continuous stable flow** as an absolute floor, not a target. Running near the floor for extended periods is permitted only for the duration of a genuine load transient and must be logged.

---

## 5. Minimum-Flow Protection and `MOV-118` Operation

`MOV-118` is a 3-inch motor-operated globe valve on the recirculation line from the common discharge header back to DA-100 through `RO-119`. Control logic:

- `FIC-101` receives the `FT-101` signal.
- Below **105 m³/h** measured discharge flow, `MOV-118` begins to open on a proportional ramp.
- At **72 m³/h** or below, `MOV-118` is commanded FULLY OPEN.
- The recirculation path is sized to pass 72 m³/h at full open, so a pump on full recirculation is exactly at its minimum continuous stable flow and no lower.
- `MOV-118` FAILS OPEN on loss of power or on loss of the `FT-101` signal.
- Valve travel time, fully closed to fully open, is 22 seconds.

**Known failure mode — sticking.** `MOV-118` has a documented history of sticking in the closed or near-closed position after long periods of continuous full-load running, when the valve has not stroked for weeks and the seat area accumulates deposit. When this happens, the DCS shows the valve *commanded* open while the actual position feedback lags or does not move at all, and the pump receives no recirculation protection. **Operators must compare commanded position against limit-switch feedback, not rely on the graphic.** A stuck-closed `MOV-118` combined with any restriction on the suction side is the specific combination that puts this pump below minimum flow without any single alarm annunciating it.

**Exercise requirement.** `MOV-118` shall be full-stroked at least once every 30 days during a planned low-load window, and the stroke logged.

---

## 6. Seal Flush System (API 682 Plan 23)

The seal on `P-101B` is a cartridge single seal with an **API 682 Plan 23** flush. An internal pumping ring circulates the seal-chamber inventory in a closed loop out to seal cooler `SC-101B` and back. A throat bushing separates the seal chamber from the hot pumped fluid so that only a small volume is being cooled.

Operator checks:
- Seal cooler `SC-101B` cooling water inlet 32 °C, outlet typically 40–46 °C with the pump at load. A cold outlet indicates no circulation.
- Seal chamber temperature normal 62 °C, alarm 80 °C.
- Vent the Plan 23 loop at the cooler high point after any maintenance. A gas pocket in the loop will stall the circulation and the faces will run dry-ish and hot.
- Any visible leakage at the gland is abnormal for this seal type and requires a work request.

Because the Plan 23 loop only cools a small isolated inventory, it has limited ability to reject heat if the *bulk* pumped fluid is running hot. If the pump is churning below minimum flow, the seal chamber will follow the casing temperature upward and the cooler will not be able to hold it. **Rising seal chamber temperature accompanied by rising `TE-101B` is a symptom of a process/flow problem, not a seal-cooler problem.**

---

## 7. Bearing Lubrication and Cooling

`P-101B` runs on hydrodynamic sleeve radial bearings and a double-acting tilting-pad thrust bearing, pressure-fed with ISO VG 32 turbine oil at 1.5 barg and 45 °C, total flow 42 L/min, cooled by `OC-101B`.

- `TE-101B` measures **babbitt metal temperature**, embedded in the bearing shell — not oil drain temperature. Oil drain typically reads 12–18 °C lower.
- Normal band 58–72 °C at steady load.
- A slow rise across *both* DE and NDE elements together points to a heat source common to the whole machine (process heat, i.e. low flow) or to a lube-oil cooling problem.
- A rise on *one* element only points to a bearing or alignment problem local to that end.
- Do not attempt to correct a rising bearing temperature by increasing lube oil flow. The oil system has no spare capacity for process heat and doing so masks the real cause.

---

## 8. Normal Shutdown

1. Reduce load by transferring duty to `P-101A` per Section 10, or by reducing boiler demand.
2. As flow falls below 105 m³/h, confirm `MOV-118` opens on automatic control.
3. Close `HV-120` slowly over not less than 60 seconds.
4. Start the auxiliary lube oil pump and confirm bearing oil pressure before stopping the motor.
5. Stop motor `M-101B`.
6. Run the auxiliary lube oil pump for a further 15 minutes to remove residual bearing heat.
7. Leave `HV-115` open and the pump primed and vented unless the machine is being handed over for maintenance.
8. Leave `MOV-118` in its fail-open position.
9. Maintain cooling water to `SC-101B` for 20 minutes after stopping to prevent the seal faces heat-soaking.
10. Log final `TE-101B`, `VE-101B`, and `PDI-S14` readings.

**Emergency shutdown.** Press the local ESD at the pump or the panel trip. The pump will coast to rest in approximately 25 seconds. Confirm `NRV-117` seats and the discharge header does not backflow through the idle machine.

---

## 9. Alarm and Trip Table

| Tag | Description | Alarm | Trip | Action |
|---|---|---|---|---|
| `TE-101B` | Bearing metal temperature DE/NDE | **85 °C** | 100 °C | Investigate flow first; see Section 11 |
| `VE-101B` | Broadband vibration | 4.5 mm/s RMS | 7.1 mm/s RMS | Reduce load, prepare to transfer duty |
| `FT-101` | Discharge flow low | 105 m³/h | 60 m³/h (2 s delay) | Confirm `MOV-118` actual position |
| `PT-101` | Discharge pressure low | 68 barg | 60 barg | Check suction, check for cavitation |
| `PT-101` | Discharge pressure high | 88 barg | 95 barg | Check downstream isolation |
| `PDI-S14` | Strainer differential high | 0.5 bar | — | Plan strainer changeout |
| `LT-100` | DA-100 level low | 35 % | 20 % | Pump trip on low-low |
| — | Lube oil pressure low | 1.0 barg | 0.7 barg | Aux pump auto-start on alarm |
| — | Seal chamber temperature | 80 °C | — | Check `SC-101B` circulation |
| — | Motor winding temperature | 130 °C | 145 °C | — |

> **NOTE — known discrepancy.** The bearing temperature alarm stated in this manual (**85 °C**) does not agree with the OEM equipment datasheet DS-ROT-101B Rev. 3, which specifies an alarm of **90 °C** and a trip of **100 °C**. The 85 °C value in this manual was adopted by site operations as a conservative early-warning setting. The discrepancy is a registered open item with Rotating Equipment Engineering. Until it is resolved, panel operators shall act on the earlier (85 °C) indication and shall not raise the DCS alarm setting without a Management of Change.

---

## 10. CAUTION — Restart Sequencing of `P-101A` and `P-101B`

`P-101A` and `P-101B` draw from a **common suction header** fed by a single 12-inch downcomer from DA-100. The header and downcomer are sized for the flow of one pump at rated duty plus margin — they are **not** sized for two pumps at full flow simultaneously.

**The hazard.** If the standby pump is started while the duty pump is already delivering full flow, the momentary combined draw on the shared header exceeds what the downcomer can supply. Header pressure at the suction nozzles collapses, NPSH available falls below the 4.8 m NPSH required, and **both machines cavitate** — not just the one being started. Cavitation in a six-stage pump at 820 m head damages first-stage impeller eyes and wear rings within minutes and produces immediate vibration excursion at `VE-101B`.

**Mandatory sequencing rules:**

1. **Never start `P-101A` while `P-101B` is running at above 150 m³/h, and never start `P-101B` while `P-101A` is running at above 150 m³/h.**
2. To transfer duty: first reduce the running pump's flow to below 150 m³/h by reducing boiler demand or by allowing its `MOV`-controlled recirculation to open. Then start the incoming pump against a closed discharge with its own recirculation open. Then bring the incoming pump onto the header and unload the outgoing pump before stopping it.
3. Overlap of both pumps on the header shall not exceed **5 minutes**.
4. During any overlap, watch DA-100 level (`LT-100`) and suction pressure continuously. A falling deaerator level during overlap is an immediate instruction to unload one machine.
5. After an unplanned trip of one pump, **do not immediately restart it into a header where the other pump has already auto-started**. Confirm the auto-started pump is stable, its recirculation is behaving, and header pressure has recovered before attempting any restart. A restart into a disturbed header is the worst case for the cavitation hazard described above.
6. If auto-standby start of `P-101A` occurs while `P-101B` is being restarted manually, abort the manual restart.
7. This caution does not apply to `P-102` or `E-301`, which are not on this suction header.

---

## 11. Troubleshooting: Pump Running Hot

This is the most frequently encountered abnormality on `P-101B`. The symptom is a rising `TE-101B` bearing metal temperature, often accompanied by rising seal chamber temperature and a broadband vibration rise at `VE-101B`. The instinct is to look at the lube oil cooler or the bearings. **On this machine, that is usually the wrong place to start.**

### 11.1 The dominant causal chain

The characteristic sequence on `P-101B`, in the order it develops:

**Step 1 — `S-14` fouls and `PDI-S14` rises.**
Suction strainer `S-14` accumulates mill scale, corrosion product, and construction debris carried from the deaerator storage section. As the element blinds, differential pressure across it climbs from the clean value of approximately **0.2 bar** toward and past the **0.5 bar** alarm. Recent trend data shows `PDI-S14` approaching **0.6 bar**, which is well into abnormal territory. Every bar of strainer differential is a bar removed from NPSH available at the pump suction nozzle.

**Step 2 — flow to `P-101B` falls, and `MOV-118` fails to compensate.**
The additional suction-side resistance shifts the pump's operating point back along its curve; delivered flow at `FT-101` drops. This should command `MOV-118` open to make up the deficit and hold the machine at or above minimum flow. But `MOV-118` has a known tendency to stick in the near-closed position after long periods without stroking (Section 5). When the valve sticks, the DCS shows the open command while the valve has not actually moved, and the protection that should have caught the falling flow silently does not act.

**Step 3 — the pump drops below minimum continuous flow and churns.**
With the strainer restricting suction and `MOV-118` not providing recirculation, total flow through `P-101B` falls below the **72 m³/h** minimum continuous stable flow. At this point the machine is absorbing well over 380 kW while delivering very little hydraulic work. The difference goes into the liquid trapped in the casing. Internal recirculation begins at the impeller eyes and discharge tips. The casing inventory heats rapidly; on a six-stage machine of this energy density, the trapped inventory can rise several degrees per minute at near-shutoff conditions.

**Step 4 — `TE-101B` bearing temperature trends up.**
Heat from the churning fluid conducts through the shaft, the balance drum, and the casing into the bearing housings, and reaches the seal chamber through the throat bushing faster than the Plan 23 loop and `SC-101B` can reject it. `TE-101B` begins a slow, steady, *symmetrical* rise on both drive-end and non-drive-end elements. This symmetry is the tell: a genuine bearing defect heats one end, while process churn heats both.

### 11.2 Diagnostic order — do these in this sequence

1. **Read `PDI-S14` first.** If it is above 0.5 bar, and especially if it is near 0.6 bar, you have found the initiating cause. Do not proceed to bearing diagnostics.
2. **Read `FT-101`.** Compare against 72 m³/h. If total flow is at or below the minimum continuous stable flow, the pump is churning regardless of what any other instrument says.
3. **Check `MOV-118` actual position feedback, in the field if necessary.** Compare against the commanded position. A mismatch confirms a stuck valve. Feel the recirculation line downstream of `RO-119` — if the pump is supposed to be recirculating, that line will be hot.
4. **Check `PT-101`.** Discharge pressure elevated toward shutoff (88 barg or above) with low `FT-101` confirms the pump is operating far back on its curve.
5. **Check `VE-101B`.** Look for broadband energy at 0.4–0.8 × running speed, the signature of suction recirculation, rather than a clean 1× or 2× line.
6. **Check the seal chamber temperature.** If it is rising together with `TE-101B`, the heat source is the process fluid, not the bearings.
7. **Only now check the lube oil system** — oil supply temperature, `OC-101B` cooling water, filter differential. If oil supply is at its normal 45 °C and the bearings are still hot, the heat is not coming from the oil system.

### 11.3 Immediate actions

- If `TE-101B` reaches the 85 °C alarm and the flow diagnosis above is confirmed: **restore flow**. Manually drive `MOV-118` open from the local station. If it will not move, increase demand to the boilers to pull flow through the pump.
- If flow cannot be restored within a few minutes, transfer duty to `P-101A` following the sequencing rules in Section 10 exactly. Do not rush the transfer — a cavitation event caused by a hurried transfer is worse than a few more minutes at elevated bearing temperature.
- Once `P-101B` is offline, isolate and change the `S-14` element (spare STR-T8-40M, held on site).
- Raise a work request for `MOV-118` stroke testing and seat inspection.
- Do not restart `P-101B` until `PDI-S14` reads at or near 0.2 bar with the new element and `MOV-118` has been proven to stroke fully.

### 11.4 Other causes of high bearing temperature (less common on this machine)

| Cause | Distinguishing evidence |
|---|---|
| Lube oil cooler `OC-101B` fouled | Oil supply temperature above 48 °C; cooling water return cold |
| Lube oil filter blocked | Filter differential high; bearing header pressure below 1.5 barg |
| Wrong oil grade after top-up | Recent maintenance record; oil appears wrong viscosity in sight glass |
| Coupling misalignment | Temperature rise on one end only; 2× running speed vibration |
| Bearing wear / babbitt damage | One element only; step change rather than slow trend; metal in oil |
| Excessive thrust from worn balance drum | Thrust bearing hot, radials normal; balance line hot |
| Seal cooler `SC-101B` fouled or gas-locked | Seal chamber hot but `TE-101B` normal or only slightly elevated |

Note that all of the entries in this table produce either an *asymmetric* or a *step-change* signature. The flow-related chain in Section 11.1 produces a *symmetric, gradual* rise on both bearings together, in company with an abnormal `PDI-S14` and a low `FT-101`. Use that distinction to triage quickly.

---

## 12. Records

Each shift shall record: `FT-101`, `PT-101`, `PDI-S14`, `TE-101B` (DE and NDE), `VE-101B`, seal chamber temperature, lube oil supply temperature, `MOV-118` position, and DA-100 level. Trend `PDI-S14` weekly and flag any sustained rise above 0.35 bar for planning purposes, well before the 0.5 bar alarm.

---

**Rev 6 — issued 2026-06-18.** Supersedes Rev 5 (2025-02-11). Changes: Section 11 expanded with full causal chain and diagnostic ordering; Section 10 restart sequencing caution formalised with numbered mandatory rules; alarm table note added regarding the bearing temperature discrepancy against DS-ROT-101B Rev. 3; `MOV-118` 30-day exercise requirement added.
