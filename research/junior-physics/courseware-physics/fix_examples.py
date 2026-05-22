import re
import sys

def fix_example_numbers(filepath):
    with open(filepath) as f:
        content = f.read()
    
    # Global sequential replacement of "例题 N"
    counter = [1]
    
    def replacer(match):
        num = counter[0]
        counter[0] += 1
        return f'例题 {num}'
    
    # Use regex to replace all "例题 N" (with possible whitespace variations)
    final = re.sub(r'例题\s+N', replacer, content)
    
    remaining = final.count('例题 N')
    print(f'{filepath}: 例题 N remaining: {remaining}')
    
    with open(filepath, 'w') as f:
        f.write(final)
    print(f'{filepath}: saved')

if __name__ == '__main__':
    fix_example_numbers(sys.argv[1])
