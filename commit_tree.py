from Objects.commit import Commit

def commit_tree(tree_sha, message, parent_sha=None):
  commit = Commit()
  commit.setCommit(tree_sha, message, parent_sha)