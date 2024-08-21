from gsrc import read_gsrc

base = 'data/gsrc'
mode = 'SOFT'
name = 'n10'

data = read_gsrc(base,name,mode)

for block_id, block_data in data.items():
    print(f"Block ID: {block_id}")
    print("Block Data:")
    for key, value in block_data.items():
        print(f"  {key}: {value}")
    print()