check bugs hierarchically
make the bug detectors themselves hierarchically in the bug detectors folder
to create a new bug type, make an appropriate folder if not already there in the appropriate category
if you need to create a folder, make sure that you add in a 'probe.py' file which will help controller.py to probe down the tree of bug types.

ther should be exactly one probe.py per folder, otherwise we will raise an exception? Becauase it may get confused otherwise.