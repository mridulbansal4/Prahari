# Suction Strainer S-14 — Maintenance and Condition History

**Asset Tag:** S-14
**Description:** Suction Strainer 14 — permanent basket-type suction strainer on the boiler feed water suction line to P-101B
**Location:** Downstream of the deaerator storage vessel outlet, upstream of the P-101B suction flange, in the horizontal run before the suction reducer
**Associated Instrument:** PDI-S14 (differential pressure indicator/transmitter across the strainer, DCS point, alarmed)
**Protected Equipment:** P-101B (Boiler Feed Pump B)
**Document revision date:** 2026-07-21
**Owner:** Utilities Maintenance / Rotating Equipment Reliability

---

## 1. Purpose and Criticality

S-14 exists for one reason: to keep solid debris out of P-101B. A multistage boiler feed water pump has extremely tight running clearances at the wear rings, interstage bushings, and balance drum — typically in the 0.30–0.45 mm diametral range. Debris that would pass harmlessly through a general-service pump will cut those clearances open in a BFW pump, and once clearances open the pump loses efficiency, loses head, and becomes hydraulically unstable.

However, S-14 is also a hazard to the very machine it protects. Every strainer is a deliberate restriction in a suction line, and a suction line is where a centrifugal pump has the least pressure margin to spare. **A fouled S-14 is a direct threat to P-101B, because it takes away net positive suction head available (NPSHa) and throttles suction flow.** This document exists largely because that is exactly what is happening at the time of writing.

---

## 2. Mechanical Specification

| Parameter | Specification |
|---|---|
| Type | Basket strainer, permanent, removable basket, top-entry cover |
| Body size / rating | DN 250 (10"), ASME B16.5 Class 300 RF |
| Body material | ASTM A216 WCB carbon steel |
| **Basket / mesh material** | **AISI 316L stainless steel, perforated plate with reinforcing backing** |
| **Perforation / mesh size** | **1.6 mm (1/16 in) perforated plate, backed by 40-mesh (≈ 0.40 mm aperture) fine screen on the startup basket; standard operating basket is 1.6 mm perforated plate only** |
| Basket open area ratio | **3.2 : 1** open area relative to the nominal pipe cross-section (design minimum 3:1 for suction service) |
| Free open area of basket | approx. 32% of the basket surface |
| **Design clean differential pressure** | **≈ 0.2 bar at rated flow of 240 m³/h** |
| **PDI-S14 high differential alarm** | **0.5 bar** |
| Recommended cleaning trigger | 0.35 bar (site practice, set below alarm to allow planned intervention) |
| Maximum permissible differential (basket collapse margin) | 1.2 bar, per basket manufacturer's collapse rating with 2:1 safety factor |
| Design flow | 240 m³/h |
| Design temperature | 160 °C |
| Fluid | Deaerated boiler feed water, treated, pH 9.2–9.6, oxygen scavenged |
| Basket removal | Requires isolation of the P-101B suction; no bypass installed |

**Note on the absence of a bypass:** S-14 has no permanent bypass line. Cleaning therefore requires taking P-101B out of service and transferring feedwater duty to P-101A. This is the single biggest reason cleaning has historically been deferred — the cleaning is not difficult, but it costs a pump swap, and swapping pumps has its own restart sequencing hazards (see the shift handover log and lessons learned document regarding suction header cavitation on restart).

---

## 3. PDI-S14 Differential Pressure Trend — CURRENT CONCERN

The differential pressure across S-14 is the primary condition indicator. A clean basket should read approximately **0.2 bar** at rated flow. Readings are corrected to rated flow where the survey was taken at part load, since differential across a strainer varies roughly with the square of flow.

| Date | PDI-S14 (bar, corrected to 240 m³/h) | FT-101 flow at reading (m³/h) | Status |
|---|---|---|---|
| 2024-11-02 (post-clean) | 0.19 | 236 | Clean baseline |
| 2025-01-15 | 0.21 | 231 | Normal |
| 2025-04-09 | 0.24 | 228 | Normal, slight rise |
| 2025-07-22 | 0.29 | 219 | Watch |
| 2025-10-06 | 0.31 | 214 | Watch |
| 2025-11-12 | 0.34 | 208 | Approaching cleaning trigger |
| 2026-01-20 | 0.38 | 199 | **Cleaning trigger exceeded (0.35 bar)** |
| 2026-03-18 | 0.44 | 186 | Deteriorating |
| 2026-05-11 | 0.52 | 171 | **ALARM — 0.5 bar exceeded** |
| 2026-06-30 | 0.58 | 158 | Alarm standing |
| **2026-07-18 (latest)** | **≈ 0.60** | **149** | **ALARM STANDING — S-14 IS CLOGGED** |

### Interpretation

The differential has risen from a clean **0.2 bar** to approximately **0.6 bar** — three times the clean value and well past the **0.5 bar alarm**. The corresponding fall in FT-101 indicated flow, from 236 m³/h down to 149 m³/h, is the direct hydraulic consequence. **S-14 fouling is currently restricting flow to P-101B and is the upstream origin of the pump's low-flow operating problem.**

Two aggravating observations:

1. **The alarm has been standing since 2026-05-11 and has effectively become background noise on the DCS alarm list.** Operators have logged it repeatedly in shift notes. It has not resulted in a cleaning work order being executed, because executing it requires the pump swap described in Section 2.

2. **The flow figures above are the daytime steady-state averages.** On hot afternoons, when total feedwater demand is highest and the deaerator storage temperature is at its highest (so NPSHa margin is at its thinnest), the instantaneous flow through P-101B has been logged as low as **55–68 m³/h**. That is below the pump's **minimum continuous stable flow of 72 m³/h**. Under those conditions the pump is running in a region it was never designed to occupy.

---

## 4. Cleaning History and Debris Found

| # | Date | Trigger | ΔP before (bar) | ΔP after (bar) | Debris recovered | Mass (approx) | Basket condition | Executed by |
|---|---|---|---|---|---|---|---|---|
| 1 | 2019-03-11 | Combined with statutory pump inspection | 0.33 | 0.20 | Mill scale flakes, some weld slag beads, black magnetite fines | 1.4 kg | Good, no damage | Mech. Maint. (RKS) |
| 2 | 2020-06-24 | Routine | 0.30 | 0.21 | Mill scale, magnetite sludge | 0.9 kg | Good | Mech. Maint. (AJ) |
| 3 | 2021-09-08 | Alarm | 0.51 | 0.22 | Heavy magnetite, corrosion product from deaerator internals, small quantity of gasket fragment | 2.1 kg | Minor deformation on one basket panel, dressed back | Mech. Maint. (RKS) |
| 4 | 2022-05-30 | Routine | 0.36 | 0.21 | Magnetite fines, mill scale | 1.1 kg | Good | Mech. Maint. (PVN) |
| 5 | 2023-02-14 | Alarm | 0.55 | 0.23 | Mill scale, weld slag (traced to the 2022 deaerator downcomer tie-in), corrosion products | 2.6 kg | Perforated plate locally distorted; basket replaced | Mech. Maint. (AJ) |
| 6 | 2023-08-18 | **Post seal-failure investigation on P-101B** | 0.62 | 0.20 | **Heavy loading — magnetite, mill scale, deaerator corrosion products, approx 25% of open area blinded** | 3.4 kg | New basket (from #5) still sound | Mech. Maint. (RKS) |
| 7 | 2024-04-19 | Routine | 0.35 | 0.21 | Magnetite fines | 0.8 kg | Good | Mech. Maint. (PVN) |
| 8 | 2024-11-02 | Routine | 0.41 | 0.19 | Magnetite, light mill scale | 1.2 kg | Good | Mech. Maint. (AJ) |
| — | **OUTSTANDING** | **Alarm standing since 2026-05-11** | **≈ 0.60** | — | **Not yet cleaned** | — | — | **Work order raised, not executed** |

### Debris source analysis

Three distinct debris populations recur:

- **Mill scale** — hard, black, flaky iron oxide from the original fabrication of the feedwater piping and the deaerator storage vessel. Mill scale continues to shed for years after commissioning and is released in pulses whenever the system sees a thermal transient. It is the dominant debris after any shutdown/restart cycle.
- **Weld slag** — angular, glassy, grey particles. These trace to piping modifications; the 2023 population was clearly attributable to the deaerator downcomer tie-in performed in the 2022 shutdown, where post-weld cleaning was evidently incomplete. Weld slag is the most damaging debris class because it is hard and angular and will score wear rings.
- **Corrosion products from the deaerator** — predominantly magnetite (Fe₃O₄) fines, sometimes as a soft black sludge, sometimes as harder adherent scale. This population correlates with periods when deaerator oxygen scavenging has been off specification or when the unit has been laid up wet without a nitrogen blanket. Magnetite fines are individually small enough to pass a 1.6 mm perforation, but they agglomerate into a mat on the basket surface and it is this mat, not the individual particles, that blinds the open area.

**The fouling mechanism is progressive blinding, not sudden blockage.** The magnetite mat builds gradually over weeks, which is why the PDI-S14 trend is a smooth ramp rather than a step. It also means the pump is subjected to a slowly worsening restriction that never triggers an obvious "something broke" moment — and that is precisely why it is easy to normalise and defer.

---

## 5. Consequences of Fouling on P-101B

### 5.1 Loss of NPSH available

NPSHa at the pump suction is:

> NPSHa = (suction vessel pressure head) + (static head) − (friction losses, including S-14) − (vapour pressure head)

The deaerator operates at saturation. Its liquid is, by definition, at its boiling point at the vessel pressure. That means **the entire NPSHa for P-101B comes from the static elevation of the deaerator above the pump, minus every friction loss in the suction line.** There is no pressure margin from subcooling to draw on.

The available static head from the deaerator elevation is approximately 12.5 m water column. A differential of **0.2 bar** across a clean S-14 consumes about **2.0 m** of that. A differential of **0.6 bar** consumes about **6.1 m** — very nearly half of the total available head, gone into a fouled strainer basket.

| Condition | S-14 ΔP (bar) | Head lost at S-14 (m) | Approx. NPSHa at pump (m) | NPSHr at duty (m) | Margin (m) |
|---|---|---|---|---|---|
| Clean | 0.20 | 2.0 | 9.3 | 5.2 | 4.1 — healthy |
| Cleaning trigger | 0.35 | 3.6 | 7.7 | 5.2 | 2.5 — adequate |
| Alarm | 0.50 | 5.1 | 6.2 | 5.2 | 1.0 — **marginal** |
| **Current (≈0.6 bar)** | **0.60** | **6.1** | **5.2** | **5.2** | **≈ 0 — NO MARGIN** |

At the current condition there is essentially **no NPSH margin**. API 610 practice is to require a comfortable margin over NPSHr, and margin ratios of 1.1–1.3 (or a fixed margin of several metres, whichever is greater) are normal for hot BFW service specifically because the consequences of getting it wrong are so severe. Operating at a margin of zero means the pump is on the edge of incipient cavitation, and it will tip over that edge whenever the deaerator temperature rises — which happens on hot afternoons and on high steam demand.

### 5.2 Reduced flow

The strainer restriction directly reduces the flow the pump can draw. FT-101 has fallen from 236 m³/h to 149 m³/h steady-state, with excursions to 55–68 m³/h on hot afternoons. **Against a minimum continuous stable flow of 72 m³/h, those excursions put P-101B below its minimum flow limit.**

### 5.3 Downstream consequences on the pump

Low flow, once it occurs, produces a well-documented cascade on a multistage BFW pump:

- **Churn heating.** The pump absorbs shaft power regardless of how much useful hydraulic work it does. At very low flow, most of the absorbed power goes into heating the small amount of liquid trapped and recirculating inside the casing rather than leaving as useful head. The temperature rise per unit time is inversely proportional to the flow — halve the flow, roughly double the heating rate.
- **Suction and discharge recirculation.** Below about 50–60% of BEP, a vortex forms at the impeller eye and at the discharge vane tips. These recirculation cells are unsteady, produce high localised velocities, and are a recognised source of cavitation-like erosion damage on the pressure side of the vane inlet — damage that looks like cavitation but occurs at NPSHa values well above NPSHr.
- **Increased radial and axial loading.** Off-design operation loads the rotor asymmetrically, raising bearing loads and axial thrust and driving up vibration. The 2026 vibration surveys on P-101B record exactly this: broadband sub-synchronous energy and rising axial.
- **Bearing and seal chamber temperature rise.** The churn-heated liquid heats the casing, the seal chamber, and by conduction the bearing housings, showing up as an upward trend on **TE-101B**. The API 682 Plan 23 seal cooler has to absorb this extra heat, and if the cooler is itself fouled it cannot.
- **Reliance on MOV-118.** The minimum-flow recirculation valve MOV-118 exists to guarantee that at least 72 m³/h always passes through the pump by returning flow to the deaerator. This protection only works if MOV-118 actually opens. It is known to stick, particularly in summer.

**Summary of the chain: S-14 fouls → suction flow to P-101B falls and NPSH margin disappears → the pump runs below 72 m³/h minimum continuous flow, and MOV-118 does not reliably make up the shortfall → churn heating and internal recirculation → TE-101B bearing temperature trends up and the pump runs hot.**

---

## 6. Cleaning Procedure

**Prerequisite:** feedwater duty must be transferred to P-101A and the boiler load confirmed stable before P-101B is isolated. Note the site restart sequencing rule recorded in the operator log regarding order of pump restart and suction header cavitation.

1. **Permit and isolation.** Obtain a work permit. Confirm P-101B stopped, motor isolated and locked out, MOV-118 position confirmed. Close the suction isolation valve and the discharge isolation valve. Fit isolation tags.
2. **Depressurise and drain.** Vent through the strainer body vent connection. Confirm zero pressure at the local gauge, not just at PDI-S14. **The line contains water above 100 °C at operating conditions — allow it to cool below 60 °C before breaking containment, and drain to the closed drain header, not to grade.** Flashing hot condensate is the principal hazard on this job.
3. **Confirm zero energy.** Crack the cover bolts in a star pattern before full removal; confirm no residual pressure.
4. **Remove the cover.** Support the cover; it is heavy. Do not damage the gasket seating face.
5. **Withdraw the basket.** Lift the basket vertically with the handle. Do not drag it against the body seat — the seat is the seal between dirty and clean sides, and a scored seat allows bypass.
6. **Record before cleaning.** Photograph the basket in place and after removal. Record the debris type, quantity, and the approximate percentage of open area blinded. Retain a sample of any unusual debris for analysis — the debris population is the diagnostic evidence for where the contamination is coming from.
7. **Clean the basket.** Wash with clean water; use a soft brush. **Do not use a wire brush on the 316L basket** — it embeds carbon steel particles and initiates galvanic pitting. For adherent magnetite, ultrasonic cleaning or a citric-acid based descaling solution is acceptable, followed by thorough rinsing and passivation.
8. **Inspect the basket.** Check for perforation enlargement, tears, panel distortion, weld failure at the reinforcing ring, and damage to the sealing lip. **Any tear, however small, means the strainer is no longer protecting the pump — replace the basket, do not repair it.** A spare basket is held in stores; replace and clean the removed one off line rather than holding the outage.
9. **Clean the strainer body.** Remove any debris that has settled in the body below the basket seat.
10. **Reassemble.** Fit a new spiral-wound gasket — never reuse. Seat the basket squarely on the body seat. Torque the cover bolts in a star pattern to the specified value in two passes.
11. **Return to service.** Open the suction valve slowly and fill; vent air from the strainer body vent and from the pump casing high-point vent. **A strainer body that has not been vented will carry an air pocket straight into the pump suction and cause immediate vapour binding.** Then open the discharge valve, restore isolation, and remove tags.
12. **Verify and record.** Start the pump, allow to stabilise, and **record PDI-S14 at a known flow. The post-clean reading must be ≤ 0.25 bar at rated flow.** If it is not, the basket is still fouled, the seat is bypassing, or there is another restriction in the suction line — investigate before accepting the job as complete. Confirm FT-101 has recovered and confirm TE-101B settles back to its normal band.
13. **Close out.** Update the cleaning history table above with date, ΔP before/after, debris found, mass, and basket condition.

---

## 7. Recommendations

| # | Recommendation | Rationale | Priority |
|---|---|---|---|
| 1 | **Clean S-14 immediately.** The alarm has been standing since 2026-05-11 at ≈ 0.6 bar. | NPSH margin is effectively zero and the pump is being driven below minimum flow. | Immediate |
| 2 | Install a permanent bypass or a duplex (changeover) strainer arrangement on the P-101B suction. | Removes the pump-swap cost that causes cleaning to be deferred. This is the single highest-value modification available. | High — engineer for next shutdown |
| 3 | Set a **hard maximum cleaning interval of 6 months**, independent of ΔP, and treat the ΔP trigger as the earlier of the two. | Fouling is progressive and easy to normalise; a calendar backstop defeats deferral. | High |
| 4 | Escalate the PDI-S14 alarm to a shift-supervisor-acknowledged alarm with a mandatory action, so it cannot sit standing on the alarm list. | The alarm has become background noise. | High |
| 5 | Trend PDI-S14 against FT-101 as a normalised ratio on the DCS, so fouling is visible independent of load. | Raw ΔP is flow-dependent and masks early fouling at low load. | Medium |
| 6 | Investigate the continuing magnetite source — review deaerator oxygen scavenging control and layup practice. | Treating the strainer treats the symptom; the deaerator is the source. | Medium |
| 7 | Chemically clean or replace any remaining pre-commissioning mill scale burden in the suction piping at the next major outage. | Long-term elimination of the dominant debris class. | Low/long-term |
| 8 | Review whether the fine 40-mesh startup screen is still fitted. If it is, it must be removed for normal operation — it is a startup item only and will foul rapidly. | Common cause of unexplained high ΔP. | Verify at next clean |

---

*Related documents: P-101B compiled inspection reports; 2023 P-101B seal failure incident report; BFW pump lessons learned; operator shift handover log. Reference is also made to strainer arrangements on P-101A and P-102, which are duplex type and do not exhibit this deferral problem.*
