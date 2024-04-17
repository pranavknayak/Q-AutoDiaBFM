import os
from git import Repo

repo = Repo('./test_repo/')
commit_counts = 0
for commit in repo.iter_commits():

