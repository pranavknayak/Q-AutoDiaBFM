### Automatic Diagnosis of Quantum Software Bug Fix Motifs

## Q-Diff
```Q-Diff``` is an automated tool that detects bug-fix patterns in quantum codes. The tools classifies pairs of buggy and patched codes based on AST-parsers, RegEx checks and other semantic checks. Currently, the tool is still in a proof-of-concept (PoC) stage and has been designed only for certain classes of Qiskit codes, namely those which only have a single bug in a single line in the buggy code, of any of the following $$3$$ types:
- ```IncorrectGate```
- ```IncorrectInit```
- ```IncorrectMeasurement```

# Instructions to run the source code:

1. Clone this repository:

```bash
git clone https://github.com/KrishnKher/Q-AutoDiaBFM
```

2. Navigate to the main.py file:

```bash
cd src/main.py
```

3. Pass in two strings of code, one being the buggy and the other, the patched one to the bugInvestigator.classifyBugs method.

4. Run the following command in the console:

```bash
python main.py.
```
  
 # Instructions to run the tests:
 
1. Clone this repository:

```bash
git clone https://github.com/KrishnKher/Q-AutoDiaBFM
```

2. Navigate to the testRunner.py file:

```bash
cd src/tests.testRunner.py
```

3. Pick a test method from src/tests/testGenerator.py and run it inside src/tests/testRunner.py.

4. Run the following command in the console:

```bash
python testRunner.py
```
  
  Please note that an example is already present in the tests folder.
