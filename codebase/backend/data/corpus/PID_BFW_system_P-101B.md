# P&ID (Textual) — Boiler Feed Water System, Train B
## Document No. PID-BFW-002 Rev. 4
**Unit:** 100 — Boiler Feed Water / Deaeration
**Area:** Utilities Block, Elev. +0.00 m (pump bay), +12.50 m (deaerator platform)
**Design Code Basis:** API 610 12th Ed. (BB4 multistage), API 682 4th Ed. (seals), ASME B31.1 (power piping)
**Prepared by:** Process Engineering / Rotating Equipment
**Status:** ISSUED FOR OPERATION

---

## 1. Scope and Purpose

This document is the textual (machine-readable) representation of the boiler feed water (BFW) system serving Boilers B-01 and B-02. It covers the deaerator storage section, the common suction header, the duty/standby feed pump pair `P-101A` and `P-101B`, the suction strainer `S-14`, the discharge header, and the minimum-flow recirculation loop returning to the deaerator via `MOV-118`.

The system is arranged 2 × 100% — one pump running, one on auto-standby. `P-101B` is the subject asset of this revision; `P-101A` is shown only as far as necessary to establish the parallel topology and shared-header interactions. Downstream users `P-102` (condensate transfer) and exchanger `E-301` (BFW preheat) appear at battery-limit references only and are detailed on PID-CND-011 and PID-HX-004 respectively.

---

## 2. ASCII Schematic

```
                       VENT TO ATMOS
                            ^
                            |
        LP STEAM  ------>  +---------------------------+
        (PCV-140)          |     DEAERATOR  DA-100     |   Elev +12.50 m
        COND RETURN ---->  |   (storage section 28 m3) |
                           +-------------+-------------+
                                         |
                              LI-100 / LT-100  (level)
                                         |
                          12"-BFW-1001-A1A  (suction downcomer)
                                         |
                                         v
     +===================== COMMON SUCTION HEADER ======================+
     |                     12"-BFW-1002-A1A                             |
     +===+==========================================================+===+
         |                                                          |
   [HV-114 gate]                                              [HV-115 gate]
         |                                                          |
         |                                                    +-----------+
         |                                                    |  STRAINER |
    +---------+                                               |   S-14    |  <-- PDI-S14
    |STRAINER |                                               | (T-type,  |      (clean 0.2 bar
    |  S-13   |                                               |  40 mesh) |       alarm 0.5 bar)
    +---------+                                               +-----------+
         |                                                          |
         |  8"-BFW-1003-A1A                                         |  8"-BFW-1004-A1A
         v                                                          v
    +---------+                                               +-----------+
    | P-101A  |  (parallel / standby)                         |  P-101B   |
    | BB4 6-stg|                                              | BB4 6-stg |
    +---------+                                               +-----------+
         |                                                    |  TE-101B (brg temp)
         |                                                    |  VE-101B (vibration)
    [NRV-116]                                               [NRV-117]
         |                                                    |
         |  6"-BFW-1005-B2C                                   |  6"-BFW-1006-B2C
         |                                                    |
         |                                            PT-101 --+-- FT-101
         |                                                    |
     +===+========== COMMON DISCHARGE HEADER ================+=+
     |               6"-BFW-1010-B2C   (to boilers B-01/B-02)  |
     +===+=====================================================+
         |                                   |
         |                                   +---> 6"-BFW-1012-B2C --> E-301 (BFW preheat, ref PID-HX-004)
         |
         |  3"-BFW-1020-B2C   MINIMUM-FLOW RECIRCULATION
         |
      [MOV-118]  <-- controlled from FT-101 (FIC-101) low-flow logic
         |
      [RO-119]  restriction orifice, 14.7 mm bore, breakdown 78 bar -> 6 bar
         |
         v
    back to DEAERATOR DA-100 storage section (sparger nozzle N-7)


    V-201  KNOCKOUT DRUM  (LP steam supply KO to PCV-140)
      steam header --> V-201 --> demister --> PCV-140 --> DA-100 sparge
      V-201 condensate LCV-201 --> condensate return header --> DA-100
      NOTE: V-201 carryover degrades deaerator pegging steam quality and
            can depress DA-100 pressure, reducing NPSHa at S-14 / P-101B.
```

---

## 3. Line Schedule

| Line No. | Size | Spec | Service | From | To | Design P/T |
|---|---|---|---|---|---|---|
| 12"-BFW-1001-A1A | 12 in | A1A (CS, 150#) | DA storage downcomer | DA-100 | Suction header | 10 barg / 180 °C |
| 12"-BFW-1002-A1A | 12 in | A1A | Common suction header | 1001 | HV-114 / HV-115 | 10 barg / 180 °C |
| 8"-BFW-1003-A1A | 8 in | A1A | P-101A suction | HV-114 / S-13 | P-101A | 10 barg / 180 °C |
| 8"-BFW-1004-A1A | 8 in | A1A | P-101B suction | HV-115 / S-14 | P-101B | 10 barg / 180 °C |
| 6"-BFW-1005-B2C | 6 in | B2C (CS, 900#) | P-101A discharge | P-101A | Disch header | 140 barg / 200 °C |
| 6"-BFW-1006-B2C | 6 in | B2C | P-101B discharge | P-101B | Disch header | 140 barg / 200 °C |
| 6"-BFW-1010-B2C | 6 in | B2C | Common discharge header | 1005/1006 | Boiler econ. inlets | 140 barg / 200 °C |
| 6"-BFW-1012-B2C | 6 in | B2C | BFW to preheat | Disch header | E-301 | 140 barg / 200 °C |
| 3"-BFW-1020-B2C | 3 in | B2C | Min-flow recirculation | Disch header | MOV-118 / RO-119 | 140 barg / 200 °C |
| 3"-BFW-1021-A1A | 3 in | A1A | Recirc return | RO-119 | DA-100 nozzle N-7 | 10 barg / 180 °C |
| 2"-SC-1305-A1A | 2 in | A1A | V-201 condensate | V-201 | Cond. return header | 16 barg / 210 °C |

Suction piping to `P-101B` is arranged with a minimum of five pipe diameters of straight run immediately upstream of the pump suction nozzle, in line with API 610 clause 6.4 intent for suction piping arrangement. No elbow is permitted directly on the nozzle. The suction line falls continuously from the deaerator with no high-point pockets; the static leg from DA-100 liquid level to the `P-101B` centreline is 11.20 m, which is the dominant term in NPSHa.

---

## 4. Component List (machine-readable)

```
ID: DA-100      | TYPE: Deaerator            | SERVICE: BFW deaeration/storage | DUTY: 28 m3 storage, 0.35 barg
ID: V-201       | TYPE: Knockout Drum        | SERVICE: LP steam KO to DA-100  | DUTY: 1.2 m3, demister pad
ID: S-13        | TYPE: Suction Strainer     | SERVICE: P-101A suction         | DUTY: T-type, 40 mesh, SS316
ID: S-14        | TYPE: Suction Strainer     | SERVICE: P-101B suction         | DUTY: T-type, 40 mesh, SS316
ID: P-101A      | TYPE: Centrifugal Pump     | SERVICE: Boiler Feed Pump A     | DUTY: multistage, parallel/standby
ID: P-101B      | TYPE: Centrifugal Pump     | SERVICE: Boiler Feed Pump B     | DUTY: 6-stage BB4, 240 m3/h rated
ID: P-102       | TYPE: Centrifugal Pump     | SERVICE: Condensate transfer    | DUTY: ref PID-CND-011
ID: E-301       | TYPE: Shell & Tube Exch.   | SERVICE: BFW preheat            | DUTY: ref PID-HX-004
ID: MOV-118     | TYPE: Motor Operated Valve | SERVICE: Min-flow recirculation | DUTY: 3in globe, fail-open
ID: RO-119      | TYPE: Restriction Orifice  | SERVICE: Recirc breakdown       | DUTY: 14.7 mm bore
ID: NRV-116     | TYPE: Check Valve          | SERVICE: P-101A discharge       | DUTY: 6in swing, spring assist
ID: NRV-117     | TYPE: Check Valve          | SERVICE: P-101B discharge       | DUTY: 6in swing, spring assist
ID: HV-114      | TYPE: Gate Valve           | SERVICE: P-101A suction isol.   | DUTY: 8in, CS, LO
ID: HV-115      | TYPE: Gate Valve           | SERVICE: P-101B suction isol.   | DUTY: 8in, CS, LO
ID: HV-120      | TYPE: Gate Valve           | SERVICE: P-101B discharge isol. | DUTY: 6in, 900#
ID: PCV-140     | TYPE: Control Valve        | SERVICE: DA-100 pegging steam   | DUTY: from V-201
ID: LCV-201     | TYPE: Control Valve        | SERVICE: V-201 condensate level | DUTY: 2in
ID: TE-101B     | TYPE: Temperature Element  | SERVICE: P-101B bearing temp    | DUTY: RTD Pt100, DE+NDE
ID: VE-101B     | TYPE: Vibration Element    | SERVICE: P-101B vibration       | DUTY: accelerometer, mm/s RMS
ID: PT-101      | TYPE: Pressure Transmitter | SERVICE: BFW discharge pressure | DUTY: 0-160 barg
ID: FT-101      | TYPE: Flow Transmitter     | SERVICE: BFW discharge flow     | DUTY: orifice, 0-350 m3/h
ID: PDI-S14     | TYPE: Diff. Press. Indic.  | SERVICE: S-14 strainer dP       | DUTY: 0-2.5 bar
ID: LT-100      | TYPE: Level Transmitter    | SERVICE: DA-100 storage level   | DUTY: DP type
```

---

## 5. Connection / Topology List (machine-readable)

```
DA-100  -> UPSTREAM_OF -> SUCTION_HEADER
SUCTION_HEADER -> UPSTREAM_OF -> HV-114
SUCTION_HEADER -> UPSTREAM_OF -> HV-115
HV-115  -> UPSTREAM_OF -> S-14
S-14    -> UPSTREAM_OF -> P-101B
S-13    -> UPSTREAM_OF -> P-101A
P-101B  -> UPSTREAM_OF -> NRV-117
NRV-117 -> UPSTREAM_OF -> DISCHARGE_HEADER
P-101A  -> PARALLEL_WITH -> P-101B
P-101A  -> SHARES_SUCTION_HEADER_WITH -> P-101B
DISCHARGE_HEADER -> UPSTREAM_OF -> MOV-118
MOV-118 -> UPSTREAM_OF -> RO-119
RO-119  -> UPSTREAM_OF -> DA-100
DISCHARGE_HEADER -> UPSTREAM_OF -> E-301
PDI-S14 -> MEASURES -> S-14
TE-101B -> MEASURES -> P-101B
VE-101B -> MEASURES -> P-101B
PT-101  -> MEASURES -> DISCHARGE_HEADER
FT-101  -> MEASURES -> DISCHARGE_HEADER
FT-101  -> CONTROLS -> MOV-118
V-201   -> UPSTREAM_OF -> PCV-140
PCV-140 -> UPSTREAM_OF -> DA-100
V-201   -> AFFECTS_NPSHA_OF -> P-101B
S-14    -> AFFECTS_FLOW_TO -> P-101B
MOV-118 -> PROTECTS -> P-101B
```

---

## 6. Instrumentation and Control Notes

**N-01.** `FT-101` is the master flow signal for minimum-flow protection. `FIC-101` opens `MOV-118` on falling discharge flow; the recirculation path is sized to pass 72 m³/h, which is the minimum continuous stable flow of `P-101B` (approximately 30 % of BEP, BEP being 240 m³/h). `MOV-118` fails OPEN on loss of power or instrument air.

**N-02.** `PDI-S14` reads differential pressure across strainer `S-14`. Clean-element differential is approximately 0.2 bar at rated flow. Operations alarm is set at 0.5 bar. **As of the current campaign `PDI-S14` is trending toward 0.6 bar**, indicating progressive fouling of the `S-14` element and reduced suction availability to `P-101B`.

**N-03.** `TE-101B` comprises duplex Pt100 RTDs in the drive-end and non-drive-end bearing housings of `P-101B`. Refer to the equipment datasheet and the operating manual for alarm and trip settings — note that the two documents currently disagree on the alarm value and the discrepancy is under review by Reliability Engineering.

**N-04.** `VE-101B` accelerometers are mounted radially on both bearing housings. Evaluation is per ISO 20816-3 for Group 1 rigidly-mounted machines above 15 kW; measurements are reported as broadband velocity in mm/s RMS. Zone A/B boundary and Zone B/C boundary values are tabulated on the datasheet.

**N-05.** Seal system for `P-101B` is **API 682 Plan 23** — a closed-loop recirculation from the seal chamber through a pumping ring to seal cooler `SC-101B` and back to the seal chamber. Plan 23 is selected in preference to Plan 11 because the pumped fluid is at 105 °C, close to saturation, and Plan 23 circulates only the small seal-chamber inventory rather than continuously drawing hot discharge fluid across the faces. Cooling water to `SC-101B` is from the closed cooling water loop, tag `CWS-101B` / `CWR-101B`.

**N-06.** `P-101A` and `P-101B` share the common suction header. Simultaneous starting, or starting the standby pump while the duty pump is already drawing full flow, will transiently depress header pressure at the pump suction nozzles. Refer to the operating manual for the mandatory restart sequencing caution.

**N-07.** `RO-119` breaks down recirculation pressure from discharge (approximately 78 barg) to deaerator pressure (approximately 6 barg upstream of the sparger nozzle) in a single stage; the orifice is a multi-hole cascade type to control flashing and erosion.

**N-08.** Suction strainers `S-13` and `S-14` are permanent items, not temporary start-up cones. Element changeout requires the corresponding pump to be isolated and the parallel pump to carry full load.

**N-09.** Battery limits: `P-102` and `E-301` are shown for connectivity only and are not part of the BFW pump protection scheme.

---

## 7. Revision History

| Rev | Date | Description |
|---|---|---|
| 0 | 2019-03-14 | Issued for construction |
| 1 | 2020-07-02 | Added `PDI-S14`; strainer dP monitoring |
| 2 | 2022-01-19 | `MOV-118` replaced (fail-open actuator) |
| 3 | 2024-05-30 | Updated ISO 20816-3 reference (superseded ISO 10816-3) |
| 4 | 2026-06-11 | Added V-201 NPSHa interaction note N-02/N-06; topology list expanded |
