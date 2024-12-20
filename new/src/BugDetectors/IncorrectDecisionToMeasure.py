import ast 
import re


class IncorrectDecisionToMeasure():
    def _checkBinRepCalls(self, code_ast):
        binrep_call = []
        for node in code_ast:
            if (
                isinstance(node, ast.Call) and
                isinstance(node.func, ast.Attribute) and
                isinstance(node.func.value, ast.Name)
            ):
                if (
                    node.func.value.id == "np" and
                    node.func.attr == "binary_repr"
                ):
                    print("Cool", node.args)  
                    binrep_call.append(node.args)  
                
        return binrep_call

    def _checkRepresentation(self, codeDiff, astSample):

        buggy, patched = codeDiff[0], codeDiff[1]
        buggyList = list(filter(("").__ne__, buggy.split("\n")))
        patchedList = list(filter(("").__ne__, patched.split("\n")))

        buggyAST, patchedAST = ast.walk(astSample[0]), ast.walk(astSample[1])    

        buggy_binrep, patched_binrep = self._checkBinRepCalls(buggyAST), self._checkBinRepCalls(patchedAST)

        if len(buggy_binrep) != len(patched_binrep):
            return True
        else:
            for iter_ in range(0, len(buggy_binrep)):
                if buggy_binrep[iter_] != patched_binrep[iter_]:
                    return True

        return False

    def _detectIncorrectDecisionToMeasure(self, codeDiff, astSample):
        status = False
        bugTypeMessage = "Incorrect Decision To Measure detected."
        try:
            status = self._checkRepresentation(codeDiff, astSample)
            print("checkRepresentation WORKS")
        except:
            status = False
            print("error in checkRepresentation")
            raise

        return status, bugTypeMessage

    def assessBugType(self, codeSample, astSample):
        return self._detectIncorrectDecisionToMeasure(codeSample, astSample)