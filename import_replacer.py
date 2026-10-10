import os

from file_walker import ImportToReplace


def replace(original_file_contents: str, imports_to_replace: list[ImportToReplace]) -> str:
    """imports_to_replace should be a list of all transitive dependencies. inlines all dependencies and removes their includes"""
    output = [
        
    ]

    replace_dict: dict[str, ImportToReplace] = {}

    for v in imports_to_replace:
        replace_dict[v.entire_line] = v
    
    for v in imports_to_replace:
        import_file_contents = open(os.path.join(v.resolved_path)).read()
        for line in import_file_contents.splitlines():
            if line not in replace_dict:
                output.append(line)

    for line in original_file_contents.splitlines():
        if line not in replace_dict:
            output.append(line)
    
    return "\n".join(output)