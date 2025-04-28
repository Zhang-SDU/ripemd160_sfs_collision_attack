import subprocess
import time
import os
from constrain_condition import *


def handle(s):
    temp = s.replace("0b", "").split(" = ")
    index = temp[0].split("_")
    return index, temp[1]

def get_dc(data_list, var_str, step):
    result = []
    data = data_list.replace("ASSERT( ", "").replace(" );", "").replace("\nInvalid.", "").split("\n")

    xv = [] 
    xd = []
    x = []

    for i in range(step):
        temp_v = []
        temp_d = []
        temp = []
        for j in range(32):
            temp_v.append(0)
            temp_d.append(0)
            temp.append(0)
        xv.append(temp_v)
        xd.append(temp_d)
        x.append(temp)

    for i in data:
        if var_str + "v" in i:
            index, value = handle(i)
            xv[int(index[1])][int(index[2])] = value
        elif var_str + "d" in i:
            index, value = handle(i)
            xd[int(index[1])][int(index[2])] = value
    for i in range(len(xv)):
        for j in range(32):
            if xv[i][j] == "1" and xd[i][j] == "1":
                x[i][j] = "u"
            elif xv[i][j] == "0" and xd[i][j] == "0":
                x[i][j] = "0"
            elif xv[i][j] != xd[i][j]:
                x[i][j] = "n"

    for i in range(len(x)):
        temp = "%s\"" % str(i - 5).zfill(2)
        for j in range(32 - 1, -1, -1):
            if x[i][j] == "0":
                temp += "="
            elif x[i][j] == "u":
                temp += "u"
            elif x[i][j] == "n":
                temp += "n"
        temp += "\","
        result.append(temp)
    return result

def read_differential_characteristic(result_file, step):
    result = []
    print(result_file)
    data_list = open(result_file, "r").read()
    variable_list = ["x"]
    for var in variable_list:
        result.append(get_dc(data_list, var, step))
        result.append("")
    return result

class FunctionModel:
    def __init__(self, steps, bounds):
        self.__bounds_rounds = bounds
        self.__step = steps
        # save variables
        self.__declare = []
        # save constraint statements
        self.__constraints = []
        # save assignment constraints
        self.__assign = []  
        self.__RotateCons_right = ["-", "-", "-", "-", "-", 
                                8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
                                9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
                                9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
                                15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
                                8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
        
        self.__OrderMessageWords_right = ["-", "-", "-", "-", "-", 
                                5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
                                6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
                                15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
                                8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
                                12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]

        self.__isc = ["-", "-", "-", "-", "-", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        
        self.__isf = ["-", "-", "-", "-", "-", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        self.__isv = ["-", "-", "-", "-", "-", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        
        self.__isk = ["-", "-", "-", "-", "-", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.__boolFunction_right = ["ONX", "IFZ", "ONZ", "IFX", "XOR"]

    def save_variable(self, s):
        temp = s + ": BITVECTOR(1);\n"
        if temp not in self.__declare:
            self.__declare.append(temp)
        return s

    def create_constraints(self, X, propagation_trail):
        fun = []
        for maxterm in propagation_trail:
            temp = []
            for i in range(len(maxterm)):
                if maxterm[i] == '1':
                    temp.append('(' + '~' + X[i] + ')')
                elif maxterm[i] == '0':
                    temp.append(X[i])
            fun.append('(' + "|".join(temp) + ')')
        sbox_main = 'ASSERT ' + '&'.join(fun) + '=0bin1' + ';\n'
        return sbox_main

    def left_shift(self, order, num):
        return order[-num:] + order[:-num]
    
    def right_shift(self, order, num):
        return order[num:] + order[:num]

    def addexp_model(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, out_var_v, out_var_d, step):

        eqn = "% ADDEXP_MODEL\n"
        eqn += "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (self.save_variable("cv6" + "_" + str(step) + "_" + str(0)),
                                                             self.save_variable("cd6" + "_" + str(step) + "_" + str(0)))
        for i in range(32):
            temp = [self.save_variable(in_var_v_0[i]), self.save_variable(in_var_d_0[i]),
                    self.save_variable(in_var_v_1[i]), self.save_variable(in_var_d_1[i]),
                    self.save_variable("cv6" + "_" + str(step) + "_" + str(i)),
                    self.save_variable("cd6" + "_" + str(step) + "_" + str(i)),
                    self.save_variable(out_var_v[i]), self.save_variable(out_var_d[i]),
                    self.save_variable("cv6" + "_" + str(step) + "_" + str(i + 1)),
                    self.save_variable("cd6" + "_" + str(step) + "_" + str(i + 1))]
            eqn += self.create_constraints(temp, addexp_model_constrain)
        self.__constraints.append(eqn)


    def boolConditionNumber_model_XOR(self, fna, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v,
                       out_var_d, in_var_d_bitconditionNumber):
        
        eqn = "% boolConditionNumber_model " + str(fna) + "\n"
        for i in range(32):
            temp = [self.save_variable(in_var_v_0[i]),
                    self.save_variable(in_var_d_0[i]),
                    self.save_variable(in_var_v_1[i]),
                    self.save_variable(in_var_d_1[i]),
                    self.save_variable(in_var_v_2[i]),
                    self.save_variable(in_var_d_2[i]),
                    self.save_variable(out_var_v[i]),
                    self.save_variable(out_var_d[i]),
                    self.save_variable(in_var_d_bitconditionNumber[i])]
            eqn += self.create_constraints(temp, xor_condition_number_contsrain)
        self.__constraints.append(eqn)


    def boolConditionNumber_model(self, fna, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v,
                       out_var_d, in_var_v_bitconditionNumber, in_var_d_bitconditionNumber):

        if fna == "ONX":
            eqn = "% boolConditionNumber_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_v_bitconditionNumber[i]),
                        self.save_variable(in_var_d_bitconditionNumber[i])]
                eqn += self.create_constraints(temp, onx_condition_number_contsrain)
            self.__constraints.append(eqn)
        elif fna == "IFZ":
            eqn = "% boolConditionNumber_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_v_bitconditionNumber[i]),
                        self.save_variable(in_var_d_bitconditionNumber[i])]
                eqn += self.create_constraints(temp, ifz_condition_number_contsrain)
            self.__constraints.append(eqn)
        elif fna == "IFX":
            eqn = "% boolConditionNumber_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_v_bitconditionNumber[i]),
                        self.save_variable(in_var_d_bitconditionNumber[i])]
                eqn += self.create_constraints(temp, ifz_condition_number_contsrain)
            self.__constraints.append(eqn)

        elif fna == "ONZ":
            eqn = "% boolConditionNumber_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_v_bitconditionNumber[i]),
                        self.save_variable(in_var_d_bitconditionNumber[i])]
                eqn += self.create_constraints(temp, onx_condition_number_contsrain)
            self.__constraints.append(eqn)

    def boolFull_model(self, fna, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v,
                       out_var_d, in_var_0, in_var_1, in_var_2):
        if fna == "ONX":
            eqn = "% boolFull_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_0[i]),
                        self.save_variable(in_var_1[i]),
                        self.save_variable(in_var_2[i])]
                eqn += self.create_constraints(temp, onx_full_constrain)
            self.__constraints.append(eqn)
        elif fna == "XOR":
            eqn = "% boolFull_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_0[i]),
                        self.save_variable(in_var_1[i]),
                        self.save_variable(in_var_2[i])]
                eqn += self.create_constraints(temp, xor_full_constrain)
            self.__constraints.append(eqn)

        elif fna == "IFZ":
            eqn = "% boolFull_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_0[i]),
                        self.save_variable(in_var_1[i]),
                        self.save_variable(in_var_2[i])]
                eqn += self.create_constraints(temp, ifz_full_constrain)
            self.__constraints.append(eqn)
        elif fna == "IFX":
            eqn = "% boolFull_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_1[i]),
                        self.save_variable(in_var_2[i]),
                        self.save_variable(in_var_0[i])]
                eqn += self.create_constraints(temp, ifz_full_constrain)
            self.__constraints.append(eqn)

        elif fna == "ONZ":
            eqn = "% boolFull_model " + str(fna) + "\n"
            for i in range(32):
                temp = [self.save_variable(in_var_v_2[i]),
                        self.save_variable(in_var_d_2[i]),
                        self.save_variable(in_var_v_0[i]),
                        self.save_variable(in_var_d_0[i]),
                        self.save_variable(in_var_v_1[i]),
                        self.save_variable(in_var_d_1[i]),
                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_2[i]),
                        self.save_variable(in_var_0[i]),
                        self.save_variable(in_var_1[i])]
                eqn += self.create_constraints(temp, onx_full_constrain)
            self.__constraints.append(eqn)


    def boolean_value(self, fna, x0, x1, x2, out):
        eqn = ""
        if fna == "ONZ":
            for i in range(32):
                temp = [self.save_variable(x0[i]), 
                        self.save_variable(x1[i]), 
                        self.save_variable(x2[i]), 
                        self.save_variable(out[i])]
                eqn += self.create_constraints(temp, onz_value_constrain)
            self.__constraints.append(eqn)
        elif fna == "XOR":
            for i in range(32):
                temp = [self.save_variable(x0[i]), 
                        self.save_variable(x1[i]), 
                        self.save_variable(x2[i]), 
                        self.save_variable(out[i])]
                eqn += self.create_constraints(temp, xor_value_constrain)
            self.__constraints.append(eqn)
        elif fna == "IFX":
            for i in range(32):
                temp = [self.save_variable(x0[i]), 
                        self.save_variable(x1[i]), 
                        self.save_variable(x2[i]), 
                        self.save_variable(out[i])]
                eqn += self.create_constraints(temp, ifx_value_constrain)
            self.__constraints.append(eqn)


    def computer_q(self, in_var_v_z, in_var_d_z, in_var_v_x, in_var_d_x, in_var_z, in_var_x, in_var_q, step):
        for i in range(32):
            self.derive_cond(in_var_x[i], in_var_v_x[i], in_var_d_x[i])
            self.derive_cond(in_var_z[i], in_var_v_z[i], in_var_d_z[i])
        self.val_add_model(in_var_x, in_var_q, in_var_z, 32, step)

    def derive_cond(self, in_var_x, in_var_v_x, in_var_d_x):
        temp = [in_var_x, in_var_v_x, in_var_d_x]
        eqn = self.create_constraints(temp, derive_cond_constrain)
        self.__constraints.append(eqn)

    def expand_model(self, in_var_v, in_var_d, out_var_v, out_var_d, isK, step):
        eqn = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (self.save_variable("cv7" + "_" + str(step) + "_" + str(0)),
                                                            self.save_variable("cd7" + "_" + str(step) + "_" + str(0)))
        if isK == 1:
            for i in range(32):
                temp = [self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable(in_var_v[i]),
                        self.save_variable(in_var_d[i]),
                        "cv7" + "_" + str(step) + "_" + str(i),
                        "cd7" + "_" + str(step) + "_" + str(i),
                        self.save_variable("cv7" + "_" + str(step) + "_" + str(i + 1)),
                        self.save_variable("cd7" + "_" + str(step) + "_" + str(i + 1))]
                eqn += self.create_constraints(temp, expand_model_contsrain_2)
            self.__constraints.append(eqn)
        else:
            for i in range(32):
                temp = [self.save_variable(in_var_v[i]),
                        self.save_variable(in_var_d[i]),
                        self.save_variable("cv7" + "_" + str(step) + "_" + str(i)),
                        self.save_variable("cd7" + "_" + str(step) + "_" + str(i)),

                        self.save_variable(out_var_v[i]),
                        self.save_variable(out_var_d[i]),
                        self.save_variable("cv7" + "_" + str(step) + "_" + str(i + 1)),
                        self.save_variable("cd7" + "_" + str(step) + "_" + str(i + 1))]
                eqn += self.create_constraints(temp, expand_model_contsrain_1)
            self.__constraints.append(eqn)

    def modadd_model(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_c_v, in_var_c_d, out_var_v,
                     out_var_d):
        eqn = ""
        for i in range(32):
            temp = [self.save_variable(in_var_v_0[i]),
                    self.save_variable(in_var_d_0[i]),
                    self.save_variable(in_var_v_1[i]),
                    self.save_variable(in_var_d_1[i]),
                    self.save_variable(in_var_c_v[i]),
                    self.save_variable(in_var_c_d[i]),
                    self.save_variable(out_var_v[i]),
                    self.save_variable(out_var_d[i]),
                    self.save_variable(in_var_c_v[i + 1]),
                    self.save_variable(in_var_c_d[i + 1])]
            eqn += self.create_constraints(temp, modadd_model_constrain)
        self.__constraints.append(eqn)

    def rotate_model(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, out_var_v_0, out_var_d_0, out_var_v_1,
                     out_var_d_1, c_var_v_0, c_var_d_0):
        temp = [self.save_variable(in_var_v_0),
                self.save_variable(in_var_d_0),
                self.save_variable(in_var_v_1),
                self.save_variable(in_var_d_1),
                self.save_variable(out_var_v_0),
                self.save_variable(out_var_d_0),
                self.save_variable(out_var_v_1),
                self.save_variable(out_var_d_1),
                self.save_variable(c_var_v_0),
                self.save_variable(c_var_d_0)]
        eqn = self.create_constraints(temp, rotate_model_constrain)
        self.__constraints.append(eqn)

    def signed_q_model(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v,
                       out_var_d, s):
        eqn = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (in_var_v_2[0], in_var_d_2[0])

        temp = [self.save_variable(in_var_v_0[0]),
                self.save_variable(in_var_d_0[0]),

                self.save_variable(in_var_v_1[0]),
                self.save_variable(in_var_d_1[0]),

                self.save_variable(in_var_v_2[0]),
                self.save_variable(in_var_d_2[0]),

                self.save_variable(out_var_v[0]),
                self.save_variable(out_var_d[0]),

                self.save_variable(in_var_v_2[1]),
                self.save_variable(in_var_d_2[1])]
        eqn += self.create_constraints(temp, modadd_model_constrain)
        for i in range(1, s + 1):
            temp = [self.save_variable(in_var_v_0[i]),
                    self.save_variable(in_var_d_0[i]),
                    self.save_variable("temp_v" + "_" + str(i)),
                    self.save_variable("temp_d" + "_" + str(i)),

                    self.save_variable(in_var_v_2[i]),
                    self.save_variable(in_var_d_2[i]),

                    self.save_variable(out_var_v[i]),
                    self.save_variable(out_var_d[i]),

                    self.save_variable(in_var_v_2[i + 1]),
                    self.save_variable(in_var_d_2[i + 1])]
            eqn += self.create_constraints(temp, modadd_model_constrain)
            eqn += "ASSERT temp_v" + "_" + str(i) + " = 0bin0;\n"
            eqn += "ASSERT temp_d" + "_" + str(i) + " = 0bin0;\n"
        self.__constraints.append(eqn)

    def rotate_diff_first(self, s, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, out_var_v_0, out_var_d_0, in_var_v_2,
                          in_var_d_2, in_var_v_b4Outer, in_var_d_b4Outer, isV, isK, step):

        in_var_v_b4 = []
        in_var_d_b4 = []

        for i in range(32):
            in_var_v_b4.append("bv4" + "_" + str(step) + "_" + str(i))
            in_var_d_b4.append("bd4" + "_" + str(step) + "_" + str(i))

        in_var_v_b5 = []
        in_var_d_b5 = []
        for i in range(32):
            in_var_v_b5.append("bv5" + "_" + str(step) + "_" + str(i))
            in_var_d_b5.append("bd5" + "_" + str(step) + "_" + str(i))

        in_var_v_c0 = []
        in_var_d_c0 = []
        for i in range(33):
            in_var_v_c0.append("cv0" + "_" + str(step) + "_" + str(i))
            in_var_d_c0.append("cd0" + "_" + str(step) + "_" + str(i))

        "chv" + "_" + str(step)
        "chd" + "_" + str(step)
        # ∇b4[i + s mod 32] = ∇b3[i]
        for i in range(30 - s):
            eqn = "ASSERT %s = %s;\nASSERT %s = %s;\n" % (self.save_variable(in_var_v_b4[(i + s) % 32]),
                                                          self.save_variable(in_var_v_0[i]),
                                                          self.save_variable(in_var_d_b4[(i + s) % 32]),
                                                          self.save_variable(in_var_d_0[i]))
            self.__constraints.append(eqn)
        for i in range(32 - s, 30):
            eqn = "ASSERT %s = %s;\nASSERT %s = %s;\n" % (self.save_variable(in_var_v_b4[(i + s) % 32]),
                                                          self.save_variable(in_var_v_0[i]),
                                                          self.save_variable(in_var_d_b4[(i + s) % 32]),
                                                          self.save_variable(in_var_d_0[i]))
            self.__constraints.append(eqn)

        self.rotate_model(in_var_v_0[31 - s], in_var_d_0[31 - s],
                          in_var_v_0[30 - s], in_var_d_0[30 - s],
                          in_var_v_b4[31], in_var_d_b4[31],
                          in_var_v_b4[30], in_var_d_b4[30],
                          in_var_v_c0[0], in_var_d_c0[0])

        self.rotate_model(in_var_v_0[31], in_var_d_0[31],
                          in_var_v_0[30], in_var_d_0[30],
                          in_var_v_b4[(31 + s) % 32], in_var_d_b4[(31 + s) % 32],
                          in_var_v_b4[(30 + s) % 32], in_var_d_b4[(30 + s) % 32],
                          "chv" + "_" + str(step),
                          "chd" + "_" + str(step))
        self.modadd_model(in_var_v_1, in_var_d_1, in_var_v_b4, in_var_d_b4, in_var_v_c0, in_var_d_c0,
                          in_var_v_b5, in_var_d_b5)
        self.expand_model(in_var_v_b5, in_var_d_b5, out_var_v_0, out_var_d_0, isK, step)

        in_var_v_cOuter = []
        in_var_d_cOuter = []
        for i in range(33):
            in_var_v_cOuter.append("cvOuter" + "_" + str(step) + "_" + str(i))
            in_var_d_cOuter.append("cdOuter" + "_" + str(step) + "_" + str(i))

        self.signed_b4_model(in_var_v_b4, in_var_d_b4, in_var_v_c0, in_var_d_c0, in_var_v_cOuter,
                                in_var_d_cOuter, in_var_v_b4Outer, in_var_d_b4Outer)
        
        if isV == 1:
            in_var_v_c1 = []
            in_var_d_c1 = []
            for i in range(33):
                in_var_v_c1.append("cv1" + "_" + str(step) + "_" + str(i))
                in_var_d_c1.append("cd1" + "_" + str(step) + "_" + str(i))
            self.signed_q_model(in_var_v_b4, in_var_d_b4, in_var_v_c0, in_var_d_c0, in_var_v_c1,
                                in_var_d_c1, in_var_v_2, in_var_d_2, s)
            

    def rotate_diff_second(self, s, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, out_var_v_0, out_var_d_0,
                           in_var_v_2, in_var_d_2, in_var_v_b4Outer, in_var_d_b4Outer, isV, isK, step):

        in_var_v_b4 = []
        in_var_d_b4 = []
        for i in range(32):
            in_var_v_b4.append("bv4" + "_" + str(step) + "_" + str(i))
            in_var_d_b4.append("bd4" + "_" + str(step) + "_" + str(i))
        self.expand_model(in_var_v_b4, in_var_d_b4, in_var_v_0, in_var_d_0, isK, step)
        self.addexp_model(in_var_v_1, in_var_d_1, self.left_shift(in_var_v_b4, s), self.left_shift(in_var_d_b4, s),
                          out_var_v_0, out_var_d_0, step)
        
        eqn = ""
        for i in range(32):
            eqn += "ASSERT %s = %s;\n" % (
                self.save_variable(in_var_v_b4Outer[i]), self.save_variable(in_var_v_b4[((i - s) + 32) % 32]))
            eqn += "ASSERT %s = %s;\n" % (
                self.save_variable(in_var_d_b4Outer[i]), self.save_variable(in_var_d_b4[((i - s) + 32) % 32]))

        if isV == 1:
            for i in range(s + 1):
                eqn += "ASSERT %s = %s;\n" % (
                    self.save_variable(in_var_v_2[i]), self.save_variable(in_var_v_b4[((i - s) + 32) % 32]))
                eqn += "ASSERT %s = %s;\n" % (
                    self.save_variable(in_var_d_2[i]), self.save_variable(in_var_d_b4[((i - s) + 32) % 32]))
            self.__constraints.append(eqn)

    def modadd_value(self, a, b, c, v):
        eqn = " ASSERT %s = 0bin0;\n" % c[0]
        for i in range(32):
            temp = [self.save_variable(a[i]), 
                    self.save_variable(b[i]), 
                    self.save_variable(c[i]), 
                    self.save_variable(v[i]), 
                    self.save_variable(c[i + 1])]
            eqn += self.create_constraints(temp, modular_addition_value_constrain)
        self.__constraints.append(eqn)


    def val_add_model(self, a, b, v, l, step):

        eqn = "ASSERT c" + "_" + str(step) + "_" + str(0) + " = 0bin0;\n"
        for i in range(l):
            temp = [self.save_variable(a[i]),
                    self.save_variable(b[i]),
                    self.save_variable("c" + "_" + str(step) + "_" + str(i)),
                    self.save_variable(v[i]),
                    self.save_variable("c" + "_" + str(step) + "_" + str(i + 1))]
            eqn += self.create_constraints(temp, modular_addition_value_constrain)
        self.__constraints.append(eqn)


    def val_diff_add_model(self, in_var_v_a, in_var_d_a, b, v, l, num, step):

        eqn = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (
            self.save_variable("cv" + str(num) + "_" + str(step) + "_" + str(0)),
            self.save_variable("cd" + str(num) + "_" + str(step) + "_" + str(0)))
        for i in range(l):
            temp = [self.save_variable(in_var_v_a[i]),
                    self.save_variable(in_var_d_a[i]),

                    self.save_variable(b[i]),
                    self.save_variable("cv" + str(num) + "_" + str(step) + "_" + str(i)),
                    self.save_variable("cd" + str(num) + "_" + str(step) + "_" + str(i)),

                    self.save_variable("cv" + str(num) + "_" + str(step) + "_" + str(i + 1)),
                    self.save_variable("cd" + str(num) + "_" + str(step) + "_" + str(i + 1)),

                    self.save_variable(v[i])]
            eqn += self.create_constraints(temp, val_diff_add_constrain)

        self.__constraints.append(eqn)

    def rotate_diff_filter(self, s, in_var_v_a5, in_var_d_a5, in_var_v_a1, in_var_d_a1, in_var_v_b3, in_var_d_b3,
                           in_var_v_q, in_var_d_q, in_var_a5, in_var_a1, step):
        # Claim a binary vector q of size 32
        q = []
        for i in range(32):
            q.append("q" + "_" + str(step) + "_" + str(i))
        self.computer_q(in_var_v_a5, in_var_d_a5, in_var_v_a1, in_var_d_a1, in_var_a5, in_var_a1, q, step)
        # Claim a binary vector v0 of size s + 1
        v0 = []
        for i in range(s + 1):
            v0.append("v0" + "_" + str(step) + "_" + str(i))
        self.val_diff_add_model(in_var_v_q, in_var_d_q, q, v0, s + 1, 4, step)
        # Claim a binary vector v1 of size 33 − s
        v1 = []
        for i in range(33 - s):
            v1.append("v1" + "_" + str(step) + "_" + str(i))
        self.val_diff_add_model(in_var_v_b3, in_var_d_b3, self.right_shift(q, s), v1, 33 - s, 5, step)
        eqn = "ASSERT %s = %s;\n" % (self.save_variable(v0[0]), self.save_variable(v1[32 - s]))
        eqn += "ASSERT %s = %s;\n" % (self.save_variable(v0[s]), self.save_variable(v1[0]))
        self.__constraints.append(eqn)

    # get the real signed difference of b4
    def signed_b4_model(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, in_var_v_2, in_var_d_2, out_var_v,
                       out_var_d):

        eqn = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (in_var_v_2[0], in_var_d_2[0])

        temp = [self.save_variable(in_var_v_0[0]),
                self.save_variable(in_var_d_0[0]),

                self.save_variable(in_var_v_1[0]),
                self.save_variable(in_var_d_1[0]),

                self.save_variable(in_var_v_2[0]),
                self.save_variable(in_var_d_2[0]),

                self.save_variable(out_var_v[0]),
                self.save_variable(out_var_d[0]),

                self.save_variable(in_var_v_2[1]),
                self.save_variable(in_var_d_2[1])]
        eqn += self.create_constraints(temp, modadd_model_constrain)
        for i in range(1, 32):
            temp = [self.save_variable(in_var_v_0[i]),
                    self.save_variable(in_var_d_0[i]),
                    self.save_variable("temp1_v" + "_" + str(i)),
                    self.save_variable("temp1_d" + "_" + str(i)),

                    self.save_variable(in_var_v_2[i]),
                    self.save_variable(in_var_d_2[i]),

                    self.save_variable(out_var_v[i]),
                    self.save_variable(out_var_d[i]),

                    self.save_variable(in_var_v_2[i + 1]),
                    self.save_variable(in_var_d_2[i + 1])]
            eqn += self.create_constraints(temp, modadd_model_constrain)
            eqn += "ASSERT temp1_v" + "_" + str(i) + " = 0bin0;\n"
            eqn += "ASSERT temp1_d" + "_" + str(i) + " = 0bin0;\n"
        self.__constraints.append(eqn)

    # given a signed difference, calculate the corresponding modualr difference
    def getOnlyModular(self, in_var_v_0, in_var_d_0, in_var_v_1, in_var_d_1, out_var_v, out_var_d):
        eqn = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (in_var_v_1[0], in_var_d_1[0])
        for i in range(32):
            temp = [self.save_variable(in_var_v_0[i]),
                    self.save_variable(in_var_d_0[i]),

                    self.save_variable(in_var_v_1[i]),
                    self.save_variable(in_var_d_1[i]),

                    self.save_variable(out_var_v[i]),
                    self.save_variable(out_var_d[i]),

                    self.save_variable(in_var_v_1[i + 1]),
                    self.save_variable(in_var_d_1[i + 1])]
            eqn += self.create_constraints(temp, only_modular_constrain)
        self.__constraints.append(eqn)


    def R(self, fNa, isC, isF, isV, isK, s, in_var_v_m, in_var_d_m, in_var_v_a0, in_var_d_a0, in_var_v_a1,
          in_var_d_a1, in_var_v_a2, in_var_d_a2, in_var_v_a3, in_var_d_a3, in_var_v_a4, in_var_d_a4, in_var_v_a5,
          in_var_d_a5, in_var_a4, in_var_a3, in_var_a2, in_var_a5, in_var_a1, step):

        # Claim signed difference vectors ∇b0,∇b1,∇b2,∇b3 of size 32,let a reputation b0, b1,b2,b3
        in_var_v_b0 = []
        in_var_d_b0 = []
        in_var_v_b1 = []
        in_var_d_b1 = []
        in_var_v_b2 = []
        in_var_d_b2 = []
        in_var_v_b3 = []
        in_var_d_b3 = []
        for i in range(32):
            in_var_v_b0.append("bv0" + "_" + str(step) + "_" + str(i))
            in_var_d_b0.append("bd0" + "_" + str(step) + "_" + str(i))
            in_var_v_b1.append("bv1" + "_" + str(step) + "_" + str(i))
            in_var_d_b1.append("bd1" + "_" + str(step) + "_" + str(i))
            in_var_v_b2.append("bv2" + "_" + str(step) + "_" + str(i))
            in_var_d_b2.append("bd2" + "_" + str(step) + "_" + str(i))
            in_var_v_b3.append("bv3" + "_" + str(step) + "_" + str(i))
            in_var_d_b3.append("bd3" + "_" + str(step) + "_" + str(i))

        # Claim signed difference vectors ∇c2,∇c3 of size 33.
        in_var_v_c2 = []
        in_var_d_c2 = []
        in_var_v_c3 = []
        in_var_d_c3 = []
        for i in range(33):
            in_var_v_c2.append("cv2" + "_" + str(step) + "_" + str(i))
            in_var_d_c2.append("cd2" + "_" + str(step) + "_" + str(i))
            in_var_v_c3.append("cv3" + "_" + str(step) + "_" + str(i))
            in_var_d_c3.append("cd3" + "_" + str(step) + "_" + str(i))
        # Claim a signed difference vector ∇q of size s + 1.
        in_var_v_q = []
        in_var_d_q = []
        for i in range(s + 1):
            in_var_v_q.append("qv" + "_" + str(step) + "_" + str(i))
            in_var_d_q.append("qd" + "_" + str(step) + "_" + str(i))

        eqn = "% assign m to b0\n"
        for i in range(32):
            eqn += "ASSERT %s = %s;\n" % (self.save_variable(in_var_v_m[i]), self.save_variable(in_var_v_b0[i]))
            eqn += "ASSERT %s = %s;\n" % (self.save_variable(in_var_d_m[i]), self.save_variable(in_var_d_b0[i]))
        self.__constraints.append(eqn) 

        # Claim a bitconditionnumber of size 32.
        if fNa == "XOR":
            in_var_d_bitconditionNumber = []
            for i in range(32):
                in_var_d_bitconditionNumber.append("bitconditionNumberd" + "_" + str(step) + "_" + str(i))
            self.boolConditionNumber_model_XOR(fNa, in_var_v_a4, in_var_d_a4, in_var_v_a3, in_var_d_a3, in_var_v_a2, in_var_d_a2,
                                in_var_v_b1, in_var_d_b1, in_var_d_bitconditionNumber)
        else:
            in_var_v_bitconditionNumber = []
            in_var_d_bitconditionNumber = []
            for i in range(32):
                in_var_v_bitconditionNumber.append("bitconditionNumberv" + "_" + str(step) + "_" + str(i))
                in_var_d_bitconditionNumber.append("bitconditionNumberd" + "_" + str(step) + "_" + str(i))

            self.boolConditionNumber_model(fNa, in_var_v_a4, in_var_d_a4, in_var_v_a3, in_var_d_a3, in_var_v_a2, in_var_d_a2,
                                in_var_v_b1, in_var_d_b1, in_var_v_bitconditionNumber, in_var_d_bitconditionNumber)
        
        if isC == 1:
            self.boolFull_model(fNa, in_var_v_a4, in_var_d_a4, in_var_v_a3, in_var_d_a3, in_var_v_a2,
                                in_var_d_a2, in_var_v_b1, in_var_d_b1, in_var_a4, in_var_a3, in_var_a2)
        # no carry for the least significant bit.
        eqn = "% no carry for the least significant bit\n"
        eqn += "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (self.save_variable(in_var_v_c2[0]),
                                                             self.save_variable(in_var_d_c2[0]))
        eqn += "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (self.save_variable(in_var_v_c3[0]),
                                                             self.save_variable(in_var_d_c3[0]))
        self.__constraints.append(eqn)
        self.modadd_model(in_var_v_b0, in_var_d_b0, in_var_v_b1, in_var_d_b1, in_var_v_c2, in_var_d_c2,
                          in_var_v_b2, in_var_d_b2)
        self.modadd_model(in_var_v_b2, in_var_d_b2, in_var_v_a0, in_var_d_a0, in_var_v_c3, in_var_d_c3,
                          in_var_v_b3, in_var_d_b3)

        # real signed difference of b4
        in_var_v_b4Outer = []
        in_var_d_b4Outer = []

        for i in range(32):
            in_var_v_b4Outer.append("bv4Outer" + "_" + str(step) + "_" + str(i))
            in_var_d_b4Outer.append("bd4Outer" + "_" + str(step) + "_" + str(i))

        if isF == 1:
            self.rotate_diff_first(s, in_var_v_b3, in_var_d_b3, in_var_v_a1, in_var_d_a1, in_var_v_a5,
                                   in_var_d_a5, in_var_v_q, in_var_d_q, in_var_v_b4Outer, in_var_d_b4Outer, 
                                   isV, isK, step)
        else:
            self.rotate_diff_second(s, in_var_v_b3, in_var_d_b3, in_var_v_a1, in_var_d_a1, in_var_v_a5,
                                    in_var_d_a5, in_var_v_q, in_var_d_q, in_var_v_b4Outer, in_var_d_b4Outer, 
                                    isV, isK, step)
        
        # Claim a bitconditionnumber of size 32.
        in_var_v_innerModular = []
        in_var_d_innerModular = []
        in_var_v_outerModular = []
        in_var_d_outerModular = []
        for i in range(32):
            in_var_v_innerModular.append("innerModularv" + "_" + str(step) + "_" + str(i))
            in_var_d_innerModular.append("innerModulard" + "_" + str(step) + "_" + str(i))
            in_var_v_outerModular.append("outerModularv" + "_" + str(step) + "_" + str(i))
            in_var_d_outerModular.append("outerModulard" + "_" + str(step) + "_" + str(i))
        
        in_var_v_cInner = []
        in_var_d_cInner = []
        in_var_v_cOuter = []
        in_var_d_cOuter = []
        for i in range(33):
            in_var_v_cInner.append("cvInner" + "_" + str(step) + "_" + str(i))
            in_var_d_cInner.append("cdInner" + "_" + str(step) + "_" + str(i))
            in_var_v_cOuter.append("cvOuter" + "_" + str(step) + "_" + str(i))
            in_var_d_cOuter.append("cdOuter" + "_" + str(step) + "_" + str(i))

        self.getOnlyModular(in_var_v_b3, in_var_d_b3, in_var_v_cInner, in_var_d_cInner, in_var_v_innerModular, in_var_d_innerModular)
        self.getOnlyModular(in_var_v_b4Outer, in_var_d_b4Outer, in_var_v_cOuter, in_var_d_cOuter, in_var_v_outerModular, in_var_d_outerModular)
        
        flag0 = "flag0" + "_" + str(step)
        flag1 = "flag1" + "_" + str(step)
        eqn = "ASSERT %s = IF %s = %s THEN 0bin1 ELSE 0bin0 ENDIF;\n" % (self.save_variable(flag0),
                                                             self.save_variable(in_var_d_innerModular[32-s]), self.save_variable(in_var_d_outerModular[0]))
        eqn += "ASSERT %s = IF %s = %s THEN 0bin1 ELSE 0bin0 ENDIF;\n" % (self.save_variable(flag1),
                                                             self.save_variable(in_var_d_innerModular[0]), self.save_variable(in_var_d_outerModular[s]))
        self.__constraints.append(eqn)


        in_var_targetInModular = []
        eqn = ""
        for i in range(32 - s):
            in_var_targetInModular.append("targetInModular" + "_" + str(step) + "_" + str(i))
            eqn += "ASSERT %s = IF %s = 0bin1 THEN ~%s ELSE %s ENDIF;\n" % (self.save_variable(in_var_targetInModular[i]), self.save_variable(flag0), 
                                                                    self.save_variable(in_var_d_innerModular[i]), self.save_variable(in_var_d_innerModular[i]))
        
        in_var_targetOutModular = []
        for i in range(s):
            in_var_targetOutModular.append("targetOutModular" + "_" + str(step) + "_" + str(i))
            eqn += "ASSERT %s = IF %s = 0bin1 THEN ~%s ELSE %s ENDIF;\n" % (self.save_variable(in_var_targetOutModular[i]), self.save_variable(flag1), 
                                                                    self.save_variable(in_var_d_outerModular[i]), self.save_variable(in_var_d_outerModular[i]))
        self.__constraints.append(eqn)
        
        w0 = "w0" + "_" + str(step)
        w1 = "w1" + "_" + str(step)
        self.__declare.append(w0 + ": BITVECTOR(6);\n")
        self.__declare.append(w1 + ": BITVECTOR(6);\n")

        eqn = ""
        for i in range(32 - s):
            eqn += "ASSERT IF "
            for j in range(i + 1):
                if j == i:
                    eqn += "%s = 0bin" % (in_var_targetInModular[31-s-j])
                else:
                    eqn += "%s@" % (in_var_targetInModular[31-s-j])
            for j in range(i + 1):
                if j == i:
                    eqn += "1 THEN %s = 0bin%s ELSE 0bin1 = 0bin1 ENDIF;\n" % (w0, bin(i+1)[2:].zfill(6))
                else:
                    eqn += "0"      

        eqn += "ASSERT IF "
        for j in range(32-s):
            if j == 31 - s:
                eqn += "%s = 0bin" % (in_var_targetInModular[31-s-j])
            else:
                eqn += "%s@" % (in_var_targetInModular[31-s-j])
        for j in range(32-s):
            if j == 31 - s:
                eqn += "0 THEN %s = 0bin%s ELSE 0bin1 = 0bin1 ENDIF;\n" % (w0, bin(40)[2:].zfill(6))
            else:
                eqn += "0"
        self.__constraints.append(eqn)

    
        eqn = ""
        for i in range(s):
            eqn += "ASSERT IF "
            for j in range(i + 1):
                if j == i:
                    eqn += "%s = 0bin" % (in_var_targetOutModular[s-1-j])
                else:
                    eqn += "%s@" % (in_var_targetOutModular[s-1-j])
            for j in range(i + 1):
                if j == i:
                    eqn += "1 THEN %s = 0bin%s ELSE 0bin1 = 0bin1 ENDIF;\n" % (w1, bin(i+1)[2:].zfill(6))
                else:
                    eqn += "0"      

        eqn += "ASSERT IF "
        for j in range(s):
            if j == s - 1:
                eqn += "%s = 0bin" % (in_var_targetOutModular[s-1-j])
            else:
                eqn += "%s@" % (in_var_targetOutModular[s-1-j])
        for j in range(s):
            if j == s - 1:
                eqn += "0 THEN %s = 0bin%s ELSE 0bin1 = 0bin1 ENDIF;\n" % (w1, bin(40)[2:].zfill(6))
            else:
                eqn += "0"
        self.__constraints.append(eqn)
        
        
        if isV == 1:
            self.rotate_diff_filter(s, in_var_v_a5, in_var_d_a5, in_var_v_a1, in_var_d_a1, in_var_v_b3,
                                    in_var_d_b3, in_var_v_q, in_var_d_q, in_var_a5, in_var_a1, step)


    def ripemd_value(self, fNa, s, in_var_m, in_var_a0, in_var_a1, in_var_a2, in_var_a3, in_var_a4, in_var_a5, constant, step):
        # constant
        c = []
        for i in range(32):
            c.append("constant_" + str(step) + "_" + str(i))
            self.__constraints.append("ASSERT %s = 0bin%s;\n" % (self.save_variable("constant_" + str(step) + "_" + str(31 - i)), bin(constant)[2:].zfill(32)[i])) 

        in_var_b = []
        for j in range(4):
            in_var_bc = []
            for i in range(32):
                in_var_bc.append("b" + str(j) + "_" + str(step) + "_" + str(i))
            in_var_b.append(in_var_bc)

        in_var_c = []
        for j in range(4):
            in_var_cm = []
            for i in range(33):
                in_var_cm.append("c" + str(j) + "_" + str(step) + "_" + str(i))
            in_var_c.append(in_var_cm)

        self.boolean_value(fNa, in_var_a4, in_var_a3, in_var_a2, in_var_b[0])
        self.modadd_value(in_var_b[0], in_var_a0, in_var_c[0], in_var_b[1])
        self.modadd_value(in_var_m, in_var_b[1], in_var_c[1], in_var_b[2])
        self.modadd_value(c, in_var_b[2], in_var_c[2], in_var_b[3])
        self.modadd_value(self.left_shift(in_var_b[3], s), in_var_a1, in_var_c[3], in_var_a5)


    def check_assign(self, s):
        if s not in self.__assign:
            self.__assign.append(s)

    def assign_value(self):
        for i in range(15, 20):
            for j in range(32):
                temp = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (self.save_variable("xd_" + str(i) + "_" + str(j)),
                                                                     self.save_variable("xv_" + str(i) + "_" + str(j)))
                self.check_assign(temp)

        for i in range(16):
            for j in range(32):
                if i == 12 and (j == 15):
                    temp = "ASSERT %s = 0bin1;\nASSERT %s = 0bin0;\n" % (
                        self.save_variable("md_" + str(i) + "_" + str(j)),
                        self.save_variable("mv_" + str(i) + "_" + str(j)))
                    self.check_assign(temp)

                else:
                    temp = "ASSERT %s = 0bin0;\nASSERT %s = 0bin0;\n" % (
                        self.save_variable("md_" + str(i) + "_" + str(j)),
                        self.save_variable("mv_" + str(i) + "_" + str(j)))
                    self.check_assign(temp)

    # objective function
    def Object(self, object_value):
        obj = "pro: BITVECTOR(13);\n"
        obj += "ASSERT pro = BVPLUS(13,"
        # the conditions derived by boolean functions
        for i in range(self.__step, self.__bounds_rounds):
            if self.__boolFunction_right[(i - 5) // 16] == "XOR":
                for j in range(32):
                    obj += "0bin000000000000@bitconditionNumberd_%s_%s" % (i, j) + ", "
            else:
                for j in range(32):
                    obj += "0bin000000000000@bitconditionNumberv_%s_%s" % (i, j) + ", "
                    obj += "0bin000000000000@bitconditionNumberd_%s_%s" % (i, j) + ", "
        
        # the probabilities derived by <<< s
        for i in range(self.__step, self.__bounds_rounds):
            obj += "0bin0000000@w0_%s" % (i) + ", "
            obj += "BVUMINUS(0bin000000000000@flag0_%s)" % (i) + ", "
            obj += "0bin0000000@w1_%s" % (i) + ", "
            obj += "BVUMINUS(0bin000000000000@flag1_%s)" % (i) + ", "

        # hamming weight
        for i in range(self.__step, self.__bounds_rounds):
            for j in range(32):
                if i == self.__bounds_rounds - 1 and j == 31:
                    obj += "0bin000000000000@xd_%s_%s);\n" % (i, j)
                else:
                    obj += "0bin000000000000@xd_%s_%s" % (i, j) + ", "


        obj += "ASSERT BVLE(pro, 0bin%s);\n" %bin(object_value)[2:].zfill(13)


        # # 加入约束: 循环移位的概率
        # obj += "ASSERT BVGE(BVPLUS(10,"
        # for i in range(self.__step, self.__bounds_rounds):
        #     if i == self.__bounds_rounds - 1:
        #         obj += "0bin0000@w0_%s" % (i) + ", "
        #         obj += "BVUMINUS(0bin000000000@flag0_%s)" % (i) + ", "
        #         obj += "0bin0000@w1_%s" % (i) + ", "
        #         obj += "BVUMINUS(0bin000000000@flag1_%s)" % (i)
        #     else:
        #         obj += "0bin0000@w0_%s" % (i) + ", "
        #         obj += "BVUMINUS(0bin000000000@flag0_%s)" % (i) + ", "
        #         obj += "0bin0000@w1_%s" % (i) + ", "
        #         obj += "BVUMINUS(0bin000000000@flag1_%s)" % (i) + ", "
        # obj += "), 0bin%s);\n" %bin(4)[2:].zfill(10)

        return obj

    def main(self):
        in_var_v_a = []
        in_var_d_a = []
        in_var_v_m = []
        in_var_d_m = []
        in_var_a = []

        for step in range(0, self.__bounds_rounds):
            temp_v_a = []
            temp_d_a = []
            temp_a = []
            for i in range(32):
                temp_v_a.append("xv_" + str(step) + "_" + str(i))
                temp_d_a.append("xd_" + str(step) + "_" + str(i))
                temp_a.append("x_" + str(step) + "_" + str(i))
            in_var_v_a.append(temp_v_a)
            in_var_d_a.append(temp_d_a)

            in_var_a.append(temp_a)
            
        for step in range(0, self.__bounds_rounds):
            temp_v_m = []
            temp_d_m = []
            for i in range(32):
                temp_v_m.append("mv_" + str(self.__OrderMessageWords_right[step]) + "_" + str(i))
                temp_d_m.append("md_" + str(self.__OrderMessageWords_right[step]) + "_" + str(i))
            in_var_v_m.append(temp_v_m)
            in_var_d_m.append(temp_d_m)

        for i in range(self.__step, self.__bounds_rounds):
            self.R(self.__boolFunction_right[(i - 5) // 16], self.__isc[i], self.__isf[i], self.__isv[i],
                   self.__isk[i],
                   self.__RotateCons_right[i],
                   in_var_v_m[i],
                   in_var_d_m[i],
                   self.left_shift(in_var_v_a[i - 5], 10),
                   self.left_shift(in_var_d_a[i - 5], 10),
                   self.left_shift(in_var_v_a[i - 4], 10),
                   self.left_shift(in_var_d_a[i - 4], 10),
                   self.left_shift(in_var_v_a[i - 3], 10),
                   self.left_shift(in_var_d_a[i - 3], 10),
                   in_var_v_a[i - 2],
                   in_var_d_a[i - 2],
                   in_var_v_a[i - 1],
                   in_var_d_a[i - 1],
                   in_var_v_a[i],
                   in_var_d_a[i],

                   in_var_a[i - 1],
                   in_var_a[i - 2],
                   self.left_shift(in_var_a[i - 3], 10),
                   in_var_a[i],
                   self.left_shift(in_var_a[i - 4], 10),
                   i)
            

    def solver(self):
        self.main()
        self.assign_value()
        constrain = "".join(self.__constraints)
        assign = "".join(self.__assign)
        variable = "".join(self.__declare)
        query = '\n' + 'QUERY FALSE;\nCOUNTEREXAMPLE;'

        pro = 49
        while True:
            print("the probability of differential characteristic: %s" % (pro - 1))
            obj = self.Object(pro - 1)
            file_write = open("right_model_43.cvc", "w")
            file_write.write(variable)
            file_write.write(constrain)
            file_write.write(assign)
            file_write.write(obj)
            file_write.write(query)
            file_write.close()
            stp_parameters = ["stp", "right_model_43.cvc", "--cryptominisat", "--threads", "64"]
            R = subprocess.check_output(stp_parameters)

            if "Valid.\n" != R.decode():
                old_name = "right_res2_m12_" + str(pro - 1) + ".out"
                file = open("right_res2_m12_" + str(pro - 1) + ".out", "w")
                file.write(R.decode())
                file.close()
                data_list = open("right_res2_m12_" + str(pro - 1) + ".out", "r").read()
                data = data_list.replace("ASSERT( ", "").replace(" );", "").replace("\nInvalid.", "").split("\n")
                for i in data:
                    if "pro" in i:
                        temp = i.split(" = ")
                        pro = int(temp[1], 2)
                print("the probability of differential characteristic: %s satisfied" % pro)
                os.rename(old_name, "right_res2_m12_" + str(pro) + ".out")

            else:
                print("the probability of differential characteristic: %s unsatisfied" % (pro - 1))
                break

        for temp in read_differential_characteristic("right_res2_m12_" + str(pro) + ".out", self.__bounds_rounds):
            print(temp)
    
if __name__ == '__main__':
    start = time.time()
    step = 20
    bounds = 37
    FunctionModel(step, bounds).solver()
    print()
    print("Time: ", time.time()- start)