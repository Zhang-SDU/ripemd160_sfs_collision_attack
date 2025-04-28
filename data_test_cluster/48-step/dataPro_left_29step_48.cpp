#include <string>
#include <iostream>
#include <vector>
#include <random>
#include <cstdint>
#include <chrono>
#include <thread>
#include <atomic>

using namespace std;

int m_order[29] = { 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12, 1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2};

double calculate_mean(const std::vector<double>& data) {
    double sum = 0.0;
    for (const auto& value : data) {
        sum += value;
    }
    return sum / data.size();
}

double calculate_variance(const std::vector<double>& data) {
    double mean = calculate_mean(data);
    double variance = 0.0;
    for (const auto& value : data) {
        variance += (value - mean) * (value - mean);
    }
    return variance / data.size();
}


// generate random numbers that satisfies the conditions
uint32_t adjustRandomNumber(uint32_t random_number, const std::string& pattern, int flag) {
    uint32_t temp = random_number;
    if (flag == 0){
        for (size_t i = 0; i < pattern.size(); ++i) 
        {
            char bit = pattern[i];
            uint32_t mask = 1U << (31 - i);

            if (bit == 'n' || bit == '0') {
                temp &= ~mask;
            } else if (bit == 'u' || bit == '1') {
                temp |= mask;
            }
        }
    }
    else{
        for (size_t i = 0; i < pattern.size(); ++i)
         {
            char bit = pattern[i];
            uint32_t mask = 1U << (31 - i);

            if (bit == 'n' || bit == '1') {
                temp |= mask;
            } else if (bit == 'u' || bit == '0') {
                temp &= ~mask;
            }
        }
    }
    return temp;
}



uint32_t leftRotate(uint32_t n, int s) {
    return (n << s) | (n >> (32 - s));
}

uint32_t IFX(uint32_t x, uint32_t y, uint32_t z) {
    return ((x & y) ^ (~x & z));
}

uint32_t ONZ(uint32_t x, uint32_t y, uint32_t z) {
    return (x | ~y) ^ z;
}

uint32_t IFZ(uint32_t x, uint32_t y, uint32_t z) {
    return ((x & z) ^ (~z & y));
}

// Step function
vector<uint32_t> step_function_ONZ(uint32_t x0, uint32_t x1, uint32_t x2, uint32_t x3, uint32_t x4, uint32_t m, int s) {
    uint32_t b0 = ONZ(x4, x3, leftRotate(x2, 10)) & 0xffffffff;
    uint32_t b1 = (b0 + leftRotate(x0, 10) + m) & 0xffffffff;
    return {x1, x2, x3, x4, (leftRotate(x1, 10) + leftRotate(b1, s)) & 0xffffffff};
}

// Step function
vector<uint32_t> step_function_IFZ(uint32_t x0, uint32_t x1, uint32_t x2, uint32_t x3, uint32_t x4, uint32_t m, int s) {
    uint32_t b0 = IFZ(x4, x3, leftRotate(x2, 10)) & 0xffffffff;
    uint32_t b1 = (b0 + leftRotate(x0, 10) + m) & 0xffffffff;
    return {x1, x2, x3, x4, (leftRotate(x1, 10) + leftRotate(b1, s)) & 0xffffffff};
}

void hash_collision_detection(int thread_id, int num_threads, int64_t dataTotal, int s[], uint32_t K1, uint32_t K2, atomic<int>& number_59, atomic<int>& number_60, atomic<int>& number_61, atomic<int>& number_62, atomic<int>& number_63, vector<uint32_t> m0, vector<uint32_t> m1, vector<uint32_t> result) {

    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<uint32_t> dis(0, UINT32_MAX);

    // X30 ———— X34
    // [31][8] | 7[30][8] = 1
    // [32][8] | 7[31][8] = 1
    // [34][29] | 7[33][29] = 1
    // [34][27] | 7[33][27] = 1
    // [34][25] | 7[33][25] = 1
    // [34][16] | 7[33][16] = 1
    // [35][4] | 7[34][4] = 1
    // [35][2] | 7[34][2] = 1
    string patterns[] = {
        "nn0u0n=1un1101unnu0111u01=nnnnnn",  // 30  
        "10=nnn101111011011=1110001n1n0u0",  // 31 
        "===u1100====u=u0n01=00u==u111=0=",  // 32 
        "==0n=n0u====0=0=0=0===0==10=====",  // 33 
        "===110=0=======1======u==u=0=0=="   // 34 
    };


    vector<uint32_t> initial_values(5, 0);
    vector<uint32_t> hash0(5, 0), hash1(5, 0);
    for (int64_t i = thread_id; i < dataTotal; i += num_threads) {
        initial_values = {dis(gen), dis(gen), dis(gen), dis(gen), dis(gen)};
        for(int j = 0; j < 5; j++){
            hash0[j] = adjustRandomNumber(initial_values[j], patterns[j], 0);
            hash1[j] = adjustRandomNumber(initial_values[j], patterns[j], 1);
        }

        int round;
        for (round = 0; round < 13; round++) {
            hash0 = step_function_ONZ(hash0[0], hash0[1], hash0[2], hash0[3], hash0[4], m0[m_order[round]] + K1, s[round]);
            hash1 = step_function_ONZ(hash1[0], hash1[1], hash1[2], hash1[3], hash1[4], m1[m_order[round]] + K1, s[round]);
        }

        for (round = 13; round < 29; round++) {
            hash0 = step_function_IFZ(hash0[0], hash0[1], hash0[2], hash0[3], hash0[4], m0[m_order[round]] + K2, s[round]);
            hash1 = step_function_IFZ(hash1[0], hash1[1], hash1[2], hash1[3], hash1[4], m1[m_order[round]] + K2, s[round]);
        }

        if (((hash1[0] - hash0[0]) & 0xffffffff) == result[0]) {
            number_59++;
            if (((hash1[1] - hash0[1]) & 0xffffffff) == result[1]) {
                number_60++;
                if (((hash1[2] - hash0[2]) & 0xffffffff) == result[2]) {
                    number_61++;
                    if (((hash1[3] - hash0[3]) & 0xffffffff) == result[3]) {
                        number_62++;
                        if (((hash1[4] - hash0[4]) & 0xffffffff) == result[4]) {
                            number_63++;
                        }
                    }
                }
            }
        }
    }
}

int main() {
    auto start = chrono::high_resolution_clock::now();

    int num_threads = thread::hardware_concurrency();
    int data = 24;
    int64_t dataTotal = 16777216;

    vector<uint32_t> result = {0x0, 0x0, 0x0, 0x80000000, 0x0};
    int s[29] = {7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5, 11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12};
    uint32_t K1 = 0x6ed9eba1;
    uint32_t K2 = 0x8f1bbcdc;

    vector<thread> threads;

    cout << "thread number: " << num_threads << endl;
    cout << "data number: " << dataTotal << endl;

    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<uint32_t> dis(0, UINT32_MAX);

    int cishu_number = 1024;
    vector<double> proList_59(cishu_number, 0);
    vector<double> proList_60(cishu_number, 0);
    vector<double> proList_61(cishu_number, 0);
    vector<double> proList_62(cishu_number, 0);
    vector<double> proList_63(cishu_number, 0);

    for (int cishu = 0; cishu < cishu_number; cishu++){
        atomic<int> number_59(0);
        atomic<int> number_60(0);
        atomic<int> number_61(0);
        atomic<int> number_62(0);
        atomic<int> number_63(0);

        vector<uint32_t> m0(16, 0);
        vector<uint32_t> m1(16, 0);
        for (int i = 0; i < 16; i++) {
            m0[i] = dis(gen);
            if (i == 7) {
                m1[i] = (m0[i] + 0x10000) & 0xffffffff;
            }
            else {
                m1[i] = m0[i];
            }
        }


        for (int i = 0; i < num_threads; i++) {
            threads.push_back(thread(hash_collision_detection, i, num_threads, dataTotal, s, K1, K2, ref(number_59), ref(number_60), ref(number_61), ref(number_62), ref(number_63), m0, m1, result));
        }

        for (auto& t : threads) {
            t.join();
        }

        threads.clear();  // 清空线程池

        proList_59[cishu] = static_cast<double>(number_59) / dataTotal;
        proList_60[cishu] = static_cast<double>(number_60) / dataTotal;
        proList_61[cishu] = static_cast<double>(number_61) / dataTotal;
        proList_62[cishu] = static_cast<double>(number_62) / dataTotal;
        proList_63[cishu] = static_cast<double>(number_63) / dataTotal;
    }


    double mean = calculate_mean(proList_59);
    double variance = calculate_variance(proList_59);
    std::cout << "Mean59: " << mean << std::endl;
    std::cout << "Variance59: " << variance << std::endl;

    mean = calculate_mean(proList_60);
    variance = calculate_variance(proList_60);
    std::cout << "Mean60: " << mean << std::endl;
    std::cout << "Variance60: " << variance << std::endl;

    mean = calculate_mean(proList_61);
    variance = calculate_variance(proList_61);
    std::cout << "Mean61: " << mean << std::endl;
    std::cout << "Variance61: " << variance << std::endl;

    mean = calculate_mean(proList_62);
    variance = calculate_variance(proList_62);
    std::cout << "Mean62: " << mean << std::endl;
    std::cout << "Variance62: " << variance << std::endl;

    mean = calculate_mean(proList_63);
    variance = calculate_variance(proList_63);
    std::cout << "Mean63: " << mean << std::endl;
    std::cout << "Variance63: " << variance << std::endl;


    cout << endl << "59" << endl;
    for (int i = 0; i < cishu_number; i++){
        cout << proList_59[i] << ", ";
    }

    cout << endl << "60" << endl;
    for (int i = 0; i < cishu_number; i++){
        cout << proList_60[i] << ", ";
    }

    cout << endl << "61" << endl;
    for (int i = 0; i < cishu_number; i++){
        cout << proList_61[i] << ", ";
    }

    cout << endl << "62" << endl;
    for (int i = 0; i < cishu_number; i++){
        cout << proList_62[i] << ", ";
    }

    cout << endl << "63" << endl;
    for (int i = 0; i < cishu_number; i++){
        cout << proList_63[i] << ", ";
    }

    cout << endl;
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> duration = end - start;
    cout << "Execution time: " << duration.count() << " s" << endl;

    return 0;
}
