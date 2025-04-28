// 统计每一步的概率
#include <string>
#include <iostream>
#include <vector>
#include <random>
#include <cstdint>
#include <chrono>
#include <thread>
#include <atomic>
#include <iomanip>

using namespace std;
const int cons = 7;

double calculate_mean(const vector<double>& data) {
    double sum = 0.0;
    for (const auto& value : data) {
        sum += value;
    }
    return sum / data.size();
}

double calculate_variance(const vector<double>& data) {
    double mean = calculate_mean(data);
    double variance = 0.0;
    for (const auto& value : data) {
        variance += (value - mean) * (value - mean);
    }
    return variance / data.size();
}

// generate random numbers that satisfies the conditions
uint32_t adjustRandomNumber(uint32_t random_number, const string& pattern, int flag) {
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


uint32_t ONZ(uint32_t x, uint32_t y, uint32_t z) {
    return (x | ~y) ^ z;
}


// Step function
vector<uint32_t> step_function(uint32_t x0, uint32_t x1, uint32_t x2, uint32_t x3, uint32_t x4, uint32_t m, int s) {
    uint32_t b0 = ONZ(x4, x3, leftRotate(x2, 10)) & 0xffffffff;
    uint32_t b1 = (b0 + leftRotate(x0, 10) + m) & 0xffffffff;
    return {x1, x2, x3, x4, (leftRotate(x1, 10) + leftRotate(b1, s)) & 0xffffffff};
}

void hash_collision_detection(int thread_id, int num_threads, int64_t dataTotal, int s[], uint32_t K, atomic<int>& number_39, atomic<int>& number_40,atomic<int>& number_41, atomic<int>& number_42, atomic<int>& number_43,vector<uint32_t> m0, vector<uint32_t> m1, vector<uint32_t> result) {
    
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<uint32_t> dis(0, UINT32_MAX);

    string patterns[] = {
        "==1=====================0=======", // Y32
        "==1======0======================", // Y33
        "=========n==============1=======", // Y34
        "=========1==============u======0", // Y35
        "=========1====1=========10======", // Y36
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

        for (round = 0; round < cons; round++) {
            hash0 = step_function(hash0[0], hash0[1], hash0[2], hash0[3], hash0[4], m0[round], s[round]);
            hash1 = step_function(hash1[0], hash1[1], hash1[2], hash1[3], hash1[4], m1[round], s[round]);
        }

        if (((hash1[0] - hash0[0]) & 0xffffffff) == result[0]) {
            number_39++;
            if (((hash1[1] - hash0[1]) & 0xffffffff) == result[1]) {
                number_40++;
                if (((hash1[2] - hash0[2]) & 0xffffffff) == result[2]) {
                    number_41++;
                    if (((hash1[3] - hash0[3]) & 0xffffffff) == result[3]) {
                        number_42++;
                        if (((hash1[4] - hash0[4]) & 0xffffffff) == result[4]) {
                            number_43++;
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
    int data = 38;
    int64_t dataTotal = 274877906944;  // data: pow(2, 38)
    
    // the modular difference of (Y39, Y40, Y41, Y42, Y43)
    vector<uint32_t> result = {0xfffe0000, 0xf0000000, 0xff7f4000, 0x3ff, 0xf90f8000};
    vector<uint32_t> modularM = {0x0, 0x0, 0x0, 0x0, 0x0, 0x8000, 0x0};
    int s[cons] = {6, 6, 14, 12, 13, 5, 14};
    uint32_t K = 0x6d703ef3;

    vector<thread> threads;

    cout << "thread number: " << num_threads << endl;
    cout << "data number: " << dataTotal << endl;

    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<uint32_t> dis(0, UINT32_MAX);

    int test_number = 200;
    vector<double> proList_39(test_number, 0);
    vector<double> proList_40(test_number, 0);
    vector<double> proList_41(test_number, 0);
    vector<double> proList_42(test_number, 0);
    vector<double> proList_43(test_number, 0);

    for (int cishu = 0; cishu < test_number; cishu++){
        atomic<int> number_39(0);
        atomic<int> number_40(0);
        atomic<int> number_41(0);
        atomic<int> number_42(0);
        atomic<int> number_43(0);

        vector<uint32_t> m0(cons, 0);
        vector<uint32_t> m1(cons, 0);

        for (int i = 0; i < cons; i++) {
            m0[i] = dis(gen) + K;
            m1[i] = (m0[i] + modularM[i]) & 0xffffffff;
        }


        cout << "message words: " << endl;
        for (int i = 0; i < cons; i++) {
            cout << "0x" << setw(8) << setfill('0') << hex << m0[i] << "  " << "0x" << setw(8) << setfill('0') << hex << m1[i] << endl;
        }
        cout << endl;

        for (int i = 0; i < num_threads; i++) {
            threads.push_back(thread(hash_collision_detection, i, num_threads, dataTotal, s, K, ref(number_39),ref(number_40),ref(number_41), ref(number_42), ref(number_43), m0, m1, result));
        }

        for (auto& t : threads) {
            t.join();
        }
        threads.clear(); 

        proList_39[cishu] = static_cast<double>(number_39) / dataTotal;
        proList_40[cishu] = static_cast<double>(number_40) / dataTotal;
        proList_41[cishu] = static_cast<double>(number_41) / dataTotal;
        proList_42[cishu] = static_cast<double>(number_42) / dataTotal;
        proList_43[cishu] = static_cast<double>(number_43) / dataTotal;
    }


    double mean = calculate_mean(proList_39);
    double variance = calculate_variance(proList_39);
    std::cout << "Mean39: " << mean << std::endl;
    std::cout << "Variance39: " << variance << std::endl;

    mean = calculate_mean(proList_40);
    variance = calculate_variance(proList_40);
    std::cout << "Mean40: " << mean << std::endl;
    std::cout << "Variance40: " << variance << std::endl;

    mean = calculate_mean(proList_41);
    variance = calculate_variance(proList_41);
    std::cout << "Mean41: " << mean << std::endl;
    std::cout << "Variance41: " << variance << std::endl;

    mean = calculate_mean(proList_42);
    variance = calculate_variance(proList_42);
    std::cout << "Mean42: " << mean << std::endl;
    std::cout << "Variance42: " << variance << std::endl;

    mean = calculate_mean(proList_43);
    variance = calculate_variance(proList_43);
    std::cout << "Mean43: " << mean << std::endl;
    std::cout << "Variance43: " << variance << std::endl;


    cout << endl << "39" << endl;
    for (int i = 0; i < test_number; i++){
        cout << proList_39[i] << ", ";
    }

    cout << endl << "40" << endl;
    for (int i = 0; i < test_number; i++){
        cout << proList_40[i] << ", ";
    }

    cout << endl << "41" << endl;
    for (int i = 0; i < test_number; i++){
        cout << proList_41[i] << ", ";
    }

    cout << endl << "42" << endl;
    for (int i = 0; i < test_number; i++){
        cout << proList_42[i] << ", ";
    }

    cout << endl << "43" << endl;
    for (int i = 0; i < test_number; i++){
        cout << proList_43[i] << ", ";
    }

    cout << endl;
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> duration = end - start;
    cout << "Execution time: " << duration.count() << " s" << endl;

    return 0;
}
