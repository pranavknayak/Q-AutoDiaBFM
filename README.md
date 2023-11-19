### Automated Detection of Quantum Bug Fix-Patterns [![GitHub version](https://badge.fury.io/gh/KrishnKher%2FQ-AutoDiaBFM.svg)](https://badge.fury.io/gh/KrishnKher%2FQ-AutoDiaBFM)
## Q-PAC
[![Visual Studio](https://badgen.net/badge/test/test/blue?icon=visualstudio)](https://badge.fury.io/gh/KrishnKher%2FQ-AutoDiaBFM)
[![GitHub](https://badgen.net/badge/test/test/purple?icon=github)](https://badge.fury.io/gh/KrishnKher%2FQ-AutoDiaBFM)

```Q-PAC``` is an automated tool that detects bug-fix patterns in quantum codes. The tools classifies pairs of buggy and patched codes based on AST-parsers, regex checks and other semantic checks. Currently, the tool is still in a proof-of-concept (PoC) stage and has been designed only for certain classes of Qiskit codes:
- `ExcessiveMeasurements`
- `IncorrectInitializations`
- `IncorrectMeasurements`
- `IncorrectOpaqueGates`
- `IncorrectHadamardGates`
- `IncorrectStandardGates`
- `UnequalBits`

Examples demonstrations have been provided under the tests folder.

# Instructions to run the source code:

1. Clone this repository:

```bash
git clone https://github.com/pranavknayak/Q-PAC
```

2. Navigate to the directory of the ```main.py``` file:

```bash
cd src
```

3. Pass in two strings of code, one being the buggy and the other, the patched one to the ```bugInvestigator.classifyBugs(buggy=..., patched=..., commandLine=...)``` method.

4. Run the following command in the console:

```bash
python3 main.py
```
