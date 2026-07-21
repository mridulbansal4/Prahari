# Lock-Out / Tag-Out and Isolation Procedure — P-101B

**Document No.:** SAF-LOTO-P101B-002
**Revision:** 4
**Equipment:** P-101B — Boiler Feed Pump B (multistage centrifugal boiler feed water pump)
**Applies to:** All mechanical, electrical and instrument work requiring the pump to be de-energised and depressurised
**Related documents:** `MP-ROT-P101B-004` (seal and bearing maintenance), `compliance_OISD_P-101B.md`

---

## 1. Purpose and Scope

This procedure defines the isolation, lock-out, tag-out and energy-verification steps that must be completed before any person breaks containment on, opens, dismantles or works on **P-101B**, its driver, its seal support system or its associated piping including the suction strainer **S-14**.

No person shall commence work on P-101B until every step in Sections 5 and 6 is complete and signed. This procedure is mandatory. There is no "quick job" exemption.

Adjacent equipment — **P-101A**, **P-102** and exchanger **E-301** — remains live during this work. The isolation boundary is limited to P-101B and its immediate suction and discharge spool pieces up to and including the first isolation valves. Do not assume any adjacent line is dead.

---

## 2. Hazard Identification

| Hazard | Description | Potential consequence |
|---|---|---|
| Hot pressurised water flashing to steam | Boiler feed water is stored well above its atmospheric boiling point. On depressurisation it flashes violently. | Severe scald burns, blast injury, fatality |
| Stored pressure in casing and seal loop | The multistage casing and the API 682 Plan 23 closed seal loop retain pressure even after line isolation. | Gasket/bolt ejection, jet injury |
| Thermal burn from casing and bearing housings | Casing and bearing metal remains hot long after shutdown. | Contact burns |
| Unexpected electrical energisation | Auto-start logic may attempt to start P-101B on low header pressure or on P-101A trip. | Electrocution, rotating-part entrapment, amputation |
| Stored rotational energy | Rotor coast-down and coupling backlash. | Hand and finger injury |
| Gravity drain-back | Elevated discharge header can drain back through the pump when the discharge valve is opened. | Hot water release onto personnel |
| Instrument air / hydraulic actuator energy | MOV-118 actuator retains stored energy. | Unexpected valve movement |
| Chemical exposure | Feed water contains oxygen scavenger and amine dosing chemicals. | Skin and eye irritation |
| Manual handling | Bearing housings, coupling spacer, seal cartridge. | Musculoskeletal injury, crush |
| Slip hazard | Oil and condensate on the plinth. | Fall injury |

A job-specific risk assessment (JSA) shall be completed and signed by the work party before the permit is issued. The JSA is not a substitute for this procedure.

---

## 3. Energy Sources to Be Isolated

Every one of the following must be positively isolated. Isolating only the electrical supply is **not** an acceptable isolation for P-101B.

1. **Electrical** — motor supply from the MCC feeder. Racked out and locked. Includes the space heater circuit and the local start/stop station.
2. **Process — suction side** — hot feed water from the deaerator storage / suction header, via the suction line and strainer **S-14**.
3. **Process — discharge side** — back-flow from the pressurised boiler feed header, including back-flow through the non-return valve, which must never be treated as an isolation.
4. **Process — minimum-flow recirculation** — via **MOV-118** back to the deaerator.
5. **Stored pressure** — trapped liquid in the casing, in the balance line, in the seal chamber and in the Plan 23 loop and cooler.
6. **Thermal** — residual heat in casing metal, bearing housings and lagged pipework.
7. **Gravity** — head from the elevated discharge header and from the deaerator, both of which can drain back into an opened casing.
8. **Mechanical / stored rotational** — rotor inertia during coast-down; coupling wound-up torque.
9. **Auxiliary services** — seal cooling water supply and return, instrument air to MOV-118, and lube oil top-up connections.
10. **Instrumentation** — **TE-101B**, **VE-101B**, **PT-101**, **FT-101** and **PDI-S14** are to be inhibited so that spurious trips or auto-start logic cannot be triggered during the work.

---

## 4. Isolation Point List

| # | Isolation point | Tag / location | Type of isolation | Locked? | Verify by |
|---|---|---|---|---|---|
| 1 | Motor feeder | MCC-2 Panel, Feeder P-101B | Rack out breaker to isolated position, apply lock and danger tag | Yes | Attempted local start from field station; confirm dead with proving unit |
| 2 | Local start/stop station | Field station adjacent to plinth | Selector to OFF, lock and tag | Yes | Visual |
| 3 | Suction isolation valve | Upstream of strainer S-14 | Close, chain and lock | Yes | Valve position + downstream drain runs dry |
| 4 | Strainer drain valve | S-14 drain | Open to safe drain, tag open | Tag only | Free drainage observed |
| 5 | Discharge isolation valve | Downstream of NRV | Close, chain and lock | Yes | PT-101 reads zero after venting |
| 6 | Minimum-flow recirculation valve | MOV-118 | Close, de-energise actuator, isolate instrument air, bleed actuator, lock | Yes | Valve position indicator + air gauge at zero |
| 7 | Balance line isolation | Balance/leak-off line valve | Close and lock | Yes | Vent runs dry |
| 8 | Casing vent | Casing high-point vent | Open, tag open | Tag only | Steady atmospheric discharge, then nil |
| 9 | Casing drain | Casing low-point drain to closed drain | Open, tag open | Tag only | Free drainage, then nil |
| 10 | Seal support system | Plan 23 loop isolation and cooler drain | Close inlet/outlet, drain loop | Yes | Loop drained to collection drum |
| 11 | Seal cooling water | Cooling water supply and return | Close and lock both | Yes | Cooler vent runs dry |
| 12 | Instrument air header to actuator | Local air isolation | Close, bleed, lock | Yes | Gauge reads zero |

Where the job requires positive isolation for entry into the process envelope for an extended period, a **spade/spectacle blind** shall be inserted at the suction and discharge flanges. Valve closure alone, however tightly chained, is a temporary isolation and is not acceptable for extended breaking of containment. The decision to blind rests with the Area Authority and must be recorded on the permit.

---

## 5. Personal Protective Equipment

Minimum PPE for all work under this procedure:

- Flame-retardant coverall
- Safety helmet with chinstrap
- Safety shoes with steel toecap and penetration-resistant sole
- Safety spectacles with side shields at all times; **full face shield plus chemical goggles** whenever a valve, vent, drain or flange is cracked open
- Heat-resistant gloves for any contact with hot surfaces; chemical-resistant gloves for dosed water contact
- Hearing protection in the pump house (measured levels exceed the 85 dB(A) action level)

Additional PPE by task:

- Draining and venting hot water: apron and gauntlets rated for hot liquid splash; stand to the side of any opening, never in front of it
- Electrical isolation at the MCC: arc-rated PPE appropriate to the incident energy marked on the panel label; use only insulated and rated tools
- Grinding or lapping: full face shield over safety spectacles

Gas detection: a calibrated multi-gas detector shall be carried by the work party whenever a drain is opened into a pit or a low-lying area.

---

## 6. Step-by-Step LOTO Sequence

1. **Obtain permission.** The Shift-in-Charge confirms that P-101A can carry full feed water duty and that its minimum-flow protection is functional. Record the confirmation on the permit.
2. **Stop the pump.** Stop P-101B from the control room. Confirm on the DCS that motor current has fallen to zero and that **FT-101** flow and **PT-101** discharge pressure have decayed.
3. **Defeat auto-start.** Place P-101B in the manual/out-of-service mode in the DCS and inhibit the auto-start-on-standby logic. Log the inhibit in the operator's inhibit register with the permit number. This is a frequently missed step and is the single most common cause of unexpected energisation on spared pumps.
4. **Allow coast-down.** Confirm the shaft is stationary by direct observation through the coupling guard before proceeding. Do not touch the coupling to stop it.
5. **Electrical isolation.** The authorised electrician racks out the MCC feeder, applies the electrical section lock and a danger tag bearing the permit number, the date and the name of the person applying it. The local start/stop station is switched off, locked and tagged.
6. **Prove dead.** Attempt to start P-101B from the field station and from the DCS. Both attempts must fail. The electrician then proves the motor terminals dead using a proving-unit-tested voltage detector (test the detector, test the circuit, re-test the detector).
7. **Process isolation.** Close and chain-lock the suction and discharge isolation valves and the balance line valve. Close, de-energise, bleed and lock MOV-118.
8. **Depressurise.** Slowly crack the casing high-point vent, standing clear of the discharge path. Allow full flashing and venting to atmosphere to complete. Only when venting has stopped, open the casing low-point drain to the closed drain system.
9. **Verify zero pressure.** Confirm **PT-101** reads zero and that **PDI-S14** across the strainer reads zero. Confirm by direct observation that the vent and drain are both open and passing nothing. A gauge reading alone is not sufficient verification — the gauge may be isolated or failed.
10. **Cool down.** Verify by contact thermometer that casing and bearing housing surface temperatures are below 45 °C before hands-on work. Do not force-cool a hot casing with water; thermal shock will distort it.
11. **Isolate auxiliaries.** Isolate and drain the Plan 23 seal loop and its cooler. Isolate seal cooling water supply and return. Isolate and bleed instrument air.
12. **Inhibit instruments.** Inhibit **TE-101B**, **VE-101B**, **PT-101**, **FT-101** and **PDI-S14** in the DCS and log each inhibit.
13. **Apply personal locks.** Every member of the work party applies their own personal lock to the group lock box, along with a tag showing their name, department, contact number and date. The lock box key is retained by the Area Authority. **One lock per person. Locks are never shared, never lent, and never removed by anyone other than the person who applied them.**
14. **Final zero-energy verification.** The Area Authority walks the full isolation point list with the lead technician, physically confirming each item, and both sign the verification block on the permit.
15. **Display the permit** at the job site for the duration of the work.

---

## 7. Permit-to-Work Requirements

- A **cold work permit** is required for all mechanical dismantling under this procedure. It is valid for one shift and must be revalidated at each shift handover by the incoming Area Authority.
- A **hot work permit** is additionally required for any welding, flame cutting, grinding or use of non-flameproof electrical equipment in the pump house. Hot work requires a gas test immediately before commencement and at intervals stated on the permit, a dedicated fire watch, and fire-fighting equipment at the location. The fire watch shall remain for a minimum of 30 minutes after hot work stops.
- A **confined space entry permit** is required if any person is to enter the pump pit, the drain sump or any excavation around the plinth. Entry requires continuous atmospheric monitoring for oxygen, flammables and toxics, forced ventilation, a trained standby attendant stationed at the entry point, rescue equipment rigged and ready, and a documented rescue plan. Never enter a pit to retrieve a dropped tool without a permit.
- Permits are cancelled at the end of each shift or on completion of the work, whichever is earlier. Work must not continue on an expired permit.
- **Shift handover:** the outgoing and incoming Area Authorities jointly re-walk the isolation list. Personal locks belonging to departing personnel are removed by those personnel before they leave site; incoming personnel apply their own.

---

## 8. Restoration Sequence

Restoration is the reverse of isolation and is at least as hazardous. It shall not be rushed at the end of a shift.

1. Confirm the job is complete, all tools and materials are accounted for, and no foreign objects remain inside the casing, seal chamber or bearing housings. Perform and record a formal tool tally.
2. Confirm all covers, guards — especially the coupling guard — and lagging have been refitted.
3. Confirm strainer **S-14** has been cleaned and correctly reinstalled with a new gasket and with the element the right way round.
4. Each member of the work party removes their own personal lock and tag. The lead technician's lock is removed last.
5. Close the casing vent and drain. Close the strainer drain.
6. Restore seal cooling water and refill and vent the Plan 23 loop before any attempt to start.
7. Restore instrument air to the MOV-118 actuator and stroke the valve to prove it operates.
8. Open the suction isolation valve slowly and allow the casing to fill and vent completely. Watch for leaks at every joint that was broken.
9. Open the discharge isolation valve slowly.
10. Restore the electrical isolation: the electrician removes the electrical lock and tag and racks in the MCC feeder.
11. Remove DCS inhibits on TE-101B, VE-101B, PT-101, FT-101 and PDI-S14. Confirm each reads live and plausible. Clear each entry from the inhibit register.
12. Confirm the **TE-101B high-temperature alarm is configured at 85 °C** as required by the P-101B operating manual before the pump is started.
13. Restore the auto-start logic and return P-101B to standby or duty as instructed by the Shift-in-Charge.
14. Close the permit. File the permit, the JSA, the isolation list and the lock log with the work order.

---

## 9. Statutory and Regulatory References

The following are paraphrased summaries of the obligations that apply to this work. Consult the current text of each instrument for the authoritative wording; the summaries below are for site guidance only.

- **Factories Act, 1948 (India), Chapter IV — Safety.** The occupier and manager carry a duty to ensure that machinery is securely fenced and that no person is permitted to examine, lubricate or adjust machinery in motion except in the limited circumstances the Act allows, and then only by a trained adult male worker wearing tight-fitting clothing. Section 21 addresses the fencing of machinery. Section 22 restricts work on machinery in motion. Section 28 addresses hoists and lifts, relevant where lifting equipment is used to handle pump components. Section 31 addresses plant and machinery under pressure, requiring that safe operating pressures are not exceeded and that effective measures are taken to ensure this. Sections 40A and 40B address the maintenance of buildings and the appointment of safety officers. The Act also imposes obligations regarding excessive noise and the provision of protective equipment where hazards cannot otherwise be eliminated. Under the Act and the associated State Factories Rules, records of examination and testing of specified plant must be maintained and produced to the Inspector of Factories on demand.

- **Petroleum and Explosives Safety Organisation (PESO).** PESO administers licensing and periodic inspection under the Explosives Act, 1884, the Petroleum Act, 1934 and the associated Rules (including the Static and Mobile Pressure Vessels (Unfired) Rules and the Gas Cylinders Rules). Pressure vessels and associated equipment within the licensed premises are subject to periodic external and internal examination and hydrostatic testing at the intervals stated in the applicable Rules, carried out by a competent person, with certificates retained and available for inspection. Any modification to licensed equipment or to the approved layout requires prior PESO approval. Work on or near equipment covered by a PESO licence must not compromise the conditions of that licence.

- **OISD standards (Oil Industry Safety Directorate).** OISD-STD-105 addresses work permit systems, including the classification of cold and hot work, the responsibilities of the issuing and receiving authorities, gas testing, and the validity and renewal of permits. OISD-STD-137 addresses inspection of pressure-relieving devices. OISD-STD-128 addresses inspection of unfired pressure vessels. OISD-GDN-134 addresses inspection of rotating equipment, covering periodic condition monitoring, inspection intervals and record-keeping for pumps of this class. Compliance status for P-101B against these standards is tracked in `compliance_OISD_P-101B.md`. **Note that the OISD periodic inspection of P-101B is currently overdue; see that register before planning further work.**

- **Electrical safety.** Isolation, locking and proving dead at the MCC shall be performed only by a person authorised under the site electrical safety rules and holding a valid competency certificate under the applicable State Electricity Rules.

---

## 10. Accountability

Failure to follow this procedure is a serious safety violation and will be treated as such regardless of whether an incident results. Any person may stop this job at any time without needing to justify the decision in advance.

If any step in this procedure cannot be completed as written — a valve that will not seat, a lock that will not fit, a gauge that cannot be verified — **stop and escalate to the Area Authority.** Do not improvise an alternative isolation.

| Role | Responsibility |
|---|---|
| Shift-in-Charge | Authorises taking P-101B out of service; confirms P-101A availability |
| Area Authority | Issues permit; verifies isolation; holds the lock box key; authorises restoration |
| Authorised Electrician | Electrical isolation, locking, proving dead, and restoration |
| Lead Technician | Applies first and removes last personal lock; performs tool tally |
| Work Party Members | Apply and remove their own personal locks; comply with the JSA |
| Safety Officer | Audits permit and LOTO compliance; may stop the job |
