# all uncontrolled conditions

# 1. Traverse X11, solve m7 and verify LQ15: [1, 0.093]
# 2. Solve X10, verify X10 and LQ14: [1, 1.508]
# 3. Solve X9 and verify LQ13: [1, 0.093]
# 4. Solve X8 and verify LQ12: [1, 0.001]
# 5. Solve Y13 and verify Y13: [27, 1]
# 6. Solve Y14 and verify Y14: [1, 1]
# 7. Solve Y15, verify Y15 and RQ15: [1, 1.001]
# 8. Solve Y17, verify Y16 and Y17: [2, 2]
# 9. Solve Y18 and verify Y18: [1, 1]
# 10. Solve Y19 and verify Y19: [1, 1]
# 11. Solve Y21, verify Y20 and Y21: [2, 3]
# 12. Solve Y22 and verify Y22: [1, 2]
# 13. Solve Y23 and verify Y23: [1, 2]
# 14. Solve Y25, verify Y24 and Y25: [2, 5]
# 15. Solve Y26 and verify Y26: [1, 3]
# 16. Solve Y36 and verify \delta Y36、(\delta X37 <<< 10) + (\delta Y36 <<< 10) = 0: [10, 14.397]
# 17. Solve Y37 and verify \delta Y37、(\delta X38 <<< 10) + (\delta Y37 <<< 10) = 0: [1, 2.373]
# 28. Solve Y38 and verify \delta Y38、\delta X39 + (\delta Y38 <<< 10) = 0: [1, 2.938 + 0.003 = 2.941]
# 19. Solve Y39 and verify \delta Y39: [1, 4.937]
# 20. Solve Y40 and verify \delta Y40: [1, 4.290]


from itertools import combinations
from math import log


# generate all orders
def generate_insert_permutations(list1, list2):
    positions = list(combinations(range(len(list1) + len(list2)), len(list1)))
    result = []
    
    for pos in positions:
        merged = []
        it1, it2 = iter(list1), iter(list2)
        for i in range(len(list1) + len(list2)):
            if i in pos:
                merged.append(next(it1))
            else:
                merged.append(next(it2))
        result.append(merged)
    
    return result


n1 = 3
p1 = 9.005
r = 40

# the second stage
forward = []

backward = [[1, 1.508], [1, 0.093], [1, 0.001], [27, 1], [1, 1], [1, 1.001], [2, 2], [1, 1], [1, 1], [2, 3], [1, 2], [1, 2], [2, 5], [1, 3], [10, 14.397], [1, 2.373], [1, 2.941], [1, 4.937], [1, 4.290]]

permutations = generate_insert_permutations(forward, backward)

total_pro = 52.634
complexity = []
for i in range(len(permutations)):
    current_list = [[1, 0.093]]
    current_list = current_list + permutations[i]
    total_pro = 52.634
    complexity_temp = 0
    for j in range(len(current_list)):
        complexity_temp += (current_list[j][0] / 2 / (r + 1)) * pow(2, total_pro)
        total_pro = total_pro - current_list[j][1]
    complexity.append(complexity_temp)


min_complexity_second = min(complexity)
index_min = complexity.index(min_complexity_second)

print("Best verification order: ")
print(permutations[index_min])


# the first stage
# 1. solve X12, verify X12 and LQ18: [1, 5]
# 2. solve m13、m1 and X39, verify X39 and LQ39: [3, 3 + 0.912]
# 3. solve X40, verify LQ40: [1, 0.093]

print()
print("first complexity: ", log(pow(2, 52.634-(32-n1)) * ((1/2/(r+1)) * pow(2, p1) + (3/2/(r+1)) * pow(2, p1 - 5) + (1/2/(r+1)) * pow(2, p1 - 5 - 3 - 0.912)), 2))
print("second complexity: ", log(min_complexity_second, 2))
print("total complexity: ", log(pow(2, 52.634-(32-n1)) * ((1/2/(r+1)) * pow(2, p1) + (3/2/(r+1)) * pow(2, p1 - 5) + (1/2/(r+1)) * pow(2, p1 - 5 - 3 - 0.912)) + min_complexity_second, 2))