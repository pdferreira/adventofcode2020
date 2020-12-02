def parse_policy(input_line):
    (policy, _, password) = input_line.partition(': ')
    (prange, _, pletter) = policy.partition(' ')
    (a, _, b) = prange.partition('-')
    return (int(a), int(b), pletter, password)


def parse_file(input_file):
    with open(input_file) as f:
        return [parse_policy(line) for line in f.readlines()]
        
def validate_policy_part1(minOccur, maxOccur, letter, password):
    return minOccur <= password.count(letter) <= maxOccur

def validate_policy_part2(fstPos, sndPos, letter, password):
    fstMatches = password[fstPos - 1] == letter
    sndMatches = password[sndPos - 1] == letter
    return fstMatches != sndMatches

def solve(password_policies, validation_fn):
    return [
        validation_fn(a, b, letter, password)
        for (a, b, letter, password)
        in password_policies].count(True)
  
if __name__ == '__main__':
    pwd_policies = parse_file('input.txt')
    print('Part 1 answer:', solve(pwd_policies, validate_policy_part1))
    print('Part 2 answer:', solve(pwd_policies, validate_policy_part2))