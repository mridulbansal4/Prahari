# Incident Report — Mechanical Seal and Bearing Failure, P-101B

**Report Number:** INC-2023-0814-P101B
**Classification:** Equipment Damage / Production Impact — no injury, no loss of containment to atmosphere beyond localised steam release
**Asset:** P-101B — Boiler Feed Pump B, multistage centrifugal boiler feed water pump
**Date of Failure:** 2023-08-14
**Date of Report Issue:** 2023-09-06
**Revision:** Rev 2 (2023-10-02 — corrective action dates updated after review)
**Investigation Team:** Rotating Equipment Engineer (lead), Shift Superintendent, Instrument Engineer, Reliability Engineer, Utilities Operations Supervisor
**Investigation Method:** Timeline reconstruction, DCS historian data retrieval, component teardown and failure surface examination, 5-Whys root cause analysis

---

## 1. Incident Summary

On 2023-08-14, boiler feed pump **P-101B** suffered a catastrophic failure of its mechanical seal accompanied by severe damage to the thrust bearing and measurable damage to the inboard radial sleeve bearing. The failure released hot boiler feed water as flashing steam at the gland, tripped the pump on high vibration, and forced an unplanned reduction in boiler load while feedwater duty was transferred to P-101A.

The immediate physical cause was **dry running and thermal distress of the mechanical seal faces**, following loss of the liquid film between the faces. The underlying cause was **prolonged operation of P-101B below its minimum continuous stable flow of 72 m³/h**, which produced churn heating of the liquid in the casing and seal chamber, degraded the API 682 Plan 23 seal flush loop's ability to reject that heat, and eventually allowed the liquid in the seal chamber to flash.

Two independent protection layers that should have prevented this both failed to function:

1. **MOV-118**, the minimum-flow recirculation valve, did not open when it was commanded. It was found mechanically stuck.
2. **Suction strainer S-14** was heavily fouled, restricting suction flow and reducing NPSH available, so the pump could not draw its rated flow even with the discharge path open.

A third factor — the **TE-101B bearing temperature indication reading approximately 5% high** — meant that operators had, over a period of months, learned to mentally discount high temperature readings on this machine, which reduced the perceived significance of the rising trend in the days before the failure.

There were **no injuries**. One operator was in the vicinity at the time of the gland release and withdrew without harm. The area was barriered within four minutes.

---

## 2. Equipment and Process Context

| Item | Detail |
|---|---|
| Pump | P-101B, 6-stage horizontal multistage BFW pump, API 610 type BB4 |
| Rated / BEP flow | 240 m³/h |
| **Minimum continuous stable flow** | **72 m³/h (30% of BEP)** |
| Rated differential head | 1,180 m |
| Driver | 900 kW, 2-pole induction motor, 2,970 rpm nominal |
| Seal | Single cartridge, balanced, SiC vs carbon faces |
| **Seal flush plan** | **API 682 Plan 23** — closed-loop recirculation from seal chamber via pumping ring through seal cooler and back |
| Bearings | Radial: hydrodynamic sleeve. Thrust: tilting pad |
| Minimum-flow protection | MOV-118 recirculation valve to deaerator, auto-open on low flow from FT-101 |
| Suction protection | Suction Strainer S-14, monitored by PDI-S14 |
| Key instruments | TE-101B (bearing temp), VE-101B (vibration), PT-101 (discharge pressure), FT-101 (flow) |
| Parallel pump | P-101A |

**Documented temperature limits (note the inconsistency, which is itself a finding):** the operating manual states a bearing temperature alarm of **85 °C**. The vendor datasheet states **90 °C alarm and 100 °C trip**. The DCS was configured to the datasheet values. This discrepancy had existed since commissioning and was not resolved.

**Operating context in the days before the incident:** the site was in a period of high ambient temperature (daily maxima 41–44 °C) and high steam demand. Deaerator storage temperature was running at the top of its normal band, which reduces NPSH available. P-101B was the running BFW pump; P-101A was on hot standby. Unrelated equipment P-102 and E-301 were in normal service and had no bearing on this event.

---

## 3. Timeline of Events

All times are local. Data from the DCS historian at 1-minute resolution, cross-checked against the shift log and operator interviews.

### Pre-incident period

| Date | Event |
|---|---|
| 2023-02-14 | S-14 cleaned. PDI-S14 restored from 0.55 bar to 0.23 bar. Basket found locally distorted and replaced. |
| 2023-04 to 2023-07 | PDI-S14 trends steadily upward. Logged in shift notes; no cleaning work order executed because cleaning requires a pump swap. |
| 2023-06-20 | Shift note records MOV-118 "slow to open, had to hand-wind it" during a routine low-load period. No work order raised. |
| 2023-07-11 | PDI-S14 exceeds 0.5 bar alarm. Alarm acknowledged. Cleaning deferred to "next opportunity". |
| 2023-07 onward | FT-101 shows increasingly frequent afternoon excursions below 100 m³/h. TE-101B daily peak rises from 76 °C to 84 °C across the month. Operators note that P-101B "always runs hot on hot afternoons" and treat the readings as normal, partly because TE-101B is known to read high. |
| 2023-08-11 | TE-101B afternoon peak 88 °C. Above the operating manual's 85 °C alarm, below the DCS-configured 90 °C alarm. No alarm annunciated. No action. |
| 2023-08-12 | Routine vibration route data taken. Outboard radial 5.8 mm/s RMS — **ISO 20816-3 Zone C**. Report filed but not escalated; the route report was not reviewed until after the failure. |
| 2023-08-13 | PDI-S14 at 0.61 bar. FT-101 afternoon minimum 61 m³/h — **below the 72 m³/h minimum continuous flow.** MOV-118 commanded open by the low-flow logic. Valve position feedback shows it moved 6% and stopped. No valve-fault alarm was configured on position deviation. |

### Day of failure — 2023-08-14

| Time | Event |
|---|---|
| 06:00 | Night shift hands over. Log entry notes S-14 ΔP high, P-101B "warm but OK", MOV-118 "sticky, keep an eye". |
| 09:30 | Ambient 34 °C and rising. FT-101 = 142 m³/h. TE-101B = 79 °C. Seal chamber temperature (local gauge, spot read) 91 °C. |
| 12:40 | Ambient 42 °C. Steam demand peaks. FT-101 falls to 96 m³/h. TE-101B = 85 °C. |
| 13:15 | FT-101 = 74 m³/h. Low-flow logic commands MOV-118 open. **Valve position feedback rises to 7% and stalls.** No fault alarm configured. Recirculation flow essentially nil. |
| 13:22 | FT-101 = **68 m³/h — below minimum continuous stable flow of 72 m³/h.** Pump now in the churn regime. |
| 13:22 – 14:48 | **86 minutes of continuous operation below minimum flow.** FT-101 continues to decay, reaching 54 m³/h at 14:30. TE-101B climbs from 85 °C to 93 °C. PT-101 becomes unsteady, oscillating ±0.8 bar around the mean, consistent with internal recirculation. VE-101B broadband rises from 5.6 to 7.9 mm/s RMS. |
| 14:05 | DCS high bearing temperature alarm (90 °C, datasheet value) annunciates. Operator acknowledges. Interview record: the operator interpreted the reading as the known high-side error on TE-101B combined with the known hot-afternoon behaviour, estimated the true value at around 88 °C, and judged it as "hot but within the 100 °C trip". No corrective action taken. |
| 14:33 | Seal chamber liquid reaches saturation at seal chamber pressure. Faces begin to run on vapour. Local audible change reported by an operator on rounds ("a dry whistling"). |
| 14:41 | Visible vapour plume at the gland. Operator reports to control room. |
| 14:46 | VE-101B exceeds 9 mm/s. Rapid rise. |
| 14:48 | **Seal fails completely.** Gross release of flashing hot feed water at the gland. Pump trips on high vibration at 11.4 mm/s. Motor de-energised. |
| 14:49 | Control room initiates start of P-101A. Boiler load reduced by 35% to protect drum level. |
| 14:52 | Area barriered. Operator on rounds accounted for, uninjured. |
| 14:58 | P-101A established on load. Drum level recovered. Boiler load restored to 80% by 15:20. |
| 15:30 | P-101B isolated, locked out, allowed to cool. |
| 16:10 | Initial walkdown. Gland area, coupling guard, and baseplate soaked. No fire, no secondary damage. |
| 2023-08-17 | Teardown inspection commenced. |
| 2023-08-18 | S-14 opened. **3.4 kg of debris recovered — magnetite, mill scale, deaerator corrosion products. Approximately 25% of the basket open area blinded.** PDI-S14 after cleaning: 0.20 bar. |
| 2023-08-19 | MOV-118 removed and stripped. Stem found galled, gearbox grease degraded and hardened, valve seized in the near-closed position. |

---

## 4. Immediate Actions Taken

1. Pump tripped automatically on high vibration; motor confirmed isolated and locked out.
2. P-101A started and established on feedwater duty within 10 minutes; boiler drum level maintained within limits throughout. No boiler trip occurred.
3. Boiler load reduced 35% as a precaution, restored progressively over 30 minutes.
4. Area barriered and personnel withdrawn from the release zone.
5. Suction and discharge isolation of P-101B closed; unit depressurised and allowed to cool before any intervention.
6. DCS historian data secured and exported before the retention window could roll.
7. Incident notified to the plant manager and logged in the incident management system the same day.
8. A standing instruction was issued that evening prohibiting operation of P-101B below 100 m³/h pending investigation.

---

## 5. Damage Assessment

### 5.1 Mechanical seal

- **Carbon primary ring:** heavily heat-checked with a network of radial thermal cracks across the face. Face width had worn irregularly. Classic dry-running thermal distress signature.
- **Silicon carbide mating ring:** surface crazing and a circumferential heat band. Two radial cracks propagating from the OD. The SiC face had been thermally shocked when liquid re-entered the face gap intermittently.
- **Elastomer secondary seals:** the dynamic O-ring was hardened, compression-set, and had lost sealing capability. Colour change indicated exposure well above its continuous rating.
- **Drive lugs:** fretted, with visible material transfer, consistent with the seal faces losing hydraulic balance and the rotating assembly hammering.
- **Springs:** intact, no relaxation, no breakage.
- **Conclusion:** the seal failed from loss of the liquid film between the faces. It did not fail from wear, from debris in the faces, or from mechanical damage during installation.

### 5.2 Plan 23 seal flush loop

- **Seal cooler:** heavily fouled on the water side. Measured ΔT across the cooler in the days before the failure was 9 K against a design of approximately 40 K — the cooler was delivering less than a quarter of its design duty.
- **Pumping ring:** intact and correctly clearanced. Not the cause. However, a pumping ring's circulation rate falls with reduced pressure differential and it is not designed to sustain circulation against a fouled cooler.
- **Loop piping:** partially scaled, no blockage.

### 5.3 Thrust bearing

- **Tilting pads:** three of the six active-side pads showed **wiped babbitt**, with material displaced to the trailing edge. Two pads showed the discoloration band typical of overheating. Pad thickness reduced by 0.11 mm on the worst pad.
- **Thrust collar:** scored, requiring re-machining and re-grinding.
- **Cause:** combined effect of elevated oil temperature (thinning the oil film) and elevated axial thrust from off-design operation. A multistage pump's axial thrust balance is designed around the design-point pressure distribution; at 25% of BEP the balance device leak-off geometry no longer balances the rotor correctly.

### 5.4 Radial sleeve bearings

- **Inboard:** measurable babbitt wear, clearance opened from 0.15 mm to 0.24 mm. Light wiping on the loaded arc. Replaced.
- **Outboard:** within limits, light polishing only. Replaced as a precaution given the shaft was out.

### 5.5 Other components

- **Shaft:** runout within tolerance at 0.02 mm. Sleeve under the seal showed a light heat band; sleeve replaced, shaft accepted.
- **Impellers and wear rings:** wear ring clearances measured at 0.51–0.58 mm against a design of 0.35 mm — opened up, consistent with debris passage and with periods of off-design operation. All wear rings renewed.
- **Casing:** pressure boundary sound. Hydrotested and accepted. No cracking, no erosion of the pressure boundary.
- **Balance drum / balance line:** balance line partially restricted with debris; cleaned.
- **Motor:** no damage. Insulation resistance and polarisation index satisfactory. Bearings inspected and re-greased as a precaution.
- **MOV-118:** stem galled, actuator gearbox lubricant hardened and carbonised, valve seized. Actuator torque switch had tripped and latched without generating a DCS alarm because **no position-deviation or valve-fault alarm was configured**.

---

## 6. Root Cause Analysis — 5 Whys

**Problem statement:** On 2023-08-14 the mechanical seal and thrust bearing of P-101B failed catastrophically, causing a hot water release and an unplanned load reduction.

---

**WHY 1 — Why did the mechanical seal fail?**

Because the liquid film between the seal faces was lost and the faces ran dry. The carbon face is heat-checked and the SiC face is crazed — both are dry-running signatures, not wear or debris signatures.

*Evidence:* teardown examination of both faces; hardened and compression-set dynamic O-ring; fretted drive lugs.

---

**WHY 2 — Why was the liquid film between the faces lost?**

Because the boiler feed water in the seal chamber reached its saturation temperature at seal chamber pressure and flashed to vapour. Two effects combined to raise the seal chamber temperature: heat generated inside the pump casing by operating far below design flow, and loss of heat removal capacity because the API 682 Plan 23 seal cooler was fouled.

*Evidence:* seal chamber temperature climbing through the shift; cooler ΔT of 9 K against a design 40 K; heavy waterside fouling found on teardown; the pump's own casing temperature rising in step with falling flow.

---

**WHY 3 — Why did the seal chamber overheat?**

Because P-101B operated continuously for 86 minutes below its minimum continuous stable flow of 72 m³/h, reaching a low of 54 m³/h. At these flows the pump absorbs shaft power that it cannot convert into useful hydraulic work; that power is dissipated as heat into the small mass of liquid recirculating inside the casing. Heating rate is inversely proportional to flow, so the temperature rise accelerated as flow decayed. Internal suction and discharge recirculation further raised local temperatures and produced the unsteady discharge pressure and broadband vibration recorded on PT-101 and VE-101B.

*Evidence:* FT-101 historian trace 13:22–14:48; PT-101 oscillation of ±0.8 bar; VE-101B broadband rise from 5.6 to 11.4 mm/s; TE-101B rise from 85 °C to 93 °C over the same window.

---

**WHY 4 — Why was the pump allowed to run below minimum continuous flow?**

Because the minimum-flow protection did not function. **MOV-118, the minimum-flow recirculation valve, was commanded open at 13:15 and did not open** — it travelled 7% and stalled, and it was found on strip-down to be mechanically seized with a galled stem and hardened, carbonised actuator gearbox lubricant. Because there was **no position-deviation alarm and no valve-fault alarm configured**, the control system did not tell anyone that the protection had failed. The system reported "command sent" and nothing reported "command not achieved".

*Evidence:* MOV-118 position feedback trace; teardown of stem and actuator; DCS alarm configuration review confirming no deviation alarm existed; shift note of 2023-06-20 recording the valve as "slow to open, had to hand-wind it" with no work order raised.

---

**WHY 5 — Why was the flow to P-101B low enough for the minimum-flow protection to be needed at all, and why had MOV-118 been left in a condition where it could seize?**

Two converging answers:

**(a) The flow was low because suction strainer S-14 was heavily fouled.** PDI-S14 had risen from a clean 0.2 bar to 0.61 bar, past the 0.5 bar alarm, over a period of months. That restriction consumed roughly half the total available NPSH from the deaerator elevation and throttled the flow the pump could draw. The fouling was known, was alarmed, was logged repeatedly in shift notes, and was not cleaned — because S-14 has no bypass, so cleaning it requires taking P-101B out of service and swapping to P-101A, and that swap was repeatedly judged not worth the disruption.

**(b) MOV-118 was in a degraded state because it was not on any preventive maintenance or proof-test schedule as a protective device.** It was treated as an ordinary control valve. Because it is a rarely-actuated protection element, it sat in one position for long periods and its stem galled and its gearbox lubricant degraded without anyone exercising or inspecting it. A known symptom — the June 2023 sticking report — was logged conversationally and never became a work order.

**Underlying both:** the statutory **OISD periodic inspection of P-101B, required at intervals not exceeding 12 months, was last performed on 2019-03-11 and was already more than four years overdue at the time of this incident.** That inspection scope includes functional verification of protective trips, alarms, and minimum-flow protection. Had it been performed on schedule, MOV-118 would have been proof-tested and its condition found, and the S-14 fouling trend would have been formally assessed. The inspection had been deferred repeatedly without a closed-out deferral risk assessment.

---

### 6.1 Root Cause Statement

**Primary root cause:** Failure of the minimum-flow protection function for P-101B. MOV-118 was mechanically seized and unable to open, and its failure was undetectable because no valve position-deviation or fault alarm was configured. The protective function was neither maintained as a protective device nor proof-tested.

**Contributing root cause:** Progressive fouling of suction strainer S-14, unaddressed despite a standing high-differential alarm, which reduced flow to the pump and reduced NPSH available, creating the low-flow condition that the failed protection was supposed to handle.

**Systemic root cause:** Lapse of the statutory OISD periodic inspection regime for P-101B — last performed 2019-03-11 against a required 12-month interval — which removed the scheduled opportunity to detect both of the above.

---

## 7. Contributing Factors

| # | Factor | How it contributed |
|---|---|---|
| C1 | **TE-101B reads approximately 5% high** (verified later against a portable pyrometer). Never formally corrected or documented. | Operators had learned to discount high readings on this instrument. At 14:05 the operator mentally corrected 93 °C down to ~88 °C and judged it acceptable. The correction was directionally right but the conclusion was wrong. |
| C2 | **Conflicting temperature limits.** Operating manual says 85 °C alarm; datasheet says 90 °C alarm / 100 °C trip. DCS configured to the datasheet. | The 2023-08-11 peak of 88 °C exceeded the manual's limit but annunciated nothing. A whole day of early warning was lost. |
| C3 | **Normalisation of deviance.** "P-101B always runs hot on hot afternoons" had become accepted shift knowledge. | A genuine and worsening signal was reclassified as a harmless quirk of the machine. |
| C4 | **Standing PDI-S14 alarm.** The S-14 high-differential alarm had been standing since 2023-07-11. | Chronic standing alarms lose their power to prompt action and clutter the alarm list. |
| C5 | **No bypass on S-14.** Cleaning requires a pump swap. | Made the correct action expensive, which made deferral rational at each individual decision point and cumulatively disastrous. |
| C6 | **PdM route report of 2023-08-12 showing ISO 20816-3 Zone C was not reviewed before the failure.** | Two days of warning at a clearly unsatisfactory vibration level went unactioned. The data existed; the review loop did not close. |
| C7 | **MOV-118 not classified as a protective device.** Not on a proof-test schedule. | A safety-relevant function was maintained to a non-safety standard. |
| C8 | **June 2023 sticking report not converted to a work order.** | The single clearest advance warning was lost in a conversational log entry. |
| C9 | **High ambient temperature (42 °C) and high deaerator temperature.** | Reduced NPSH margin further and increased seal cooler inlet temperature, accelerating the failure. Note that MOV-118 is reported to stick preferentially in summer. |
| C10 | **Fouled Plan 23 seal cooler, not on a cleaning schedule.** | Removed the last line of defence that could have kept the seal chamber below flash. |

---

## 8. Cost and Downtime

| Item | Value |
|---|---|
| P-101B out of service | 2023-08-14 to 2023-09-22 — **39 days** |
| Boiler load reduced (35%) | 46 minutes |
| Single-pump (no standby) exposure while P-101B was down | 39 days — significant availability risk |
| Mechanical seal cartridge (replacement) | ₹ 8,60,000 |
| Thrust bearing pad set and collar re-machining | ₹ 6,40,000 |
| Radial sleeve bearings (2 sets) | ₹ 2,10,000 |
| Wear rings, interstage bushings, shaft sleeve | ₹ 9,80,000 |
| MOV-118 refurbishment (stem, gearbox, actuator service) | ₹ 3,25,000 |
| Seal cooler cleaning and retube of two tubes | ₹ 1,45,000 |
| S-14 basket and cleaning | ₹ 55,000 |
| Workshop labour and site labour | ₹ 7,20,000 |
| Vendor site support (2 engineers, 9 days) | ₹ 5,90,000 |
| Freight, expediting on long-lead seal | ₹ 2,30,000 |
| **Total direct maintenance cost** | **₹ 47,55,000** |
| Estimated production loss (load reduction + de-rate during single-pump operation) | **₹ 31,00,000** |
| **Total estimated cost of the event** | **≈ ₹ 78,55,000** |

For comparison, cleaning S-14 on schedule and proof-testing MOV-118 annually would have cost under ₹ 2,00,000 per year including the pump swap.

---

## 9. Corrective and Preventive Actions

| # | Action | Type | Owner | Target date | Status at Rev 2 |
|---|---|---|---|---|---|
| A1 | Rebuild P-101B: new seal cartridge, thrust pads, collar, radial bearings, wear rings, sleeves, balance line clean. Full alignment and run-in. | Corrective | Rotating Equipment Engineer | 2023-09-22 | Complete |
| A2 | Refurbish MOV-118: new stem, re-lubricate and overhaul actuator gearbox, verify full stroke and torque switch setting. | Corrective | Valves/Instrument Engineer | 2023-09-15 | Complete |
| A3 | Clean S-14 and fit new basket. Restore PDI-S14 to ≤ 0.25 bar. | Corrective | Maintenance Planner | 2023-08-18 | Complete |
| A4 | Clean the API 682 Plan 23 seal cooler; verify ΔT ≥ 35 K on return to service. | Corrective | Maintenance Planner | 2023-09-20 | Complete |
| A5 | **Configure a MOV-118 position-deviation alarm** on the DCS: alarm if commanded open and position < 80% after 60 s. | Preventive | Instrument Engineer | 2023-09-30 | Complete |
| A6 | **Classify MOV-118 as a protective device** and place it on a documented annual proof-test schedule with a full stroke test, recorded stroke time, and torque verification. Add a partial-stroke exercise every 3 months. | Preventive | Reliability Engineer | 2023-10-31 | In progress |
| A7 | **PROPOSED — not implemented. Does not describe the current configuration.** Add a low-flow protective trip on P-101B: trip the pump if FT-101 < 72 m³/h for more than 120 s continuously, with a pre-trip alarm at 90 m³/h. The setpoints in force today remain those in `operating_manual_P-101B.md`; this proposal would tighten them and requires MOC approval before any change. | Preventive | Process/Control Engineer | 2023-11-30 | In progress — awaiting MOC |
| A8 | **Calibrate TE-101B and formally document the offset.** Instrument reads ~5% high. Either correct the loop or record the correction in a controlled document so it is not carried only as tribal knowledge. | Preventive | Instrument Engineer | 2023-10-15 | In progress |
| A9 | **Resolve the conflicting alarm/trip limits.** Reconcile the operating manual (85 °C alarm) against the datasheet (90 °C alarm, 100 °C trip) into a single controlled setpoint document. Update the DCS and the manual to match. | Preventive | Rotating Equipment Engineer | 2023-11-15 | In progress |
| A10 | **Escalate the PDI-S14 alarm** to require shift-supervisor acknowledgement with a mandatory recorded action. No standing alarms permitted beyond 7 days without a raised work order. | Preventive | Operations Superintendent | 2023-10-31 | In progress |
| A11 | Set a **hard maximum cleaning interval of 6 months for S-14** independent of differential pressure. | Preventive | Maintenance Planner | 2023-10-15 | Complete |
| A12 | **Engineer a duplex or bypassed strainer arrangement for the P-101B suction** so cleaning no longer requires a pump swap. | Preventive | Projects Engineer | Next major shutdown | Open |
| A13 | Add the **seal cooler to a 6-monthly cleaning schedule** with a mandatory ΔT verification on return to service. | Preventive | Maintenance Planner | 2023-10-31 | Complete |
| A14 | **Mandatory same-week review of PdM route reports.** Any ISO 20816-3 Zone C result must be escalated to the Rotating Equipment Engineer within 48 hours with a written response. | Preventive | Reliability Engineer | 2023-10-31 | In progress |
| A15 | **Re-establish the OISD statutory periodic inspection programme for P-101B and all critical BFW pumps.** Required interval 12 months. Last P-101B statutory inspection 2019-03-11 — over four years overdue. Any deferral must carry a signed deferral risk assessment; breakdown work orders do not satisfy the statutory requirement. | Preventive | Inspection Engineer | 2023-12-31 | **Open — escalated** |
| A16 | Add minimum-flow theory and the churn-heating mechanism to operator training. Include the specific 72 m³/h figure for P-101B. | Preventive | Training Coordinator | 2023-12-15 | In progress |
| A17 | Review restart sequencing practice for P-101A / P-101B after a shutdown and capture the correct sequence in a written operating procedure rather than leaving it as verbal shift knowledge. | Preventive | Operations Superintendent | 2023-12-15 | In progress |

---

## 10. Lessons Learned

1. **A protective device that cannot be proven to work is not a protective device.** MOV-118 was the designed defence against exactly the condition that destroyed the pump. It was maintained as an ordinary valve, never proof-tested, and — critically — engineered such that its failure was silent. "Command sent" is not "function achieved". Any protective final element needs a feedback path that alarms when the function does not complete.

2. **Deferred cheap maintenance becomes expensive maintenance, and the accounting is invisible at the moment of deferral.** Every individual decision not to clean S-14 was locally reasonable: a pump swap for a strainer clean. Cumulatively those decisions cost ₹ 78 lakh. The absence of a bypass turned a trivial job into a consequential one, and the design decision to omit that bypass is the real origin of the deferral behaviour.

3. **Standing alarms are not alarms.** PDI-S14 had been in alarm for over a month. An alarm that is always on carries no information and trains operators to ignore the panel. Alarm management discipline — every standing alarm gets a work order or a documented suppression with an expiry — is a reliability control, not an administrative chore.

4. **Undocumented instrument error is a latent operational hazard.** The knowledge that TE-101B reads about 5% high was real, correct, and useful. But because it lived only in operators' heads rather than in a controlled document or in the loop calibration, it functioned as a licence to discount high readings generally. Tribal knowledge that is correct can still cause harm when it is applied as a general heuristic instead of a specific correction.

5. **Conflicting documents are worse than a single wrong document.** With the manual saying 85 °C and the datasheet saying 90 °C, the effective limit became whichever number supported continuing to run. Every setpoint should have exactly one controlled source.

6. **"It always does that" deserves investigation, not acceptance.** "P-101B runs hot on hot afternoons" was an accurate observation of a real and worsening degradation mechanism, reclassified by familiarity into a harmless personality trait of the machine. Normalisation of deviance is not a failure of intelligence; it is what happens by default when a signal changes slowly.

7. **Condition monitoring data has no value until someone reads it.** A Zone C vibration result existed two days before the failure. The measurement system worked perfectly. The review loop did not exist. Data collection and data review are separate capabilities and both must be resourced.

8. **Small process changes propagate a long way in a tightly coupled system.** A fouled basket in a suction line destroyed a mechanical seal six stages downstream. The causal distance between symptom and cause on BFW pumps is routinely large, and troubleshooting that starts at the seal will never find the strainer.

9. **Statutory inspection intervals exist because they force the periodic examination of things nobody is looking at.** The overdue OISD inspection was not a paperwork failure — it was the loss of the one scheduled event that would have proof-tested MOV-118 and formally assessed the S-14 trend. Breakdown maintenance does not substitute for it and must never be allowed to close out a statutory record.

---

**Report approved:**
Rotating Equipment Engineer — 2023-09-06
Utilities Operations Superintendent — 2023-09-07
Plant Reliability Manager — 2023-09-08
Rev 2 issued 2023-10-02

*Related documents: P-101B compiled inspection reports; S-14 maintenance and condition history; BFW pump lessons learned; operator shift handover log.*
