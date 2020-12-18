#!/usr/bin/env python
import sys
import parse

def invalid_ticket_nums(rules, ticket):
    '''Returns a list of ticket numbers that don't match any rules'''
    return [v for v in ticket if not valid_number_any(rules, v)]

def valid_number_any(rules, value):
    '''Checks if a ticket number matches any rule'''
    return any(rule_matches(rule, value) for rule in rules)

def rule_matches(rule, value):
    '''Checks if a ticket number matches the given rule'''
    return any(start <= value <= end for start,end in rule)

def find_matching_rules(rules, values):
    '''Returns all rules (their indexes) that match all of given ticket numbers'''
    candidates = set()
    for i,rule in enumerate(rules):
        matches = [rule_matches(rule, value) for value in values]
        if all(matches):
            candidates.add(i)
    return candidates

grp_rules, grp_ticket, grp_nearby = sys.stdin.read().split('\n\n')

rules = []
for line in grp_rules.split('\n'):
    name, start1, end1, start2, end2 = parse.parse('{}: {:d}-{:d} or {:d}-{:d}', line)
    rules.append(((start1, end1), (start2, end2)))

tickets = [list(map(int, line.strip().split(','))) for line in grp_nearby.strip().split('\n')[1:]]

# part 1 - find sum of all invalid ticket numbers
badsum = 0
valid = []
for ticket in tickets:
    if invalid := invalid_ticket_nums(rules, ticket):
        badsum += sum(invalid)
    else:
        valid.append(ticket)

print('part1:', badsum)
assert badsum == 25895

# part 2
# regroup ticket numbers by column
column_vals = list(zip(*valid))

# identify all potentially valid rules for each column.
# sort columns by increasing number of rules so that those with the fewest options are checked first.
rule_candidates = {idx: find_matching_rules(rules,vals) for idx,vals in enumerate(column_vals)}
rule_candidates = sorted(rule_candidates.items(), key=lambda item: len(item[1]))

# split columns and rulesets into parallel lists.
columns, rulesets = zip(*rule_candidates)

def assign_rules(rulesets, rule_columns, colidx=0):
    '''
    Assign rules to columns until all are valid.

    rulesets:     list of rule candidates for each column index (indexed with colidx)
    rule_columns: final dict mapping each rule to its assigned column index
    colidx:       current index of 'columns' (not the actual column number. columns[colidx] contains that)
    '''
    if colidx >= len(rulesets):
        return True

    # only consider unused rules for this column
    rules = rulesets[colidx] - rule_columns.keys()
    for rule in rules:
        rule_columns[rule] = colidx
        if assign_rules(rulesets, rule_columns, colidx + 1):
            return True
        del rule_columns[rule]
    return False

final_rules = {}
assert assign_rules(rulesets, final_rules)

myticket = list(map(int, grp_ticket.split('\n')[1].split(',')))

prod = 1
for rulenum in range(6):           # only check the initial six 'departure' rules
    colidx = final_rules[rulenum]  # get sorted columns index associated with the rule
    column = columns[colidx]       # find actual column position with the sorted columns index
    prod *= myticket[column]       # get the ticket number at that position

print('part2:', prod)
assert prod == 5865723727753
