# Equipment Datasheet — Boiler Feed Pump `P-101B`
## Document No. DS-ROT-101B Rev. 3
**Service:** Boiler Feed Water, Train B
**Tag:** `P-101B`
**P&ID Reference:** PID-BFW-002 Rev. 4
**Specification Basis:** API 610 12th Edition (ISO 13709) — Type BB4
**Status:** AS-BUILT / CERTIFIED

---

## 1. Identification

| Item | Value |
|---|---|
| Manufacturer | Sulzer Pumps Ltd. |
| Model | MC 100-6 |
| Serial No. | 4471-0932-B |
| API 610 type | BB4 — radially split, between-bearings, multistage, ring-section |
| Year of manufacture | 2018 |
| Driver | 1 000 kW, 6.6 kV, 2-pole TEFC induction motor, tag `M-101B` |
| Coupling | Flexible disc-pack, spacer type, API 671 style, non-lubricated |
| Baseplate | Fabricated CS, fully grouted, API 610 Annex F |

---

## 2. Operating Conditions

| Parameter | Value |
|---|---|
| Pumped fluid | Deaerated boiler feed water |
| Fluid temperature (normal) | 105 °C |
| Fluid temperature (max) | 120 °C |
| Specific gravity at 105 °C | 0.955 |
| Vapour pressure at 105 °C | 1.21 bar a |
| Viscosity at 105 °C | 0.27 cP |
| Suction pressure (normal) | 1.35 bar a at nozzle |
| Discharge pressure (rated) | 78 barg |
| Differential pressure | 76.7 bar |
| pH (conditioned) | 9.2 – 9.6 |
| Dissolved O2 | < 7 ppb |

---

## 3. Hydraulic Data

| Parameter | Value |
|---|---|
| Rated flow | 240 m³/h |
| Rated total head | 820 m |
| Number of stages | 6 |
| Head per stage (rated) | 136.7 m |
| Best Efficiency Point (BEP) flow | 240 m³/h |
| Efficiency at BEP | 78.5 % |
| **Minimum continuous stable flow** | **72 m³/h (30 % of BEP)** |
| Minimum continuous thermal flow | 33 m³/h |
| Rated speed | 2 965 rpm |
| Absorbed power at rated point | 652 kW |
| Absorbed power at shutoff | 300 kW |
| Shutoff head | 985 m |
| NPSH required (NPSHr₃) at rated flow | 4.8 m |
| NPSH available at rated flow | 8.9 m |
| NPSH margin | 4.1 m (ratio 1.85, per API 610 clause 9.1 guidance) |
| Suction specific speed, Nss | 10 900 (US units) |
| Rated impeller diameter | 268 mm |
| Maximum impeller diameter | 285 mm |
| Minimum impeller diameter | 240 mm |
| Suction nozzle | 8 in, ASME B16.5 Class 300 RF |
| Discharge nozzle | 6 in, ASME B16.5 Class 900 RF |
| Direction of rotation | Clockwise viewed from driver end |

**Minimum flow note.** The minimum continuous stable flow of **72 m³/h** is the governing protection setpoint for `P-101B` and is the basis for sizing the recirculation line and the capacity of `MOV-118`. Operation below this value produces internal recirculation at the impeller eye and discharge tips, low-frequency hydraulic noise, elevated radial loads, and — most importantly for a high-head unit of this energy density — rapid conversion of absorbed power into heat in the trapped liquid. Sustained operation below minimum flow will raise both the pumped-fluid temperature and, via conduction through the shaft and the seal-flush loop, the bearing housing temperatures reported by `TE-101B`.

---

## 4. Performance Curve (tabulated, 268 mm impeller, 2 965 rpm)

| Flow (m³/h) | Total Head (m) | Efficiency (%) | Absorbed Power (kW) | NPSHr₃ (m) |
|---|---|---|---|---|
| 0 (shutoff) | 985 | 0 | 300 | — |
| 48 | 962 | 34.2 | 352 | 2.4 |
| 72 | 948 | 45.8 | 388 | 2.7 |
| 96 | 930 | 55.6 | 418 | 3.0 |
| 120 | 912 | 63.9 | 446 | 3.3 |
| 144 | 892 | 70.1 | 477 | 3.6 |
| 168 | 872 | 74.3 | 513 | 4.0 |
| 192 | 856 | 76.9 | 556 | 4.3 |
| 216 | 838 | 78.2 | 602 | 4.5 |
| **240 (BEP/rated)** | **820** | **78.5** | **652** | **4.8** |
| 264 | 796 | 77.8 | 703 | 5.4 |
| 288 | 764 | 75.1 | 762 | 6.3 |
| 312 | 722 | 70.4 | 833 | 7.6 |
| 336 (end of curve) | 668 | 63.8 | 916 | 9.5 |

Absorbed power is computed throughout at the site specific gravity of 0.955 (P = ρgQH/η), so the column is internally consistent from shutoff to end of curve. Motor sizing is against the end-of-curve value of 916 kW, giving the 1 000 kW driver an API 610 clause 6.1.4 margin without relying on system resistance to limit runout.

Preferred operating region per API 610 clause 6.1.11: **168 – 288 m³/h** (70 % – 120 % of BEP). Allowable operating region: **72 – 312 m³/h**.

---

## 5. Materials of Construction

| Component | Material | Notes |
|---|---|---|
| Barrel / stage casings | ASTM A216 WCB carbon steel | API 610 material class S-6 |
| Impellers (6 off) | ASTM A743 CA6NM (13Cr-4Ni) | Hardened, 269–302 HB |
| Diffusers | ASTM A743 CA6NM | |
| Shaft | ASTM A276 Type 431 SS | 302 HB min |
| Shaft sleeves | 431 SS, hard-faced | Chrome oxide coating under seal |
| Wear rings — stationary | 410 SS, nitrided | Diametral clearance 0.45 mm new |
| Wear rings — rotating | 420 SS | Hardness differential ≥ 50 HB |
| Balance drum | 410 SS, hardened | Balance-line back to suction |
| Gaskets | Spiral wound 316L/graphite | |
| Casing bolting | ASTM A193 B7 / A194 2H | |

---

## 6. Mechanical Seal

| Parameter | Value |
|---|---|
| Seal type | Cartridge, single, balanced, pusher-type |
| API 682 category / arrangement / type | Category 2, Arrangement 1, Type A |
| **Flush plan** | **API 682 Plan 23** |
| Seal size | 60 mm |
| Face materials | Rotating: sintered silicon carbide; Stationary: resin-impregnated carbon |
| Secondary sealing | FKM O-rings (Type A) |
| Metal parts | 316 SS; springs Alloy C-276 |
| Seal chamber pressure | 3.8 barg (balance-line referenced) |
| Seal cooler | `SC-101B`, water-cooled shell-and-coil |
| Cooling water flow to `SC-101B` | 2.4 m³/h at 32 °C supply |
| Pumping ring | Bi-directional tangential, integral to cartridge |
| Seal chamber temperature (normal) | 62 °C |
| Seal chamber temperature (alarm) | 80 °C |
| **Seal gland bolt torque** | **45 N·m** |
| Gland bolt size / quantity | M12 × 1.75, 4 off, lubricated with anti-seize |
| Tightening pattern | Diagonal (star), three passes at 40 % / 70 % / 100 % |

**Plan 23 rationale.** Plan 23 recirculates the seal-chamber inventory in a closed loop through the cooler by means of the pumping ring, rather than continuously importing hot fluid from the pump discharge (Plan 11) or from the seal chamber to a drain. Because only a small, already-cooled inventory circulates, the heat load on the cooler is modest and the faces run at a stable margin below the fluid saturation temperature. This is the standard arrangement for hot-water boiler feed service per API 682 clause 9 flush-plan selection guidance. A throat bushing is fitted to isolate the seal chamber from the pumped fluid; loss of the closed-loop circulation (fouled cooler, lost cooling water, or a stalled pumping ring) removes the isolation benefit and the seal chamber will track pumped-fluid temperature upward.

---

## 7. Bearings and Lubrication

| Parameter | Value |
|---|---|
| Radial bearing — drive end | Hydrodynamic sleeve, plain cylindrical, babbitt lined, 90 mm bore |
| Radial bearing — non-drive end | Hydrodynamic sleeve, babbitt lined, 90 mm bore |
| Thrust bearing | Tilting-pad, double-acting, 6 pads per side, 130 mm |
| Lubrication | Pressurised oil, ISO VG 32 turbine oil (R&O) |
| Lube oil supply pressure | 1.5 barg at bearing header |
| Lube oil supply temperature | 45 °C ± 3 °C |
| Lube oil flow (total) | 42 L/min |
| Oil cooler | `OC-101B`, shell-and-tube, CW 32 °C |
| Oil reservoir capacity | 180 L |
| Housing sealing | Non-contacting labyrinth, bearing isolators |
| **Bearing temperature ALARM** | **90 °C** |
| **Bearing temperature TRIP** | **100 °C** |
| Bearing temperature normal band | 58 – 72 °C |
| Temperature element | `TE-101B`, duplex Pt100 RTD, 3-wire, embedded in babbitt |

Alarm and trip values above are the OEM-certified settings and reflect API 610 clause 6.10 guidance on hydrodynamic bearing metal temperature limits. The measured point is the babbitt metal temperature, not the oil drain temperature; the oil drain runs typically 12–18 °C below the metal reading.

---

## 8. Vibration Acceptance — ISO 20816

Evaluation per **ISO 20816-1** (general) and **ISO 20816-3** (industrial machines, Group 1 — rated power above 300 kW, rigid support). Broadband velocity measured radially at both bearing housings by `VE-101B`, 10–1 000 Hz, reported in mm/s RMS.

| Zone | Description | Limit (mm/s RMS) |
|---|---|---|
| A | Newly commissioned machines | ≤ 2.3 |
| B | Acceptable for unrestricted long-term operation | > 2.3 to ≤ 4.5 |
| C | Unsatisfactory for long-term; short-term operation only | > 4.5 to ≤ 7.1 |
| D | Damaging; shutdown required | > 7.1 |

Site settings derived from the above: **alert at 4.5 mm/s RMS**, **shutdown at 7.1 mm/s RMS**. Factory shop-test result at rated point was 1.6 mm/s RMS (Zone A). Shaft relative displacement is not monitored on this machine; there are no proximity probes fitted.

Note for diagnostics: operation below the 72 m³/h minimum continuous flow characteristically produces broadband energy rise below running speed (0.4–0.8 × rpm) from suction recirculation, rather than a clean 1× or 2× line-frequency signature.

---

## 9. Spare Parts List

| Item | Part No. | Qty per pump | Category |
|---|---|---|---|
| Impeller, 268 mm, CA6NM | MC100-IMP-268 | 6 | Capital |
| Stage casing | MC100-STG-06 | 5 | Capital |
| Shaft, 431 SS | MC100-SFT-431 | 1 | Capital |
| Wear ring set (stationary + rotating) | MC100-WRS-A | 6 sets | Commissioning / 2-yr |
| Balance drum + sleeve | MC100-BDS-01 | 1 set | Capital |
| Cartridge mechanical seal, 60 mm | MSL-60-C2A1-A | 1 | 2-yr / insurance |
| Seal repair kit (faces, O-rings, springs) | MSL-60-RK | 2 | 1-yr consumable |
| Sleeve bearing shells, 90 mm | MC100-BRG-90 | 2 pr | 2-yr |
| Thrust pad set, tilting pad | MC100-THR-130 | 1 set | 2-yr |
| Coupling disc pack | CPL-DP-4471 | 2 | 1-yr consumable |
| Gasket set, full casing | MC100-GSK-FULL | 2 | 1-yr consumable |
| Bearing isolator, DE / NDE | MC100-ISO-90 | 2 pr | 1-yr consumable |
| RTD, Pt100 duplex (`TE-101B`) | INST-RTD-DPX | 2 | 1-yr consumable |
| Strainer element for `S-14`, 40 mesh SS316 | STR-T8-40M | 2 | 1-yr consumable |
| Lube oil filter element | LOF-10M-101 | 4 | 6-month consumable |
| Seal cooler tube bundle (`SC-101B`) | SC101-BND | 1 | 5-yr |

---

## 10. Notes and Certification

1. Hydrostatic test: casing tested at 1.5 × maximum allowable working pressure, 210 barg, 30 min hold — PASSED, cert. HT-4471-02.
2. Performance test: API 610 Acceptance Grade 1B, witnessed — PASSED, cert. PT-4471-05.
3. NPSHr test: 3 % head-drop method at four flows — PASSED, cert. NP-4471-01.
4. Mechanical run test: 4 h at rated speed, unfiltered vibration 1.6 mm/s RMS — PASSED.
5. Material certification: EN 10204 3.1 for all pressure-retaining and shaft components.
6. Parallel unit `P-101A` is the same model and revision; parts are fully interchangeable. `P-102` and `E-301` are unrelated equipment and share no spares with this machine.
7. Any deviation between this datasheet and the operating manual shall be raised as a Management of Change item to Rotating Equipment Engineering. A known open item exists on the bearing temperature alarm value and on the seal gland bolt torque value.

---

**Rev 3 — issued 2026-04-08.** Supersedes Rev 2 (2023-11-20). Changes: ISO 10816-3 reference updated to ISO 20816-3; minimum continuous stable flow restated explicitly as 72 m³/h; spare parts list extended.
