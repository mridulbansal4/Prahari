# UTILITIES / BFW AREA — SHIFT HANDOVER LOG

Board 3 — Deaerator, BFW pumps, HP steam gen
Ops shift log. Handwritten book transcribed to file for the reliability review.
Shifts: A = 06:00-14:00, B = 14:00-22:00, C = 22:00-06:00
Initials: RKS, AJ, PVN, MTR, SD, GK, HB, NKV

---

**2026-05-28 / Shift A / RKS**
Took over from C. Nothing much o/n. 101B running, 101A standby.
FT-101 ard 175 at 07:00, drifting down thru morning. PDI-S14 = 0.53. alarm still standing, been standing since May 11. Ack'd again. Told supervisor again.
TE-101B 74 at handover, 81 by 13:30. Ambient 38.
NOTE for anyone new on board — TE-101B reads high. Not by much but it's consistent. Checked it with the portable pyro gun on the OB housing last month, gun said 77 when DCS said 81. So abt 5% high. Don't panic at 85, but don't ignore it either.
Strainer needs doing. Its been on the list.

---

**2026-05-28 / Shift B / AJ**
From RKS. 101B hot as usual on the afternoon. TE-101B peaked 86 abt 15:40, came off after 17:00 when ambient dropped. Same as always. Deducting the 5% thats really ~82.
S-14 dP 0.54.
MOV-118 — asked it to open at 16:10 when flow dipped, position feedback went to 11% and sat there. Left it, flow recovered on its own by 16:35. This valve is sticky. Its always sticky in summer. Winter its fine.
Deaerator level steady, chem on spec.
101A on standby, warm.

---

**2026-05-30 / Shift C / PVN**
Quiet night. 101B running fine overnight, TE-101B back to its normal 68 by 03:00. Thats the pattern — its a daytime problem not a nighttime problem.
FT-101 recovered to 190 overnight, demand low.
PDI-S14 0.51 (flow is higher at night so dP reads higher for a given fouling, careful reading it raw)
Nothing else. Handing to A.

---

**2026-06-02 / Shift A / MTR**
New on this board so writing more than usual.
Briefed by RKS on the two things you have to know here:
1. TE-101B reads ~5% high vs the portable. Confirmed w/ pyrometer.
2. **NEVER restart P-101A before P-101B after a shutdown.** 101B goes first, always. If you start 101A first you get cavitation in the suction header and 101B comes up on vapour. RKS says this has bitten people before. 101B FIRST.
Also told MOV-118 sticks when its hot out.
Shift itself uneventful. TE-101B 79 at end of shift. S-14 0.55.

---

**2026-06-04 / Shift B / SD**
Handover from MTR.
Hot day, 43. Predictable — 101B ran hot all afternoon. TE-101B 88 at 15:20, high temp alarm came in on DCS. Ack'd. Real value abt 84 allowing for the 5%.
Flow was down to 96 at worst. MOV-118 commanded open by the low flow logic, feedback 9%, basically didnt move. Beat on the actuator housing w/ the soft hammer, went to 40%, flow came up. Not a fix.
Raised WO for MOV-118. WO number in the book.
S-14 0.56. Somebody please clean this strainer.

---

**2026-06-07 / Shift C / GK**
o/n normal. 101B TE-101B 66-71 all night. flow 200+.
Read back the last few entries. Everyone is writing the same thing abt S-14 and 118. Its not getting done because you have to swap to 101A to pull the basket and nobody wants to swap pumps in peak season.
For the record I think thats the wrong call.

---

**2026-06-11 / Shift A / RKS**
Back on days.
S-14 dP 0.57 now. Was 0.2 when it was clean in Nov 24. Its nearly triple.
FT-101 down to 162 steady state daytime. It used to run 230+.
TE-101B tracking up week on week not just day on day. 77 at 08:00, 84 by 13:00, ambient 39.
Vib guys came thru w/ the route box. Didnt tell me the number, said "not great, its in the report".
101A standby, spun it for 10 min on recirc to keep it happy. Started 101B first obviously.

---

**2026-06-11 / Shift B / HB**
From RKS.
Nothing dramatic. TE-101B 87 peak. alarm in, ack'd. its the afternoon thing again.
Gland on 101B weeping slightly on startup this morning per RKS, cleared when it warmed thru. He said watch it. I watched it. Still dry now at 21:00.
S-14 0.57.

---

**2026-06-15 / Shift A / AJ**
!! Deaerator level control upset abt 09:40, LT went bad-PV for ~6 min. Tripped the boiler on drum lvl low-low. Full unit stop.
Restart at 11:20. **Started 101B FIRST then 101A.** Per the rule. No issues, no cavitation.
(Reminder to everyone: 101B first. If you bring 101A up first the suction header drops and 101B cavitates. This is not optional.)
After restart S-14 dP jumped to 0.59 — the thermal transient always shakes more scale loose off the pipework and it lands in the basket. Every shutdown makes the strainer worse.
101B TE-101B settled at 81 post restart, ambient 40.

---

**2026-06-16 / Shift C / NKV**
Post-upset watch. All stable.
101B temps normal for night, 69-73.
S-14 0.58, its not coming back down on its own.
FT-101 155 overnight which is low for a night — the strainer is really choking it now.

---

**2026-06-19 / Shift B / SD**
Ambient 44. Worst day so far.
TE-101B: 82 at 14:00, 89 at 15:50, held 87-89 till 18:00. High temp alarm standing thru. Corrected for the 5% thats ~85 real which is the number in the operating manual as the alarm anyway. So depending which document you read we are either fine or we are in alarm. Somebody should sort out which limit is right — the manual says 85, the datasheet on the wall says 90 alarm 100 trip.
FT-101 dropped to 71 at 16:10. **That is below min flow (72).** MOV-118 asked to open, feedback 8%. Stuck again. Same as June 4. WO is still open.
Hit it w/ the hammer again, got to 35%, flow to 105.
This is exactly what happened in 2023 before the seal went. Reading the incident report on the shelf. Same valve, same strainer, same hot afternoon.
Escalated to shift supt verbally. Writing it here too so its on record.

---

**2026-06-20 / Shift A / RKS**
Read SD's entry. Agree completely.
Called the RE. He's aware. Says the strainer clean + MOV-118 job needs a pump swap window and its going to planning.
Meanwhile: standing instruction from me — if FT-101 goes below 100, dont wait for the low flow logic, go and open 118 manually/by hand. Dont let 101B sit below 72. It heats up fast once its down there.
S-14 0.58. TE-101B 85 peak today, ambient 41.

---

**2026-06-23 / Shift C / GK**
Night. quiet.
101B fine overnight as always. 70ish.
Did a pyro check on the OB brg housing at 02:00 out of curiosity. Portable said 67, DCS TE-101B said 70. Thats 4.5% high. Consistent w/ what RKS found. So the ~5% offset is real and its been there a long time. Its not drifting, its just offset.
Somebody should get instruments to calibrate it or at least write it down somewhere official instead of in this book.

---

**2026-06-26 / Shift B / HB**
Hot again, 42.
TE-101B 88 peak 16:00. usual.
Seal gland on 101B weeping again at start of shift, few drops a min, cleared by 15:00 once hot. Second time this month. RKS said the seal cooler is probably furred up — theres no gauge on that loop so you cant tell.
Felt the cooler by hand (carefully) — outlet is much hotter than it should be. Not much temp drop across it at all.
S-14 0.59.
MOV-118 not asked for today, flow held above 130.

---

**2026-06-30 / Shift A / PVN**
Vib + IR route done this morning w/ the PdM guy. He let me see the sheet this time. OB radial 5.4 mm/s. He said thats Zone C on the ISO chart, which means "dont run like this indefinitely". Says it doesnt look like unbalance or misalignment, looks like a flow problem — lot of broadband hash low down in the spectrum.
Told him about S-14 and 118. He said that fits.
IR: brg housings 81/86, thrust 89, seal chamber 97, seal cooler outlet 71. Motor all normal, ~60s. So its the pump end thats hot not the motor.
S-14 0.58, FT-101 158.
TE-101B 84 at end of shift, ambient 41.

---

**2026-07-02 / Shift C / NKV**
Overnight normal. 101B 68-72.
Note — swapped to 101A for 3 hrs 01:00-04:00 to let maint look at a leaking drain on 101B discharge. Small job.
Bringing 101B back on — **101B started first? no — 101B was the one going BACK on, 101A was already running.** Careful here: the rule is about restart after a SHUTDOWN, when both are off. If both are off, 101B goes first. In this case 101A was already up so it was a normal swap and it was fine.
Wrote that out because I nearly overthought it at 04:00 in the morning.

---

**2026-07-06 / Shift B / AJ**
40 deg. TE-101B 86 peak.
MOV-118 — tested it deliberately at 15:00 while flow was moderate. Commanded open. Took 90 seconds to get to 30%, then jumped to full. So its not fully seized, its galling on the stem and sticking then breaking free. Classic. It'll seize properly one of these days.
Logged against the existing WO.
S-14 0.59-0.60. Basically 3x clean value.

---

**2026-07-09 / Shift A / MTR**
Quiet-ish.
S-14 0.60. FT-101 149 daytime. Thats the lowest sustained figure Ive seen on this board.
TE-101B 83 at 13:30, ambient 37 so a milder day and it still got to 83.
Thing Ive noticed writing these up — the hot afternoon thing is getting worse year on year. Old hands say 101B "always ran hot on hot afternoons" but the old logs from 2024 show it peaking 76-78 on a 40 degree day. Now its 86-89 on a 40 degree day. Same weather, hotter pump. Thats not weather, thats the machine.

---

**2026-07-12 / Shift C / GK**
Night. Nothing to report on 101B, 69-73 as usual.
S-14 0.60.
E-301 level control was hunting a bit, instrument aware, unrelated to us.
P-102 normal.

---

**2026-07-15 / Shift B / SD**
43 deg. Bad afternoon.
TE-101B: 84 at 14:00 → 90 at 16:20. Ninety. High temp alarm in from 15:10, standing.
Corrected for offset thats ~85-86 real. Still too hot.
FT-101 bottomed at 68 around 16:30. **Below min flow again.** Followed RKS's standing instruction, went out and hand wound MOV-118 open before the auto ever got it moving. Flow to 112 within 3 min, TE-101B started coming off within 15 min. Peaked 90, back to 84 by 17:15.
So the fix works. Its just that the valve wont do it by itself and the strainer is why the flow is low in the first place.
Reported to supt. Wrote it up. Again.

---

**2026-07-18 / Shift A / RKS**
S-14 dP **0.60**. Alarm standing since 11 May. That is 68 days.
FT-101 149.
TE-101B 82 at end of shift, ambient 39.
Gland weeping on start again this morning.
Summary of where we are, for whoever picks this up:
- S-14 is clogged. 0.2 clean, 0.5 alarm, sitting at 0.6.
- Because of that 101B cant draw flow. Down to 149 steady, dips under 72 on hot afternoons.
- MOV-118 is meant to protect against that and it sticks. In summer. Every summer.
- So 101B runs below min flow, churns, and gets hot. TE-101B climbing.
- TE-101B reads ~5% high so the real numbers are a bit better than the panel says, but the trend is the trend and the trend is up.
- The seal cooler is fouled too, no instrumentation on that loop so we're guessing by hand-feel.
- This is the 2023 sequence again. Read INC-2023-0814 if you havent.
Handing over. Please chase planning for the pump swap window.

---

**2026-07-20 / Shift B / HB**
From day shift.
41 deg, TE-101B 87 peak, alarm in, ack'd, usual afternoon.
FT-101 low of 79. Didnt go under 72 today. Didnt need to touch 118.
S-14 0.60.
Nothing new. Everything above still applies.

---

*Book continues. Transcription ends 2026-07-20.*
