- add in comments if possbile [in progress]
- resolve all the comments with questions
- if possible try to make an enum for threadingStyle which will be applicable in all the files
- right now even there are multiple bug-fixes in the file, it will only report the first bug it finds. Improve this to show all the bug-fixes if possible.
- Add in threading while testing
- Current individual bug tests assume commandLine = False; improve this later if possible
- For now in IncorrectGate, we have implemented assuming QuantumCircuit is used only once.
- In testGenerator.py, add a way in runTests, by which it can iterate over all the bugTypedirectories 
and run the test<bugType> function under status |=.