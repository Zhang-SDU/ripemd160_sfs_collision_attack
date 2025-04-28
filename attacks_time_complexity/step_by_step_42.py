# all uncontrolled conditions

# 1. Traverse X11, solve m7 and verify LQ15: [1, 0.093]
# 2. Solve X10, verify X10 and LQ14: [1, 1.508]
# 3. Solve X9 and verify LQ13: [1, 0.093]
# 4. Solve X8 and verify LQ12: [1, 0.001]
# 5. Solve X41 and verify LQ41: [1, 0.090]
# 6. Solve Y13, verify Y13: [27, 1]
# 7. Solve Y14, verify Y14: [1, 1]
# 8. Solve Y15, verify Y15 and RQ15: [1, 1.001]
# 9. Solve Y17, verify Y16 and Y17: [2, 2]
# 10. Solve Y18, verify Y18: [1, 1]
# 11. Solve Y19, verify Y19: [1, 1]
# 12. Solve Y21, verify Y20、Y21: [2, 3]
# 13. Solve Y22, verify Y22: [1, 2]
# 14. Solve Y23, verify Y23: [1, 2]
# 15. Solve Y25, verify Y2 and Y25: [2, 5]
# 16. Solve Y26, verify Y26: [1, 3]
# 17. Solve Y27, verify Y27 and RQ27: [1, 3.001]
# 18. Solve Y29, verify Y28 and Y29: [2, 4]
# 19. Solve Y37, verify \delta Y37 and (\delta X38 <<< 10) + (\delta Y37 <<< 10) = 0: [8, 8.146]
# 20. Solve Y38, verify \delta Y38 and (\delta X39 <<< 10) + (\delta Y38 <<< 10) = 0: [1, 3.917 + 0.003]
# 21. Solve Y39, verify \delta Y39 and \delta X40 + (\delta Y39 <<< 10) = 0: [1, 5.703 + 0.046]
# 22. Solve Y40, verify \delta Y40: [1, 4.415]
# 23. Solve Y41, verify \delta Y41: [1, 3.817]



from itertools import combinations
from math import log

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
p1 = 13.936
r = 41

# the second stage 
forward = [[1, 0.090]]

backward = [[1, 1.508], [1, 0.093], [1, 0.001], [27, 1], [1, 1], [1, 1.001], [2, 2], [1, 1], [1, 1], [2, 3], [1, 2], [1, 2], [2, 5], [1, 3], [1, 3.001], [2, 4], [8, 8.146], [1, 3.920], [1, 5.749], [1, 4.415], [1, 3.817]]

permutations = generate_insert_permutations(forward, backward)

total_pro = 56.834
complexity = []
for i in range(len(permutations)):
    current_list = [[1, 0.093]]
    current_list = current_list + permutations[i]
    total_pro = 56.834
    complexity_temp = 0
    for j in range(len(current_list)):
        complexity_temp += (current_list[j][0] / 2 / (r + 1)) * pow(2, total_pro)
        total_pro = total_pro - current_list[j][1]
    complexity.append(complexity_temp)

min_complexity = min(complexity)
index_min = complexity.index(min_complexity)

print("Best verification order: ")
print(permutations[index_min])


# the first stage
# 1. Solve X12, verify X12 and LQ18: [1, 5]
# 2. Solve m1, m1, X39, X40, verify X39, LQ39, X40 and Y40: [4, 8.936]

print()
print("first complexity: ",  log(pow(2, 56.834-(32-n1)) * (1/2/(r+1) * pow(2, p1) + 4/2/(r+1) * pow(2, p1-5)), 2))
print("second complexity: ", log(min_complexity, 2))
print("total complexity: ", log(pow(2, 56.834-(32-n1)) * (1/2/(r+1) * pow(2, p1) + 4/2/(r+1) * pow(2, p1-5)) + min_complexity, 2))