# Lessons Learned — Boiler Feed Water Pumps

**Scope:** Systemic reliability lessons across boiler feed water (BFW) pump service at this site and from published industry failure-mode experience
**Applicable assets:** P-101A, P-101B, and by extension all multistage BFW pumps in utilities service. References to P-102 (condensate transfer), E-301 (LP feedwater heater), and V-201 (knockout drum) are contextual only.
**Issue date:** 2026-07-21
**Owner:** Plant Reliability Engineering
**Status:** Living document — reviewed annually and after every BFW pump event

---

## 1. Why BFW Pumps Fail Differently

Boiler feed water pumps are among the least forgiving machines in a process plant, and they fail for reasons that are largely *not* the reasons general-service pumps fail. Understanding why is the foundation of every lesson in this document.

Four characteristics drive this:

**High energy density.** A multistage BFW pump concentrates several hundred kilowatts to a megawatt or more into a rotor of modest mass. P-101B absorbs around 900 kW at rated duty. Any fraction of that power not converted into useful hydraulic work becomes heat, and it becomes heat *inside* a small volume of liquid. There is very little thermal inertia to absorb a mistake.

**Zero suction subcooling.** BFW pumps take suction from a deaerator, which operates at saturation. The liquid at the pump suction is, by definition, at its boiling point. All of the NPSH available comes from the static elevation of the deaerator above the pump, minus friction losses. There is no pressure margin from subcooling to fall back on. This makes BFW pumps uniquely sensitive to *any* additional suction-side restriction — a fouling suction strainer that would be a nuisance elsewhere is a threat here.

**Tight internal clearances.** Wear rings, interstage bushings, and balance drums run at diametral clearances in the 0.30–0.45 mm range. Debris that passes harmlessly through a general-service pump opens these clearances up permanently. Once opened, the pump loses head, loses efficiency, and — importantly — becomes hydraulically less stable, which pushes it further off design.

**Design-point-dependent axial thrust balance.** The balance drum or balance disc that offsets the axial thrust of a multistage rotor is sized against the design-point pressure distribution across the stages. Move the pump substantially off BEP and that pressure distribution changes, the balance no longer balances, and the residual thrust lands on the thrust bearing.

The consequence of all four together: **the dominant BFW pump failure mode is not a worn part. It is an operating condition — sustained off-design flow — that then destroys parts.** Published rotating-equipment failure studies consistently attribute the largest share of centrifugal pump failures to seal and bearing distress, and for BFW service specifically, the majority of those seal and bearing failures trace back to off-design hydraulics rather than to a defect in the seal or bearing itself. Replacing the seal without addressing the flow is a repair that guarantees a repeat.

---

## 2. Standards and Reference Practice (paraphrased)

The following are summarised in the reliability team's own words. Refer to the controlled copies for the actual requirements.

**API 610 (centrifugal pumps for petroleum, petrochemical and natural gas industries)** establishes the concept of a preferred operating region around BEP and a minimum continuous stable flow below which the pump should not be run. The standard requires vendors to state both, and requires that the system be designed so the pump is not driven below the stated minimum. It also addresses NPSH margin — the point being that meeting NPSHr on paper is not sufficient; a margin above it is required, and for hot, high-energy service that margin should be generous. API 610 further addresses vibration acceptance at test and in the field, allowable nozzle loads, and baseplate/foundation requirements.

**API 682 (pumping system shaft sealing for centrifugal and rotary pumps)** defines the standard piping plans for seal flush and support. The plans relevant to BFW service:
- **Plan 23** — the correct default for hot water. A pumping ring circulates a small closed volume from the seal chamber, through a cooler, and back. Because it recirculates the same cool liquid rather than continuously introducing hot product, it is thermally efficient. Its weakness is total dependence on the cooler: if the cooler fouls, the plan silently stops working, and there is no direct indication that it has.
- **Plan 21** — flush from discharge through a cooler into the seal chamber. Thermally wasteful compared with Plan 23 and generally superseded for hot service.
- **Plan 32** — clean external injection. Used where product cleanliness is inadequate; introduces external water into the process, which is often unacceptable in a BFW loop for chemistry reasons.
- **Plan 52 / 53** — buffer or barrier fluid systems for dual seals, used where leakage cannot be tolerated.
API 682 also sets out the qualification testing, face material combinations, and the expectation of a defined seal reliability life.

**ISO 20816-3** (which supersedes ISO 10816-3) gives the evaluation of machine vibration by measurement on non-rotating parts for industrial machines. It classifies measured broadband RMS velocity into four zones: **Zone A** for newly commissioned machines; **Zone B** acceptable for unrestricted long-term operation; **Zone C** unsatisfactory for continuous operation, tolerable only for a limited period while a corrective opportunity is arranged; **Zone D** severe enough to cause damage. For the machine group and support class covering our BFW pumps, the A/B boundary is 2.8 mm/s RMS, B/C is 4.5 mm/s RMS, and C/D is 7.1 mm/s RMS. The standard also provides for evaluation against a *change* in vibration, not just an absolute level — a rise of 25% of the B/C boundary is significant even if the absolute level is still acceptable. **This change criterion is more useful than the absolute criterion for BFW pumps and is under-used at this site.**

**OISD** standards govern the site's mechanical integrity and inspection programme. Critical rotating equipment in this service requires **documented statutory periodic inspection at intervals not exceeding 12 months**, covering pressure-boundary integrity, foundation and holding-down arrangements, guarding, seal support system integrity, and — the clause that matters most for the lessons in this document — **functional verification of protective trips, alarms, and minimum-flow protection.**

---

## 3. Pattern Table — Recurring BFW Pump Failure Patterns

| # | Pattern | Mechanism | Leading indicators | Typical detection failure | Consequence |
|---|---|---|---|---|---|
| P1 | **Minimum-flow protection failure** | Recirculation valve fails to open on demand; pump runs below minimum continuous stable flow; churn heating and internal recirculation | Valve position feedback not matching command; stroke time creeping up; operator reports of "sticky" valve; flow dipping below minimum with no recirculation flow | Valve treated as a control valve rather than a protective device; no position-deviation alarm; no proof-test schedule; "command sent" logged as success | Seal flash and dry running; thrust bearing wipe; rapid catastrophic failure |
| P2 | **Suction strainer fouling** | Progressive blinding of basket by magnetite, mill scale, weld slag; ΔP rises; NPSH available collapses; flow throttled | Differential pressure trending upward; flow falling at constant demand; NPSH margin shrinking; suction pressure gauge falling | Strainer has no bypass, so cleaning costs a pump swap and gets deferred; ΔP alarm stands permanently and stops carrying information | Low-flow operation, cavitation risk, wear ring damage from any debris that does pass |
| P3 | **Seal flush cooler fouling (Plan 23)** | Waterside scaling and fouling of the seal cooler reduces heat rejection; seal chamber temperature climbs toward saturation | Cooler ΔT falling well below design; seal chamber temperature rising; occasional weeping at the gland that clears when hot | The Plan 23 loop has no flow or temperature instrumentation, so its degradation is completely invisible until the seal fails; cooler not on any cleaning schedule | Seal chamber liquid flashes; faces run dry; heat-checked carbon and crazed SiC |
| P4 | **Thermal soak on hot standby** | Standby pump sits full of hot water with no flow; casing, seal chamber and bearing housings soak to line temperature; seal faces sit hot and static | Standby pump bearing temperature approaching that of the running pump; no warming-line flow indication | Standby machines are outside the normal monitoring routine; nobody trends a pump that isn't running | Seal degradation without ever running; rotor bow; a standby pump that fails on the day it is needed |
| P5 | **Restart sequencing error** | Two pumps on a shared suction header restarted in the wrong order; transient pressure drop in the header starves the second pump; vapour formation | Suction pressure transient on the header at restart; audible cavitation; brief vibration spike at start-up | The correct sequence exists only as verbal shift knowledge, not as a written procedure; new operators do not inherit it reliably | Cavitation damage to impeller vane inlets; wear ring damage; occasional immediate trip |
| P6 | **Instrument drift** | Bearing temperature or flow instrument reads consistently off; operators learn the offset informally and apply it as a general discount | Persistent discrepancy between DCS indication and portable instrument checks; operator comments in shift logs | The offset lives in operators' heads, not in the loop calibration or any controlled document; it is correct information stored in the wrong place | High readings mentally discounted, including genuine ones; delayed response to a real excursion |
| P7 | **Conflicting documented setpoints** | Operating manual and vendor datasheet state different alarm/trip limits; DCS configured to one of them | Two different numbers found when anyone actually checks | Nobody checks until after an event; the effective limit becomes whichever number supports continuing to run | Warnings that should have annunciated do not; a whole band of early warning is lost |
| P8 | **Wear ring clearance opening** | Debris passage and off-design operation erode wear rings; internal recirculation increases; head and efficiency fall | Falling discharge pressure at constant speed and flow; rising power per unit of delivered head; efficiency drift | Performance degradation is slow and gets absorbed by control loops opening valves further; no one trends pump efficiency | Pump progressively less able to make duty; drifts further off design; a self-reinforcing loop |
| P9 | **Standing alarm normalisation** | A chronic alarm remains active for weeks; operators acknowledge and ignore; the alarm list is cluttered | A single alarm point in continuous alarm state | No governance rule limiting how long an alarm may stand; no requirement to raise a work order | Real alarms lost in the noise; the specific degradation the alarm was designed to catch proceeds unchecked |
| P10 | **Condition data collected but not reviewed** | PdM route data taken on schedule, filed, and not analysed until after a failure | A Zone C report sitting unread in the PdM system | Data *collection* is resourced and scheduled; data *review* is not; they are treated as one activity when they are two | Days or weeks of clear advance warning wasted |
| P11 | **Normalisation of a slowly worsening symptom** | A machine's degradation is slow enough that each shift sees it as normal; "it always does that" | Long-term trend rising steadily while every individual reading looks unremarkable | Shift-length observation windows cannot see multi-month trends; long-horizon trending not routinely reviewed | Genuine degradation reclassified as a harmless machine quirk |
| P12 | **Statutory inspection deferral drift** | A periodic inspection is deferred once for a legitimate reason, then again, then indefinitely; breakdown work orders are closed against the asset and create a false impression of attention | Growing gap between required and actual inspection dates; deferrals logged without closed-out risk assessments | Breakdown maintenance closing out against the asset masks the compliance gap in casual review | Loss of the one scheduled event that proof-tests protective functions; compounding latent failures |

---

## 4. Detailed Lessons

### 4.1 Minimum-flow protection is a safety function, not a convenience

The most damaging BFW pump failure mode at this site has been operation below minimum continuous stable flow. For P-101B, minimum continuous flow is **72 m³/h**, which is 30% of the BEP flow of 240 m³/h. Below this figure the pump is not merely inefficient — it is in a fundamentally different and destructive hydraulic regime, characterised by suction and discharge recirculation, unsteady discharge pressure, broadband sub-synchronous vibration, elevated radial and axial loads, and churn heating of the trapped liquid.

The heating rate is inversely proportional to flow. At 25% of minimum flow the temperature rise is fast enough to take a seal chamber from normal to flashing in well under two hours. **This is not a slow degradation mechanism once it starts. Everything upstream of it is slow; the final stage is quick.**

The recirculation valve (MOV-118 for P-101B) is therefore performing a protective function. Yet it is routinely maintained as if it were an ordinary control valve. The failure characteristics of a rarely-actuated valve are specific and predictable: stem galling from long periods in one position, actuator gearbox lubricant hardening, torque switch tripping and latching. All of these are found by exercising the valve. None of them are found by leaving it alone.

**Lessons:**
- Classify every minimum-flow recirculation valve as a protective device with a documented proof-test schedule — full stroke annually with recorded stroke time and torque verification, partial-stroke exercise quarterly.
- **Configure a position-deviation alarm on every such valve.** "Command sent" is not "function achieved". If the valve is commanded open and position feedback does not reach 80% within 60 seconds, that must annunciate as a fault. A silent protection failure is worse than no protection, because it creates false confidence.
- Where the consequence justifies it, add a hard low-flow trip on the pump itself as a second layer, independent of the valve. Trip on sustained flow below minimum continuous flow, with a pre-trip alarm above it.
- Trend valve stroke time. A protective valve whose stroke time is creeping up is telling you it is about to seize.

### 4.2 Suction strainer fouling is the hidden origin of most low-flow events

Strainers protect the pump from debris and simultaneously threaten it by consuming NPSH. In a BFW system where all the NPSH comes from deaerator elevation, a strainer differential rising from a clean 0.2 bar to 0.6 bar can consume roughly half the total available head. At that point NPSH margin approaches zero, and the pump is on the edge of incipient cavitation whenever deaerator temperature rises.

The debris populations recur predictably across the industry: **mill scale** shed from original fabrication for years after commissioning, released in pulses at thermal transients; **weld slag** from piping modifications where post-weld cleaning was incomplete — the most damaging class because it is hard and angular; and **magnetite corrosion products from the deaerator**, individually fine enough to pass the perforations but agglomerating into a blinding mat on the basket surface. It is the mat, not the particles, that causes the differential.

Because it is a mat rather than a blockage, the fouling is a smooth ramp with no step change and no obvious "something broke" moment. This is precisely what makes it easy to normalise.

**The single most important structural lesson: a suction strainer with no bypass will not be cleaned on time.** Cleaning it requires taking the pump out of service and swapping to the parallel machine. Each individual decision to defer is locally rational. The cumulative outcome is not. The engineering fix is a duplex or bypassed strainer arrangement, which converts a consequential outage into a routine changeover.

**Lessons:**
- Fit duplex or bypassed strainers on all critical pump suctions. Retrofit where absent. This is a higher-value modification than most condition-monitoring investment.
- Set a hard maximum cleaning interval independent of differential pressure — 6 months for BFW service — and treat the ΔP trigger as the earlier of the two.
- Trend strainer ΔP **normalised against flow**, since raw differential varies with the square of flow and low-load operation masks early fouling.
- Set the cleaning trigger meaningfully below the alarm (e.g. 0.35 bar against a 0.5 bar alarm) so intervention can be planned rather than forced.
- Retain and analyse the debris. The debris population tells you where the contamination originates. Treating the strainer without treating the source guarantees repetition.
- Address the source: deaerator oxygen scavenging control, layup practice under nitrogen blanket, and chemical cleaning of residual mill scale at major outages.

### 4.3 Plan 23 seal flush loops degrade invisibly

An API 682 Plan 23 arrangement is the right technical choice for hot BFW service, but it has a specific and dangerous property: **it has almost no instrumentation, so it fails silently.** There is typically no flow measurement on the loop and often no temperature measurement across the cooler. The cooler fouls gradually on the water side, its ΔT falls from a design value of perhaps 40 K to under 20 K, and nothing anywhere indicates that the seal's cooling capability has halved.

The seal then absorbs process heat it was never designed to absorb. As seal chamber temperature climbs, the margin between local liquid temperature and saturation temperature at seal chamber pressure narrows. When the liquid flashes across the faces, the lubricating film is gone and the faces destroy themselves in minutes: heat-checked carbon, crazed silicon carbide, compression-set elastomers, fretted drive lugs.

**Lessons:**
- Put Plan 23 seal coolers on a scheduled cleaning interval — 6 monthly for hot BFW service — with a **mandatory ΔT verification on return to service**. A cleaning job that does not verify the restored duty has not been completed.
- **Instrument the loop.** At minimum, temperature indication on both sides of the cooler. This is a low-cost retrofit that converts an invisible failure into a trended one.
- Include a thermographic survey of the seal cooler and gland area on every PdM route. Infrared makes cooler fouling immediately visible without any permanent instrumentation.
- Treat "occasional weeping at the gland that clears once the machine is hot" as a leading indicator, not a nuisance. It is often the first externally visible sign that the seal chamber is running hotter than it should.
- Track the margin between seal chamber temperature and saturation temperature explicitly, not just the absolute temperature.

### 4.4 Hot standby and thermal soak

A standby BFW pump held full of hot water is not in a benign state. It soaks to line temperature with no flow to carry heat away, its seal faces sit hot and static, and its bearing housings warm without the benefit of circulating oil at operating flow. Standby machines routinely fall outside monitoring routines simply because they are not running — nobody trends a pump that is off.

**Lessons:**
- Fit and verify warming lines so a standby pump is kept at a controlled temperature by a small deliberate flow, rather than by uncontrolled soak.
- Include standby machines in thermography routes. Trend standby bearing housing temperature as a distinct point.
- Rotate duty between parallel pumps on a defined schedule so neither machine accumulates long static periods. This also exercises the associated valves, including the recirculation valve.
- Where a standby machine is expected to start on demand, prove it starts. An untested standby is an assumption, not a redundancy.

### 4.5 Restart sequencing on a shared suction header

Where two pumps share a suction header, the order in which they are started after a shutdown matters. Starting the wrong machine first can produce a transient pressure depression in the header that starves the second machine and causes vapour formation and cavitation. On this site's BFW system the correct sequence exists as strongly held operator knowledge, and it is correct — but it lives in shift handover notes rather than in a controlled operating procedure.

**Lessons:**
- Capture restart sequencing rules in a written, controlled operating procedure. Verbal shift knowledge is accurate right up until the shift that does not have the person who knows it.
- Where sequencing matters, interlock it rather than relying on procedure alone.
- Instrument and trend suction header pressure with sufficient resolution to catch start-up transients. A transient that lasts ten seconds will not appear on a one-minute historian.
- Include a suction-header transient check in the commissioning and post-outage restart checklist.

### 4.6 Instrument drift and the tribal-knowledge trap

Operators frequently know that a given instrument reads high or low, and they are frequently right — this knowledge typically comes from real comparisons against portable instruments. The problem is not that the knowledge is wrong. The problem is where it lives.

When an offset lives only in operators' heads, three failure modes follow. First, it is not transferred reliably to new staff. Second, it is applied as a general heuristic ("that reading always runs high, discount it") rather than as a specific correction, so genuine excursions get discounted too. Third, no one ever fixes it, because informally correcting for it is easier than raising the work order.

**Lessons:**
- Any known instrument offset must be either **corrected in the loop** or **documented in a controlled document** — ideally both. Verify against a portable reference and record the comparison.
- Audit critical loops against portable references on a defined schedule and record the result even when it is satisfactory.
- Harvest shift handover logs periodically for exactly this class of knowledge. Informal logs are the richest available source of real machine behaviour, and mining them is one of the cheapest reliability activities available.
- Treat "everyone knows that gauge reads high" as an open finding, not as an operational adaptation.

### 4.7 Setpoint document control

Where an operating manual and a vendor datasheet state different alarm and trip limits, the effective limit becomes whichever number supports the decision someone wants to make. This is not dishonesty; it is what ambiguity does. Every setpoint must have exactly one controlled source, and the DCS configuration must be verifiable against it.

**Lessons:**
- Maintain a single controlled setpoint register per asset. Reconcile manual, datasheet, and DCS configuration into it.
- Audit DCS alarm and trip configuration against the register annually.
- Where a conservative and a less conservative limit both exist, adopt the conservative one until an engineering assessment justifies otherwise, and record that assessment.

### 4.8 Alarm and data governance

Two closely related lessons that between them account for a large share of missed warnings:

A **standing alarm is not an alarm.** An alarm point that has been continuously active for weeks conveys no information and actively degrades the alarm system by cluttering the list and training operators to acknowledge without reading.

**Data collected but not reviewed has no value.** PdM routes at this site are executed reliably and on schedule. The review loop is the weak link. A Zone C vibration result sitting unread in the PdM system is indistinguishable, in outcome, from never having taken the measurement.

**Lessons:**
- No alarm may stand for more than 7 days without either a raised work order or a documented, time-limited suppression with a named owner and an expiry date.
- Escalate chronic alarms to require shift-supervisor acknowledgement with a mandatory recorded action.
- Any ISO 20816-3 **Zone C** result must be escalated to the responsible engineer within 48 hours with a written response. Zone D requires immediate escalation and a shutdown decision.
- Apply the ISO 20816 **change criterion** as well as the absolute zone criterion. A rise of 25% of the B/C boundary is significant even within Zone B, and it catches degradation far earlier.
- Resource data review as a distinct scheduled activity with a named owner, separate from data collection.

### 4.9 Statutory inspection intervals exist for a reason

Statutory periodic inspection under the OISD regime at a 12-month maximum interval is often perceived as a compliance formality. It is not. Its scope includes **functional verification of protective trips, alarms, and minimum-flow protection** — precisely the elements that fail silently and that nothing else in the maintenance system routinely exercises.

The deferral pattern is consistent and worth naming explicitly: an inspection is deferred once for a legitimate reason such as an unavailable outage slot; it is deferred again the following year by reference to the first deferral; and thereafter the deferral becomes the status quo. Crucially, **breakdown maintenance work orders closed against the asset create a false impression that the asset is receiving attention.** A pump can be stripped, rebuilt, and returned to service under a breakdown work order without a single statutory inspection requirement being satisfied — and without the compliance gap becoming visible to anyone reviewing the asset history casually.

**Lessons:**
- Track statutory inspection status as a distinct compliance metric, visible independently of general maintenance activity. It must not be possible for a breakdown work order to close a statutory record.
- Every deferral requires a signed, closed-out deferral risk assessment with a defined revised date. An open-ended deferral is not a deferral; it is an abandonment.
- Report overdue statutory inspections on critical equipment at management review, by asset, with elapsed time since the last compliant inspection.
- Where a pump has undergone a major rebuild, use that opportunity to reset the statutory clock properly with the full inspection scope, rather than wasting the open machine.

---

## 5. Consolidated Recommendations

| # | Recommendation | Addresses patterns | Priority |
|---|---|---|---|
| R1 | Classify all minimum-flow recirculation valves as protective devices; annual full-stroke proof test, quarterly partial-stroke exercise, recorded stroke times | P1 | Critical |
| R2 | Configure position-deviation alarms on all protective valves (command vs. achieved position, 60 s window) | P1 | Critical |
| R3 | Add independent low-flow protective trips on high-energy BFW pumps, with pre-trip alarm above minimum continuous flow | P1 | Critical |
| R4 | Complete and maintain the OISD 12-month statutory periodic inspection programme for all critical BFW pumps; prohibit breakdown work orders from closing statutory records | P12, P1 | Critical |
| R5 | Retrofit duplex or bypassed suction strainers on critical BFW pump suctions | P2 | High |
| R6 | Hard 6-month maximum strainer cleaning interval, independent of differential pressure | P2 | High |
| R7 | Trend strainer differential normalised against flow; set cleaning trigger below alarm | P2, P9 | High |
| R8 | Scheduled 6-month cleaning of Plan 23 seal coolers with mandatory ΔT verification on return to service | P3 | High |
| R9 | Instrument Plan 23 loops with cooler inlet/outlet temperature indication | P3 | High |
| R10 | Alarm governance: no standing alarm beyond 7 days without a work order or a time-limited documented suppression | P9 | High |
| R11 | Mandatory 48-hour escalation and written response for any ISO 20816-3 Zone C result; adopt the standard's change criterion alongside absolute zones | P10 | High |
| R12 | Single controlled setpoint register per asset; annual audit of DCS configuration against it | P7 | High |
| R13 | Calibrate and formally document all known instrument offsets; scheduled portable-reference verification of critical loops | P6 | High |
| R14 | Capture restart sequencing rules in controlled operating procedures; interlock where consequence justifies | P5 | Medium |
| R15 | Include standby machines in thermography and vibration routes; verify warming lines; rotate duty on a defined schedule | P4 | Medium |
| R16 | Trend pump efficiency and head at reference flow to detect wear ring clearance opening | P8 | Medium |
| R17 | Periodically harvest shift handover logs for undocumented machine behaviour and instrument offsets | P6, P11 | Medium |
| R18 | Add minimum-flow theory, churn heating, and asset-specific minimum flow figures to operator training | P1, P11 | Medium |
| R19 | Address debris at source: deaerator oxygen scavenging control, wet layup practice, chemical cleaning of residual mill scale at major outages | P2 | Medium |
| R20 | Review long-horizon (12+ month) trends at a scheduled monthly reliability meeting, since shift-length observation windows cannot detect slow degradation | P11 | Medium |

---

## 6. Closing Observation

Across every BFW pump event reviewed here, the pattern is the same shape. **The slow part of the failure lasted months and was visible the entire time. The fast part lasted under two hours and was unstoppable once it started.** Strainer differential rose over months. Valve stroke times degraded over months. Cooler duty declined over months. Vibration crossed into Zone C days in advance. Every one of those signals was measured, recorded, and available.

The failure was not one of instrumentation or of technical understanding. It was a failure of the loops that convert measurement into action: alarms permitted to stand indefinitely, reports filed unread, work orders never raised from log entries, correct knowledge held informally, and statutory inspections deferred until the deferral became invisible.

**Reliability improvement on these machines lies less in measuring more and more in acting on what is already measured.**

---

*Related documents: P-101B compiled inspection reports; S-14 maintenance and condition history; 2023 P-101B seal failure incident report; operator shift handover log.*
