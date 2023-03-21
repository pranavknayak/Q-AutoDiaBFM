### Automatic Diagnosis of Quantum Software Bug Fix Motifs

## Q-Diff
```Q-Diff``` is an automated tool that detects bug-fix patterns in quantum codes. The tools classifies pairs of buggy and patched codes based on AST-parsers, RegEx checks and other semantic checks. Currently, the tool is still in a proof-of-concept (PoC) stage and has been designed only for certain classes of Qiskit codes, namely those which only have a single bug in a single line in the buggy code, of any of the following $3$ types:
- ```IncorrectGate```.
- ```IncorrectInit```.
- ```IncorrectMeasurement```.

Examples demonstrations have been provided under the tests folder.

# Instructions to run the source code:

1. Clone this repository:

```bash
git clone https://github.com/KrishnKher/Q-AutoDiaBFM
```

2. Navigate to the directory of the ```main.py``` file:

```bash
cd src
```

3. Pass in two strings of code, one being the buggy and the other, the patched one to the ```bugInvestigator.classifyBugs($\cdot$, $\cdot$, $\cdot$)``` method.

4. Run the following command in the console:

```bash
python3 main.py
```
  
 # Instructions to run the tests:
 
1. Clone this repository:

```bash
git clone https://github.com/KrishnKher/Q-AutoDiaBFM
```

2. Navigate to the directory of the ```testRunner.py``` file:

```bash
cd tests
```

3. Pick a test method from ```tests/testGenerator.py``` and run it inside ```tests```.

4. Run the following command in the console:

```bash
python3 testRunner.py
```
  
  Please note that an example is already present in the tests folder.
