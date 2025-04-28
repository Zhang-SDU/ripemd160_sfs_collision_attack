# 1. generate initial starting point: search by SAT/SMT tool
# 2. generate sufficient starting points:
    # 1. Traverse X16, modify m6, calculat X15: 2^31 X16 ===> generate 2^31 starting points: [1, 0]
    # 2. Traverse m0, modify X20, X19, X18, X17, probability is 2^-5 ===> generate 2^27 starting points: [4, 5]
    # 3. Traverse X21, modify m9, verify LQ25: 2^31 X21 ===> generate 2^31 starting points: [1, 0]
    # 1. X15 = Y15: [1, p = 1]
    # 2. X14 = Y14 and X13 = Y13: 4 steps of step function + table lookup(2^-2.1)
    # 3. X12 = Y12: [1, p = 1]
# 3. verify uncontrolled probability
    # 1. solve X11, Y11, verify X11 = Y11, [2, 2^-32]                      [2, 32]
    # 2. solve X59, verify \delta X59 = 0, [25, 2^-9.542]                  [25, 9.542]
    # 3. solve X60, verify \delta X60 = 0, [1, 2^-1.222]                   [1, 1.222]
    # 4. solve X61, verify \delta X61 = 0, [1, 2^1.099]                    [1, 1.099]
    # 5. solve X62, verify \delta X62 = 0x80000000, [1, 2^0.094]           [1, 0.094]
    # 6. solve X63, verify \delta X63 = 0, [1, 2^0.998]                    [1, 0.998]
    # 7. solve Y28, verify Y28 and RQ28, [1, 10 + 0.153]                    [1, 10.153]
    # 8. solve Y29, verify Y29 and RQ29, [1, 6 + 1.179]                     [1, 7.179]
    # 9. solve Y30, Y31, Y32, Y33, verify Y30, Y31, Y32, Y33, and RQ30, [4, 8 + 1.66 + 0.453 + 0.095 + 0.093 + 0.001]    [4, 10.302]
    # 10. solve Y34, verify RQ34, [1, 0.001]
    # 11. solve Y59, Y60, verify Y59 and Y60, [26, 1]
    # 12. solve Y61, verify Y61 and RQ61, [1, 1.001]
    # 13. solve Y62, verify Y62, [1, 1]
    # 14. Y63 has no condition


from typing import List
from math import log

def generate_insert_permutations_3(list1: List, list2: List, list3: List) -> List[List]:
    result = []

    def backtrack(i, j, k, path):
        if i == len(list1) and j == len(list2) and k == len(list3):
            result.append(path[:])
            return
        if i < len(list1):
            path.append(list1[i])
            backtrack(i + 1, j, k, path)
            path.pop()
        if j < len(list2):
            path.append(list2[j])
            backtrack(i, j + 1, k, path)
            path.pop()
        if k < len(list3):
            path.append(list3[k])
            backtrack(i, j, k + 1, path)
            path.pop()

    backtrack(0, 0, 0, [])
    return result



r = 47


# the second stage 
A = [[2,32]]
B = [[25, 9.542], [1, 1.222], [1, 1.099], [1, 0.094], [1, 0.998]]
C = [[1, 10.153], [1, 7.179], [4, 10.302], [1, 0.001], [26, 1], [1, 1.001], [1, 1]]


permutations = generate_insert_permutations_3(A, B, C)

total_pro = 75.591
complexity = []
for i in range(len(permutations)):
    current_list = []
    current_list = current_list + permutations[i]
    total_pro = 75.591
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
complexity1 = pow(2, 75.591) * (2 / 2 / 48)  + pow(2, 75.591 - 31) * (4/2/48) * pow(2, 5) + pow(2, 75.591 - 31 - 27) * (1/2/48)
complexity2 = pow(2, 75.591) * (1/ 2 / 48) + pow(2, 75.591) * ((4/2/48) + pow(2,-2.1)) + pow(2, 75.591) * (1/2/48)

print()
print("first complexity: ", log(complexity1 + complexity2, 2))
print("second complexity: ", log(min_complexity, 2))

print("total complexity: ", log(pow(2,73) + complexity1 + complexity2 + min(complexity), 2))
