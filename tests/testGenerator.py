import importlib
import os
from pathlib import Path
import sys
sys.path.insert(0, "../Q-AutoDiaBFM/src")
import bugInvestigator as bI

bugDatasetRootDirectoryName = "bugDataset"
bugDatasetRootDirectoryPath = "../Q-AutoDiaBFM/tests/bugDataset"

def runTests(bugTestFiles, characteristicBugMessage):
    allTestsPassed = False
    failedTestFiles = []
    numberOfTestsPassed = 0

    for bugTestFile in bugTestFiles:
        bugTestFileName = os.path.basename(bugTestFile)
        bugTestFileProber = importlib.import_module(bugDatasetRootDirectoryName + "." + bugTestFileName[:-3],
                                                    bugDatasetRootDirectoryPath + "/" + bugTestFileName)
        bugTypeMessage = bI.classifyBugs(bugTestFileProber.buggyCode, bugTestFileProber, commandLine = False)
        if bugTypeMessage != characteristicBugMessage:
            failedTestFiles.append((bugTypeMessage, bugTestFile))
        numberOfTestsPassed += (bugTypeMessage == characteristicBugMessage)

    allTestsPassed = (numberOfTestsPassed == len(bugTestFiles))

    if not allTestsPassed:
        print(f"{len(bugTestFiles) - numberOfTestsPassed} tests failed! Failed tests are displayed below:\n") 
        for bugTypeMessage, failedTestFile in failedTestFiles:
            with open(failedTestFile) as bugFormatter:
                print(bugFormatter.read())
            print("(Wrong) error message:", bugTypeMessage, "\n")
    return allTestsPassed


def dynamicTestHandler(numberOfTests: int, testAttribute: str): # To be tested.
    testAttributeFunction = getattr(__name__, "test" + testAttribute)
    return testAttributeFunction(numberOfTests)

def testIncorrectGate():
    allTestsPassed = False
    bugTestFilesHandler = Path(bugDatasetRootDirectoryPath).glob('**/IncorrectGate*.py')
    bugTestFiles = [bugTestFile for bugTestFile in bugTestFilesHandler]
    characteristicBugMessage = "Incorrect gate(s) used."

    print("Testing incorrect usage of gate(s).")
    allTestsPassed = runTests(bugTestFiles, characteristicBugMessage)
    if allTestsPassed:
        print("All tests for detecting incorrect usage of gate(s) have passed!")
    return allTestsPassed

def testIncorrectInit():
    allTestsPassed = False
    bugTestFilesHandler = Path(bugDatasetRootDirectoryPath).glob('**/IncorrectInit*.py')
    bugTestFiles = [bugTestFile for bugTestFile in bugTestFilesHandler]
    characteristicBugMessage = "Incorrect initialization(s) attempted."

    print("Testing for the presence of incorrect initialization(s).")
    allTestsPassed = runTests(bugTestFiles, characteristicBugMessage)
    if allTestsPassed:
        print("All tests for detecting the presesnce of incorrect initialization(s) have passed!")
    return allTestsPassed

def testIncorrectMeasurement():
    allTestsPassed = False
    bugTestFilesHandler = Path(bugDatasetRootDirectoryPath).glob('**/IncorrectMeasurement*.py')
    bugTestFiles = [bugTestFile for bugTestFile in bugTestFilesHandler]
    characteristicBugMessage = "Measurement(s) performed incorrectly."

    print("Testing for the presence of incorrectly performed measurement(s).")
    allTestsPassed = runTests(bugTestFiles, characteristicBugMessage)
    if allTestsPassed:
        print("All tests for detecting the presence of incorrectly performed measurement(s) have passed!")
    return allTestsPassed

def testIncorrectQubitCount():
    allTestsPassed = False
    bugTestFilesHandler = Path(bugDatasetRootDirectoryPath).glob('**/IncorrectQubitCount*.py')
    bugTestFiles = [bugTestFile for bugTestFile in bugTestFilesHandler]
    characteristicBugMessage = "Incorrect number of qubits used."

    print("Testing usage of incorrect number of qubits.")
    allTestsPassed = runTests(bugTestFiles, characteristicBugMessage)
    if allTestsPassed:
        print("All tests for detecting usage of incorrect number of qubits have passed!")
    return allTestsPassed

def testIncorrectQubitOrder():
    allTestsPassed = False
    bugTestFilesHandler = Path(bugDatasetRootDirectoryPath).glob('**/IncorrectQubitOrder*.py')
    bugTestFiles = [bugTestFile for bugTestFile in bugTestFilesHandler]
    characteristicBugMessage = "Incorrect order of qubits used."

    print("Testing usage of incorrect order of qubits.")
    allTestsPassed = runTests(bugTestFiles, characteristicBugMessage)
    if allTestsPassed:
        print("All tests for detecting usage of incorrect order of qubits have passed!")
    return allTestsPassed

def runAllTests(): # Code to be updated
    return True