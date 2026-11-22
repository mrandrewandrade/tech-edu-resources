# Automotive relay trainer: reversible faults and test key

Insert one fault at a time with every source disconnected. Record the original configuration before changing it. Do not create shorts, defeat protection, reverse a diode-protected coil, or exceed ratings.

## Baseline expected observations

Assume a verified form-C relay, a fused 12 V feed to 30, lamp from 87 to return, and a manual coil switch. Replace approximate values with the reference-build measurements.

| Observation | Released | Energized |
|---|---|---|
| Relay mechanical state | released | operated |
| 30–87 continuity, power off | open | closed |
| 30–87a continuity, power off | closed | open |
| Terminal 30 to return | near source voltage | near source voltage |
| Terminal 87 to return | approximately 0 V through lamp path | near source voltage |
| Lamp voltage | approximately 0 V | near source voltage |

The released terminal-87 voltage can depend on the connected load and meter input. Treat it as a diagnostic observation, not a universal constant.

## Fault 1: open control switch

**Insertion:** disconnect the switch-to-coil conductor and insulate it.

**Expected clues:** protected load voltage remains at 30; coil voltage is absent or incomplete; relay never operates; 87 does not receive the contact feed.

**Useful tests:** coil high and low-side voltages, switch voltage drop in both positions, power-off continuity after isolation.

## Fault 2: removed load fuse

**Insertion:** remove the branch fuse and retain it visibly for restoration.

**Expected clues:** coil and relay operate; supply voltage exists before the fuse but not at terminal 30; lamp remains off.

**Useful tests:** voltage to ground on both fuse-holder sides. Do not use continuity mode on the energized holder.

## Fault 3: open lamp return

**Insertion:** disconnect and insulate the lamp return.

**Expected clues:** relay operates; source voltage reaches 30 and 87; lamp does not light; both lamp terminals may appear near source potential relative to supply negative because no load current flows.

**Useful tests:** voltage across the lamp and each lamp terminal to supply negative. This fault is a good warning that voltage-to-ground alone does not prove a complete circuit.

## Fault 4: load on 87a

**Insertion:** move the lamp feed from socket 87 to 87a with power removed.

**Expected clues:** lamp is on while the relay is released and off while energized. Voltage evidence matches the contact state; this is not necessarily a failed relay.

**Useful tests:** power-off released continuity and terminal-voltage table in both states.

## Optional software/driver faults

Use only after the approved driver works:

- wrong logical active level;
- program exits without cleanup but hardware bias still forces default-off;
- driver control lead removed;
- separate coil supply switched off while BeagleBone remains on.

Do not use a missing flyback diode as a repeated live fault. Suppression is a design requirement, not a destructive demonstration.

## Restoration checklist

- [ ] Every conductor returned to the photographed baseline.
- [ ] Fuse present and correct.
- [ ] Socket terminals seated and insulated.
- [ ] Lamp connected to intended contact.
- [ ] Control circuit restored.
- [ ] Power-off continuity rechecked.
- [ ] Reference voltage test passes before the next group.

