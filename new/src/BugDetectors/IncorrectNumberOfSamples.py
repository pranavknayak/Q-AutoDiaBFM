import ast 
import re


class IncorrectNumberOfSamples():
    def _checkAllSubscripts(self, code_ast):
        index_access = []
        for node in code_ast:
            if isinstance(node, ast.Subscript):
                index_access.append(node.slice)
        print(index_access)
        return index_access

    def _checkIndexAccess(self, codeDiff, astSample):

        buggy, patched = codeDiff[0], codeDiff[1]
        buggyList = list(filter(("").__ne__, buggy.split("\n")))
        patchedList = list(filter(("").__ne__, patched.split("\n")))

        buggyAST, patchedAST = ast.walk(astSample[0]), ast.walk(astSample[1])    

        buggy_index_access, patched_index_access = self._checkAllSubscripts(buggyAST), self._checkAllSubscripts(patchedAST)

        if len(buggy_index_access) != len(patched_index_access):
            return True
        else:
            for iter_ in range(0, len(buggy_index_access)):
                print(buggy_index_access[iter_].__dict__, patched_index_access[iter_].__dict__)
                if type(buggy_index_access[iter_]) != type(patched_index_access[iter_]):
                    return True
                elif buggy_index_access[iter_].__dict__ != patched_index_access[iter_].__dict__:
                    return True

        return False

    def _detectIncorrectNumberOfSamples(self, codeDiff, astSample):
        status = False
        bugTypeMessage = "Incorrect Number Of Samples detected."
        try:
            status = self._checkIndexAccess(codeDiff, astSample)
            print("checkIndex WORKS")
        except:
            status = False
            print("error in checkIndex")
            raise

        return status, bugTypeMessage

    def assessBugType(self, codeSample, astSample):
        return self._detectIncorrectNumberOfSamples(codeSample, astSample)