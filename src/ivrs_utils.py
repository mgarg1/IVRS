import psutil

def killtree(pid, including_parent=True):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        print ("child", child)
        child.kill()

    if including_parent:
        parent.kill()
