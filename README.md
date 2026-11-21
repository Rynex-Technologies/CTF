# Rynex Technologies CTF Challenges

This public repository contains participant-ready challenge releases maintained by Rynex Technologies.

## Current challenges

- [**GHOST ISA archive**](GhostISA.zip) — Reverse Engineering, Hard. Custom virtual-machine bytecode analysis.
- [**The Forgotten Opcode archive**](ForgottenOpcode.zip) — Reverse Engineering, Medium. EVM runtime bytecode analysis.
- [**Phase Echo archive**](PhaseEcho.zip) — Cryptography, Insane. An offline mathematical cryptanalysis challenge.
- [**Cipherfall archive**](Cipherfall.zip) — Reverse Engineering, Hard. A Linux x86-64 binary analysis challenge.

All archives use the password: `rynextechnologies`.

## GHOST ISA

- **Category / difficulty:** Reverse Engineering / Hard
- **Expected solve time:** 2–5 hours for experienced players
- **Challenge archive:** [`GhostISA.zip`](GhostISA.zip)
- **Contents:** Compiled VM interpreter, compiled validator program, and participant README.

Extract `GhostISA.zip` with the password above and follow its `README.txt`.
The package is fully offline and requires only a 64-bit Linux system with a
standard C runtime. No network access, Docker, or additional packages are
needed. No source code, ISA documentation, flag, or write-up is included.

## The Forgotten Opcode

- **Category / difficulty:** Reverse Engineering / Medium
- **Challenge archive:** [`ForgottenOpcode.zip`](ForgottenOpcode.zip)
- **Contents:** Participant README, runtime bytecode, instance details, offline runner, and license.
- **Interface:** `validate(bytes) returns (bool)`

Extract `ForgottenOpcode.zip` with the password above and follow its `README.md`.
The package includes `run_offline.py`, so the challenge runs fully offline on
any machine with Python 3. No node, network service, or external tooling is
required. No source code, flag, or write-up is included. The flag format is
`RTCTF{...}`.

## Phase Echo

- **Category / difficulty:** Cryptography / Insane
- **Expected solve time:** 4–12 hours for experienced players
- **Challenge archive:** [`PhaseEcho.zip`](PhaseEcho.zip)
- **Contents:** Participant brief, Python challenge implementation, captured output, requirements, and Dockerfile.

Extract `PhaseEcho.zip` with the password above, then follow the archive's `PhaseEcho/README.md`. The challenge can be run locally with Python 3 and its listed requirements, or with Docker. No network access or submission platform is involved; this is for your own practice.

## Cipherfall

- **Category / difficulty:** Reverse Engineering / Hard
- **Target:** Linux x86-64 ELF
- **Challenge archive:** [`Cipherfall.zip`](Cipherfall.zip)
- **Contents:** Participant brief, analysis executable, and three encrypted artifacts.

Extract `Cipherfall.zip` with the password above and follow its participant README. There is no flag submission platform.

The private solutions repository contains author-only source, flags, and write-ups; none of those materials are included in these public challenge archives.

## Safety

Challenge files are supplied for personal practice and authorized CTF analysis only. Use an isolated environment and do not run unknown binaries on systems containing sensitive data. There is no flag submission platform for this practice challenge.
