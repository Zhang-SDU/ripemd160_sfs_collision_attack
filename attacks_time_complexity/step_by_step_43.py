# all uncontrolled conditions

# 1. Traverse X11, solve m7 and verify LQ15: [1, 0.093]
# 2. solve X41, verify X41 and LQ41: [1, 3.106]
# 3. solve X10, verify X10 and LQ14: [1, 1.508]
# 4. solve X42, verify LQ42: [1, 0.196]  
# 5. solve X9, verify LQ13: [1, 0.093]
# 6. solve X8, verify LQ12: [1, 0.001]
# 7. solve Y13, verify Y13: [27, 1]
# 8. solve Y14, verify Y14: [1, 1]
# 9. solve Y15, verify Y15 and RQ15: [1, 1.001]
# 10. solve Y17, verify Y16 and Y17: [2, 2]
# 11. solve Y18, verify Y18: [1, 1]
# 12. solve Y19, verify Y19: [1, 1]
# 13. solve Y21, verify Y20 and Y21: [2, 3]
# 14. solve Y22, verify Y22: [1, 2]
# 15. solve Y23, verify Y23: [1, 2]
# 16. solve Y25, verify Y24 and Y25: [2, 5]
# 17. solve Y26, verify Y26: [1, 3]
# 18. solve Y27, verify Y27 and RQ27: [1, 3.001]
# 19. solve Y29, verify Y28 and Y29: [2, 4]
# 20. solve Y30, verify Y30: [1, 1]
# 21. solve Y31, verify Y31: [1, 1] 
# 22. solve Y33, verify Y32 and Y33: [2, 3.415]
# 23. solve Y38, verify \delta Y38 and (\delta X39 <<< 10) + (\delta Y38 <<< 10) = 0: [5, 5.716 + 0.003 = 5.719]
# 24. solve Y39, verify \delta Y39 and (\delta X40 <<< 10) + (\delta Y39 <<< 10) = 0: [1, 6.191 + 0.046 = 6.237]
# 25. solve Y40, verify \delta Y40 and \delta X41 + (\delta Y40 <<< 10) = 0: [1, 4.529 + 0.093 = 4.622]
# 26. solve Y41, verify \delta Y41: [1, 4.379]
# 27. solve Y42, verify \delta Y42: [1, 6.696]


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
p1 = 25.567
r = 42

forward = [[1, 3.106], [1, 0.196]]

backward = [[1, 1.508], [1, 0.093], [1, 0.001], [27, 1], [1, 1], [1, 1.001], [2, 2], [1, 1], [1, 1], [2, 3], [1, 2], [1, 2], [2, 5], [1, 3], [1, 3.001], [2, 4], [1, 1], [1, 1], [2, 3.415], [5, 5.719], [1, 6.237], [1, 4.622], [1, 4.379], [1, 6.696]]

permutations = generate_insert_permutations(forward, backward)

total_pro = 67.067
complexity = []
for i in range(len(permutations)):
    current_list = [[1, 0.093]]
    current_list = current_list + permutations[i]
    total_pro = 67.067
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
# solve X12, verify X12 and LQ18: [1, 5]
# solve m13, m1 and X39, verify X39 and LQ39: [3, 10 + 2.825]
# solve X40, verify X40 and LQ40: [1, 6 + 1.742]

print()
print("first complexity: ", log(pow(2, 67.067-(32-n1)) * ((1/2/(r+1)) * pow(2, p1) + (3/2/(r+1)) * pow(2, p1 - 5) + (1/2/(r+1)) * pow(2, p1 - 5 - 10 - 2.825)), 2))
print("second complexity: ", log(min_complexity, 2))
print("total complexity: ", log(pow(2, 67.067-(32-n1)) * ((1/2/(r+1)) * pow(2, p1) + (3/2/(r+1)) * pow(2, p1 - 5) + (1/2/(r+1)) * pow(2, p1 - 5 - 10 - 2.825)) + min_complexity, 2))