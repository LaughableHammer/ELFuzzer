def init():
    global filetype
    global corpus
    global status
    
    filetype = ''
    corpus = []
    
    status = {
        "executions": 0,
        "completion": 0,
        "last_input": "",
        "coverage": "TODO!!! :c"
    }