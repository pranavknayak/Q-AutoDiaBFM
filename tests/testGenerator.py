import importlib
import os
from pathlib import Path
import sys
import glob
sys.path.insert(0, "../Q-AutoDiaBFM/src")
import bugInvestigator as bI

bugDatasetRootDirectoryName = "bugDataset"
bugDatasetRootDirectoryPath = "../Q-AutoDiaBFM/tests/bugDataset"

def runTests(bugTestFiles, characteristicBugMessage):
    allTestsPassed = False
    bugCounter = 1
    failedTestFiles = []
    numberOfTestsPassed = 0

    for bugTestFile in bugTestFiles:
        #bugTestFileName = os.path.basename(bugTestFile)
        print(bugDatasetRootDirectoryName + "." + bugTestFile[:-3],
                                                    bugDatasetRootDirectoryPath + "/" + bugTestFile)
        bugTestFileProber = importlib.import_module(bugDatasetRootDirectoryName + "." + bugTestFile[:-3],
                                                    bugDatasetRootDirectoryPath + "/" + bugTestFile)
        bugTypeMessage = bI.classifyBugs(bugTestFileProber.buggyCode, bugTestFileProber.patchedCode, commandLine = False)
        if bugTypeMessage != characteristicBugMessage:
            failedTestFiles.append((bugCounter, bugTypeMessage, bugTestFile))
        numberOfTestsPassed += (bugTypeMessage == characteristicBugMessage)
        bugCounter += 1

    allTestsPassed = (numberOfTestsPassed == len(bugTestFiles))

    if not allTestsPassed:
        print(f"{len(bugTestFiles) - numberOfTestsPassed} / {len(bugTestFiles)} tests failed! Failed tests are displayed below:\n") 
        for bugIndex, bugTypeMessage, failedTestFile in failedTestFiles:
            print("<===============================", f"Test {bugIndex}", "===============================>", "\n")
            with open(failedTestFile) as bugFormatter:
                print(bugFormatter.read())
            print("(Wrong) error message:", bugTypeMessage, "\n")
    return allTestsPassed


def dynamicTestHandler(numberOfTests: int, testAttribute: str): # To be tested.
    testAttributeFunction = getattr(__name__, "test" + testAttribute)
    return testAttributeFunction(numberOfTests)

def testIncorrectGate():
    allTestsPassed = False
    penultimateAddress = "IncorrectGate."
    incorrectGateAddress = bugDatasetRootDirectoryPath + "/IncorrectGate/"
    bugTestFilesHandler = Path(bugDatasetRootDirectoryPath).glob('**/IncorrectGate/IncorrectGate*.py')
    bugTestFiles = [penultimateAddress + bugTestFile for bugTestFile in os.listdir(incorrectGateAddress) if bugTestFile[-3:] == ".py"]
    print(bugTestFiles)
    characteristicBugMessage = "Incorrect usage of gate(s)."

    print("Testing incorrect usage of gate(s).")
    allTestsPassed = runTests(bugTestFiles, characteristicBugMessage)
    if allTestsPassed:
        print("All tests for detecting incorrect usage of gate(s) have passed!")
    return allTestsPassed

def testIncorrectInit():
    allTestsPassed = False
    penultimateAddress = "IncorrectInit/"
    bugTestFilesHandler = Path(bugDatasetRootDirectoryPath).glob('**/IncorrectInit/IncorrectInit*.py')
    bugTestFiles = [penultimateAddress + bugTestFile for bugTestFile in bugTestFilesHandler]
    characteristicBugMessage = "Incorrect initialization(s) attempted."

    print("Testing for the presence of incorrect initialization(s).")
    allTestsPassed = runTests(bugTestFiles, characteristicBugMessage)
    if allTestsPassed:
        print("All tests for detecting the presesnce of incorrect initialization(s) have passed!")
    return allTestsPassed

def testIncorrectMeasurement():
    allTestsPassed = False
    penultimateAddress = "IncorrectMeasurement."
    bugTestFilesHandler = Path(bugDatasetRootDirectoryPath).glob('**/IncorrectMeasurement/IncorrectMeasurement*.py')
    bugTestFiles = [penultimateAddress + bugTestFile for bugTestFile in bugTestFilesHandler]
    characteristicBugMessage = "Measurement(s) performed incorrectly."

    print("Testing for the presence of incorrectly performed measurement(s).")
    allTestsPassed = runTests(bugTestFiles, characteristicBugMessage)
    if allTestsPassed:
        print("All tests for detecting the presence of incorrectly performed measurement(s) have passed!")
    return allTestsPassed

def testIncorrectQubitCount():
    allTestsPassed = False
    penultimateAddress = "IncorrectQubitCount/"
    bugTestFilesHandler = Path(bugDatasetRootDirectoryPath).glob('**/InorrectQubitCount/IncorrectQubitCount*.py')
    bugTestFiles = [penultimateAddress + bugTestFile for bugTestFile in bugTestFilesHandler]
    characteristicBugMessage = "Incorrect number of qubits used."

    print("Testing usage of incorrect number of qubits.")
    allTestsPassed = runTests(bugTestFiles, characteristicBugMessage)
    if allTestsPassed:
        print("All tests for detecting usage of incorrect number of qubits have passed!")
    return allTestsPassed

def testIncorrectQubitOrder():
    allTestsPassed = False
    penultimateAddress = "IncorrectQubitOrder/"
    bugTestFilesHandler = Path(bugDatasetRootDirectoryPath).glob('**/IncorrectQubitOrder/IncorrectQubitOrder*.py')
    bugTestFiles = [penultimateAddress + bugTestFile for bugTestFile in bugTestFilesHandler]
    characteristicBugMessage = "Incorrect order of qubits used."

    print("Testing usage of incorrect order of qubits.")
    allTestsPassed = runTests(bugTestFiles, characteristicBugMessage)
    if allTestsPassed:
        print("All tests for detecting usage of incorrect order of qubits have passed!")
    return allTestsPassed

def runAllTests(): # Code to be updated
    return True