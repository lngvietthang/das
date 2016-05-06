import os

def getContentAndHighlight(path2File):
    '''
    Get content and highlights from a story in the file
    :param path2File: path to file
    :return: a tuple (content, highlights)
    '''

    content = []
    highlights = []
    lines = []
    #TODO: read file
    with open(path2File) as fread:
        for line in fread:
            line = line.strip()
            if line != '':
                lines.append(line)
    #TODO: get content and highlights
    isHighlight = False
    for line in lines:
        if line == '@highlight':
            isHighlight = True
            continue
        if isHighlight:
            highlights.append(line)
            isHighlight = False
        else:
            content.append(line)

    return (content, highlights)

def loadData(path2Dir):
    '''
    Load all stories in the directory
    :param path2Dir: path to directory
    :return: a list of tuple (filename, content, highlights)
    '''

    # TODO: Get list files in directory
    lstFiles = [filename for filename in os.listdir(path2Dir) if os.path.isfile(os.path.join(path2Dir, filename))]
    # TODO: Get content and highlights from a file
    data = []
    for filename in lstFiles:
        content, highlights = getContentAndHighlight(os.path.join(path2Dir, filename))
        data.append((filename, content, highlights))

    return data

def saveData(dataset, path2OutDir, extension):
    '''
    Save dataset in the directory. One tuple (content, highlights) to one file following the format:
    Content
    @highlight
    hightlight 1
    ...
    :param dataset: A list of tuple (filename, content, highlights)
    :param path2OutDir: Path to the output directory.
    :param extension: Extension of the file
    :return: None
    '''
    for filename, content, highlights in dataset:
        with open(os.path.join(path2OutDir, filename + '.' + extension), 'w') as fwrite:
            fwrite.write('\n'.join([line for line in content]))
            fwrite.write('\n')
            fwrite.write('\n'.join(['@highlight\n' + line for line in highlights]))
            fwrite.flush()

def loadRule(path2File):
    '''
    Load rule
    :param path2File: path to file has rules (a can be change to b)
    :return: list of rule (a, b)
    '''
    with open(path2File) as fread:
        lines = [line.strip() for line in fread]
    rules = []
    for line in lines:
        a, b = line.split()
        rules.append((a, b))

    return rules

def merge2Dict(dict1, dict2):
    '''
    Merge 2 dictionary, if dict1 and dict2 have same key then final value = dict1.value + dict2.value
    :param dict1: Dictionary 1
    :param dict2: Dictionay 2
    :return: dict
    '''
    result = dict1
    for key, value in dict2.items():
        if result.has_key(key):
            result[key] += value
        else:
            result[key] = value

    return result