# Maintenance Procedure — Mechanical Seal and Bearing Service, P-101B

**Document No.:** MP-ROT-P101B-004
**Revision:** 6
**Equipment:** P-101B — Boiler Feed Pump B (multistage centrifugal boiler feed water pump)
**Discipline:** Rotating Equipment / Mechanical Maintenance
**Classification:** Critical service — spared equipment, but reduced-redundancy operation during execution

---

## 1. Scope

This procedure covers the removal, inspection, refurbishment and reinstallation of the drive-end mechanical seal and both radial/thrust bearing assemblies on **P-101B**, a horizontal multistage centrifugal boiler feed water pump built to API 610 (BB-type between-bearings arrangement). It applies to planned shutdown maintenance and to corrective intervention following a seal-leakage or bearing high-temperature event.

This procedure does **not** cover: rotor rebalancing, casing hydrotest, diffuser/bowl replacement, motor rewind, or coupling replacement. Those are covered by separate work instructions and require the reliability engineer's authorisation.

While P-101B is out of service, feed water duty transfers to **P-101A**. Confirm with the shift-in-charge that P-101A is available and that its minimum-flow protection is functional before starting. **P-102** and exchanger **E-301** are not affected by this work.

---

## 2. Prerequisites

1. Work order raised and approved; job planned in the CMMS against P-101B.
2. **Lock-out/tag-out completed in full per `safety_LOTO_P-101B.md`.** No mechanical work may commence until the electrical isolation of the MCC feeder, process isolation at suction and discharge, depressurisation, drain-down and verification of zero energy are all signed off. The bearing housings and casing must be verified below 45 °C by contact thermometer before hands-on work.
3. Cold work permit issued and displayed at the job site. Any grinding, lapping with powered tools, or welding requires a separate hot work permit.
4. Suction strainer **S-14** on the P-101B suction line is isolated and its differential pressure indicator **PDI-S14** is reading zero, confirming the line is depressurised.
5. Field instruments **TE-101B** (bearing temperature), **VE-101B** (vibration), **PT-101** (discharge pressure) and **FT-101** (flow) are inhibited in the DCS and the inhibits logged in the operator's inhibit register.
6. Minimum-flow recirculation valve **MOV-118** is de-energised and secured in the closed position with its own lock.
7. Baseline data retrieved: last vibration route data from VE-101B, last thermography, last recorded seal-pot level and Plan 23 cooler outlet temperature.

---

## 3. Tools, Consumables and Spares

| Item | Specification / Notes |
|---|---|
| Calibrated torque wrench | 10–80 N·m range, calibration valid within 6 months, certificate at site |
| Dial indicators with magnetic bases | 0.001 mm resolution, two off |
| Inside/outside micrometers | 0–100 mm, calibrated |
| Feeler gauge set | 0.02–1.00 mm |
| Optical flat and monochromatic light source | For seal face flatness check |
| Induction bearing heater | Bearings to be heated to max 110 °C, never flame-heated |
| Hydraulic bearing puller set | Sized for the shaft journal diameters |
| Seal setting clips | OEM part, matched to the cartridge seal |
| Mechanical seal cartridge | API 682 Category 2, Type A, Arrangement 1, per equipment BOM |
| Bearing set | Radial: cylindrical roller; thrust: angular contact duplex pair, per BOM |
| Gaskets and O-rings | Fluoroelastomer/PTFE per BOM; single use only |
| Lint-free wipes, isopropyl alcohol | Seal face cleaning only |
| Lubricating oil | ISO VG 46 turbine oil, new stock, filtered to NAS 6 |

All spares are to be drawn against the work order and identity-verified against the OEM part numbers before the seal cavity is opened.

---

## 4. Removal Sequence

1. Disconnect and tag the API 682 Plan 23 seal flush piping at the seal chamber and at the cooler. Cap all open ends immediately. Drain the seal cooler loop to the closed collection drum.
2. Remove the coupling guard. Record the existing shaft alignment readings (rim/face or reverse-dial) before decoupling — these are needed as the reference for the post-job alignment.
3. Remove the coupling spacer. Do not strike the coupling hub.
4. Remove bearing housing end covers. Drain the oil to the used-oil drum and retain a 200 ml sample in a clean labelled bottle for laboratory analysis (viscosity, water content, ferrography, particle count).
5. Remove the oil rings/flingers, then the bearing housing halves. Record the existing bearing housing-to-shaft float and the axial rotor position with a dial indicator before disturbing the thrust assembly.
6. Extract the bearings using the hydraulic puller. Do not apply extraction force through the rolling elements. Tag each bearing with its position (DE radial, NDE radial, thrust) and bag it separately for failure analysis.
7. Withdraw the cartridge seal as a complete unit. Do **not** dismantle the cartridge in the field unless the OEM has authorised field repair; return it to the seal workshop with the setting clips fitted.
8. Cover the seal chamber and bearing housings with clean polythene and tape as soon as components are out.

---

## 5. Inspection and Acceptance Criteria

| Check | Method | Accept | Reject / Action |
|---|---|---|---|
| Shaft journal diameter | Micrometer, 3 axial × 2 radial positions | Within OEM drawing tolerance, typically h5/h6 | Undersize > 0.013 mm — refer to reliability engineer for metal spray/regrind |
| Shaft runout (TIR) at seal region | Dial indicator, shaft on vee-blocks or in bearings | ≤ 0.05 mm TIR | > 0.05 mm — straighten or replace shaft |
| Shaft runout at coupling hub fit | Dial indicator | ≤ 0.025 mm TIR | Reject shaft |
| Radial bearing diametral clearance | Micrometer / feeler on new bearing | C3 internal clearance class, 0.045–0.073 mm typical for the fitted bore size | Outside band — reject bearing |
| Thrust bearing axial float in housing | Dial indicator, rotor pushed both ways | 0.05–0.10 mm total | Outside band — adjust shim pack |
| Bearing housing bore | Inside micrometer, 3 positions | Round within 0.020 mm, no scoring | Re-machine and sleeve |
| Seal face flatness (both faces) | Optical flat, monochromatic light | ≤ 3 helium light bands (≈ 0.9 µm) | Re-lap or replace face |
| Seal face surface finish | Comparator / profilometer | Ra ≤ 0.2 µm | Re-lap |
| Seal chamber face perpendicularity | Dial indicator sweep | ≤ 0.05 mm TIR relative to shaft axis | Re-machine |
| Sleeve O-ring grooves | Visual + 10× loupe | No nicks, no fretting steps | Replace sleeve |
| Plan 23 cooler tubes | Visual, pressure test at 1.5 × MAWP | No leakage, no scale bridging | Chemically clean or retube |

Record every measurement on the job data sheet. Blank fields are not acceptable; write "N/A" with a reason if a check is genuinely not applicable.

---

## 6. Reassembly

1. Clean all mating faces with lint-free wipes and isopropyl alcohol. Confirm no wipe fibres remain on the seal faces.
2. Heat bearings on the induction heater to a maximum of **110 °C** and slide onto the shaft against the shoulder. Never heat with an open flame. Allow to cool and shrink before releasing.
3. Fit the thrust duplex pair in the correct back-to-back orientation as marked by the manufacturer. Confirm the axial float against the acceptance band in Section 5.
4. Install new gaskets and O-rings. Lightly lubricate elastomers with a compatible fluid — never use grease on Plan 23 wetted elastomers.
5. Slide the cartridge seal into the chamber with the setting clips still fitted. Ensure the gland is square to the shaft; check with a feeler gauge at four points, maximum variation 0.05 mm.
6. **Seal gland bolt tightening — the seal bolts shall be tightened to 55 N·m using a calibrated torque wrench, in a numbered star (cross) pattern.** For an eight-bolt gland, number the bolts 1 through 8 clockwise and tighten in the sequence **1 – 5 – 3 – 7 – 2 – 6 – 4 – 8**. Apply the torque in three passes: 30 % of final (≈ 16 N·m), then 70 % (≈ 38 N·m), then **100 % at 55 N·m**. After the final pass, make one further confirmation round at 55 N·m in the same star sequence to catch any bolt that has relaxed. Do not exceed 55 N·m; over-torque distorts the gland and causes face flatness loss that will not be visible until the seal leaks in service.
7. Remove the seal setting clips **only after** the gland bolts are fully torqued and the coupling is ready to be fitted. Retain the clips with the job pack — a seal commissioned with clips still fitted will shear the drive lugs on start-up.
8. Reconnect the Plan 23 flush piping. Confirm the flush loop is continuously rising from the seal chamber to the cooler and back with no vapour-trapping high points, and that the loop is vented at its highest point.
9. Refill bearing housings with ISO VG 46 oil to the sight-glass centreline. Do not overfill; overfilled housings churn and run hot.
10. Refit the coupling spacer and re-align the pump to the driver. Cold alignment target: offset ≤ 0.05 mm and angularity ≤ 0.05 mm per 100 mm, adjusted for the calculated thermal growth of the feed water service. Record final readings.
11. Refit the coupling guard. Torque hold-down bolts and check soft foot ≤ 0.05 mm at each foot before final tightening.

---

## 7. Seal Flush (API 682 Plan 23) Recommissioning

The seal on P-101B is supported by an **API 682 Plan 23** arrangement — a closed-loop recirculation from the seal chamber, driven by the internal pumping ring, through a water-cooled seal cooler and back to the seal chamber. Because the loop is closed, correct venting is essential; a trapped vapour pocket will dry-run the faces.

1. Fill the loop slowly from the highest vent, keeping the vent open until a solid liquid stream is observed.
2. Confirm cooling water is flowing to the seal cooler shell side and that the cooling water outlet valve is fully open before the pump is started.
3. Confirm the seal chamber pressure is above the product vapour pressure at the operating temperature with an adequate margin — the API 682 guidance for pressure margin over vapour pressure applies. For this hot feed water service, verify the margin against the seal datasheet before start-up.
4. Verify the pumping ring direction of rotation matches the shaft rotation direction stamped on the casing.
5. During the first hour of running, monitor the cooler outlet temperature. A rising loop temperature with steady cooling water flow indicates a blocked or vapour-locked loop; shut down and investigate.

---

## 8. Post-Job Checks and Recommissioning

1. Restore isolations in the sequence given in `safety_LOTO_P-101B.md`. Remove all locks and tags in reverse order of application; the lead technician's lock is removed last.
2. Confirm strainer **S-14** has been cleaned and reinstalled, and that **PDI-S14** is back in service. Record the clean differential pressure as the new baseline.
3. Remove DCS inhibits on **TE-101B**, **VE-101B**, **PT-101** and **FT-101**. Confirm each reads a plausible live value.
4. Confirm **MOV-118** minimum-flow recirculation valve strokes fully open and fully closed on demand, and that it is open before the pump is started.
5. Bump-start the pump for 3–5 seconds and confirm the direction of rotation.
6. Start the pump against a closed discharge with MOV-118 open. Bring the pump onto the system slowly and confirm **PT-101** discharge pressure and **FT-101** flow are consistent with the pump curve at the operating speed.
7. **Vibration acceptance per ISO 20816:** take readings at all accessible bearing housings in the horizontal, vertical and axial directions once thermal and hydraulic conditions have stabilised. Compare against the ISO 20816 evaluation zones for this machine class and support type. Zone A (newly commissioned) is the target; Zone B is acceptable for continued unrestricted operation; a reading in Zone C requires an agreed action plan and increased monitoring; Zone D requires immediate shutdown. Cross-check the field readings against the online **VE-101B** trend and confirm the two agree within 10 %.
8. **Bearing temperature verification on TE-101B:** monitor continuously for the first four hours. Temperature should rise, plateau and remain stable. **The high-temperature alarm setpoint on TE-101B is 85 °C per the P-101B operating manual.** Any approach to that setpoint, or a temperature that continues to climb without plateauing, is grounds for shutdown and investigation before the machine is handed back. Confirm the alarm setpoint is actually configured at 85 °C in the DCS before handover — do not assume.
9. Confirm the seal chamber is dry externally after two hours of running. Any visible weepage requires re-inspection, not re-torquing beyond 55 N·m.
10. Take a 24-hour and a 7-day follow-up vibration and temperature reading. Attach both to the work order before closing it.
11. Update the equipment history record in the CMMS with the failed-component analysis, all measured clearances, and the oil sample laboratory result when it returns.

---

## 9. Records to Attach

- Completed job data sheet with all Section 5 measurements
- Torque wrench calibration certificate (valid at the date of use)
- Alignment record, before and after
- Vibration report per ISO 20816, baseline and 7-day
- Oil sample laboratory report
- Failed-component photographs (bearings and seal faces, both sides)
- Permit copies and the LOTO log page

---

## 10. Sign-Off

| Stage | Name | Designation | Signature | Date / Time |
|---|---|---|---|---|
| LOTO applied and zero-energy verified | | Shift Operator | | |
| Permit issued | | Area Authority | | |
| Removal complete, components tagged | | Mechanical Technician | | |
| Inspection measurements witnessed | | Mechanical Supervisor | | |
| Seal gland torqued to 55 N·m, star pattern verified | | Mechanical Technician | | |
| Torque witnessed | | Mechanical Supervisor | | |
| Plan 23 loop filled, vented and proven | | Mechanical Technician | | |
| Alignment accepted | | Rotating Equipment Engineer | | |
| Isolations restored, instruments un-inhibited | | Shift Operator | | |
| Vibration accepted per ISO 20816 | | Reliability Engineer | | |
| TE-101B stable, alarm confirmed at 85 °C | | Shift Operator | | |
| Equipment accepted back into service | | Shift-in-Charge | | |
| Work order closed, records attached | | Maintenance Planner | | |

---

*Prepared by: Rotating Equipment Section. Reviewed by: Maintenance Manager. Approved by: Plant Manager. Any deviation from this procedure requires written concession from the Rotating Equipment Engineer before the deviation is executed, not afterwards.*
