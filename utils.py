import re

def parse_adb_row(row):
    msg = {}
    keys_positions = [(m.group(1), m.end()) 
                      for m in re.finditer(r'\b(\w+)=', row)]
    
    for i, (key, end) in enumerate(keys_positions):
        if i + 1 < len(keys_positions):
            value = row[end:keys_positions[i+1][1]].strip().rstrip(',').strip()
        else:
            value = row[end:].strip()
        msg[key] = value
    
    return msg
