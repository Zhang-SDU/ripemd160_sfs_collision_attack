#include <iostream>
#include <bitset>
#include <vector>
#include <thread>
#include <atomic>
#include <string>
#include <cstdint>
#include <chrono>
#include <random>
#include <chrono>

using namespace std;

constexpr int s_left[48] = {11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 
    8, 7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12, 11, 
    13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5};

constexpr int s_right[48] = {8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6, 9,
                13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11, 9, 7, 15, 11, 8, 6, 6, 14, 12,
                13, 5, 14, 13, 13, 7, 5};

constexpr int message_order_left[48] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                        7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8, 
                        3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12};

constexpr int message_order_right[48] = {5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
                        6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2, 15, 5, 1, 3, 7, 14, 6,
                        9, 11, 8, 12, 2, 10, 0, 4, 13};

constexpr uint32_t K_left[5] = {0x00000000, 0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xa953fd4e};

constexpr uint32_t K_right[5] = {0x50a28be6, 0x5c4dd124, 0x6d703ef3, 0x7a6d76e9, 0x00000000};

vector<string>filterBool_left = {"XOR", "IFX", "ONZ", "IFZ", "ONX"};
vector<string>filterBool_right = {"ONX", "IFZ", "ONZ", "IFX", "XOR"};


uint32_t leftRotate(uint32_t n, int s) {
    n = n & 0xffffffff;
    return ((n << s) | (n >> (32 - s)) & 0xffffffff);
}

uint32_t rightRotate(uint32_t n, int s) {
    n = n & 0xffffffff;
    return ((n >> s) | (n << (32 - s)) & 0xffffffff);
}

uint32_t IFX(uint32_t x, uint32_t y, uint32_t z) {
    return ((x & y) ^ (~x & z));
}

uint32_t ONZ(uint32_t x, uint32_t y, uint32_t z) {
    return (x | ~y) ^ z;
}

uint32_t XOR(uint32_t x, uint32_t y, uint32_t z) {
    return x ^ y ^ z;
}

uint32_t IFZ(uint32_t x, uint32_t y, uint32_t z) {
    return ((x & z) ^ (y & (~z)));
}

uint32_t ONX(uint32_t x, uint32_t y, uint32_t z) {
    return (y | (~z)) ^ x;
}

vector<uint32_t> step_function_full(uint32_t x0, uint32_t x1, uint32_t x2, uint32_t x3, uint32_t x4, uint32_t m, int s, string fNa) {
    uint32_t b0;
    if (fNa == "XOR"){
        b0 = XOR(x4, x3, leftRotate(x2, 10)) & 0xffffffff;
    }
    else if (fNa == "IFX"){
        b0 = IFX(x4, x3, leftRotate(x2, 10)) & 0xffffffff;
    }
    else if (fNa == "ONZ"){
        b0 = ONZ(x4, x3, leftRotate(x2, 10)) & 0xffffffff;
    }
    else if (fNa == "IFZ") {
        b0 = IFZ(x4, x3, leftRotate(x2, 10)) & 0xffffffff;
    }
    else if (fNa == "ONX") {
        b0 = ONX(x4, x3, leftRotate(x2, 10)) & 0xffffffff;
    }
    uint32_t b1 = (b0 + leftRotate(x0, 10) + m) & 0xffffffff;
    return {x1, x2, x3, x4, (leftRotate(x1, 10) + leftRotate(b1, s)) & 0xffffffff};
}

vector<uint32_t> ripemd(vector<uint32_t> initial_IV, vector<uint32_t> state, vector<uint32_t> m, int step){
    vector<uint32_t> left(5,0);
    vector<uint32_t> right(5,0);
    for (int i = 0; i < 5; i++){
        left[i] = state[i];
        right[i] = state[i];
    }
    for (int i = 0; i < step; i++){
        left = step_function_full(left[0], left[1], left[2], left[3], left[4], m[message_order_left[i]] + K_left[i >> 4], s_left[i], filterBool_left[i >> 4]);
        // cout << i << " " << bitset<32>(left[4]) << endl;
        right = step_function_full(right[0], right[1], right[2], right[3], right[4], m[message_order_right[i]] + K_right[i >> 4], s_right[i], filterBool_right[i >> 4]);
    }

    // hash output
    vector<uint32_t> hash(5, 0);
    hash[0] = initial_IV[1] + left[3] + leftRotate(right[2], 10);
    hash[1] = initial_IV[2] + leftRotate(left[2], 10) + leftRotate(right[1], 10);
    hash[2] = initial_IV[3] + leftRotate(left[1], 10) + leftRotate(right[0], 10);
    hash[3] = initial_IV[4] + leftRotate(left[0], 10) + right[4];
    hash[4] = initial_IV[0] + left[4] + right[3];

    return hash;
}


int main() {
                                                                                                                                                                                                
    int step = 42;
    
    // colliding message pair2
    vector<uint32_t> initial_IV = {0b11100100011110000000110011010001,
        0b00111000111100110001001011100000,
        0b10110100110101011011011101010010,
        0b10010001111111110111100011010101,
        0b00110100010111010111010111101110};   

    uint32_t m[16] = {0b01111001111110010010100010101001,
        0b01101001011101111101011000101110,
        0b10000011010100111011101001100101,
        0b11100010111010001010111110011000,
        0b00000110101001101000111011111101,
        0b01001111111000000100001111110101,
        0b11101111110011001110111101111110,
        0b10011001110011101110100110100000,
        0b11000001011100000011111001011110,
        0b01100100111011100111111011001001,
        0b10101110011110101101011110110101,
        0b00000111100011010111011010010101,
        0b01101100111010110011110111111001,
        0b11001100111010001101001111110101,
        0b01010000000000010101000010001111,
        0b11101010111111110001010100101111};


    // X_-5 = h0 >>> 10; X_-4 = h4 >>> 10; X_-3 = h3 >>> 10; X_-2 = h2, X_-1 = h1
    vector<uint32_t> state_IV(5,0);
    state_IV[0] = rightRotate(initial_IV[0], 10);
    state_IV[1] = rightRotate(initial_IV[4], 10);
    state_IV[2] = rightRotate(initial_IV[3], 10);
    state_IV[3] = initial_IV[2];
    state_IV[4] = initial_IV[1];

    vector<uint32_t> m0(16, 0), m1(16, 0);


    // message pair
    for (int i = 0; i < 16; i++){
        if (i == 12){
            m0[i] = m[i];
            m1[i] = m[i] + pow(2,15);
        }
        else{
            m0[i] = m[i];
            m1[i] = m[i];
        } 
    }

    vector<uint32_t> hash0(5, 0), hash1(5, 0);
    hash0 = ripemd(initial_IV, state_IV, m0, step);
    hash1 = ripemd(initial_IV, state_IV, m1, step);
    
    cout << "CV0:" << endl;
    for (int i = 0; i < 5; i++) {
        cout << hex << initial_IV[i] << endl;
    }

    cout << endl << "m0: " << endl;
    for (int i = 0; i < 16; i++) {  
        cout << hex << m0[i] << endl;
    }

    cout << endl << "m1: " << endl;
    for (int i = 0; i < 16; i++) {  
        cout << hex << m1[i] << endl;
    }

    cout << endl << "hash0:" << endl;
    for (int i = 0; i < 5; i++) {  
        cout << hex << hash0[i] << endl;
    }


    cout << endl << "hash1:" << endl;
    for (int i = 0; i < 5; i++) {  
        cout << hex << hash1[i] << endl;
    }
}


// // colliding message pair1
// vector<uint32_t> initial_IV = {0b00011100010110010001011100110101,
//     0b01010000110000011000000101100011,
//     0b00011110000110100010001000111010,
//     0b10001110100011110011101010111011,
//     0b01111100011111001010111101101011};   

// uint32_t m[16] = {0b01111001111110010010100010101001,
//     0b01011111100001001100110011001101,
//     0b10000011010100111011101001100101,
//     0b11100010111010001010111110011000,
//     0b00000110101001101000111011111101,
//     0b01001111111000000100001111110101,
//     0b11101111110011001110111101111110,
//     0b11101011000110001100010011000111,
//     0b11000001011100000011111001011110,
//     0b01100100111011100111111011001001,
//     0b10101110011110101101011110110101,
//     0b00000111100011010111011010010101,
//     0b01101100111010110011110111111001,
//     0b01011111111110000100001000000101,
//     0b01010000000000010101000010001111,
//     0b11101010111111110001010100101111};



// // colliding message pair2
// vector<uint32_t> initial_IV = {0b11100100011110000000110011010001,
//     0b00111000111100110001001011100000,
//     0b10110100110101011011011101010010,
//     0b10010001111111110111100011010101,
//     0b00110100010111010111010111101110};   

// uint32_t m[16] = {0b01111001111110010010100010101001,
//     0b01101001011101111101011000101110,
//     0b10000011010100111011101001100101,
//     0b11100010111010001010111110011000,
//     0b00000110101001101000111011111101,
//     0b01001111111000000100001111110101,
//     0b11101111110011001110111101111110,
//     0b10011001110011101110100110100000,
//     0b11000001011100000011111001011110,
//     0b01100100111011100111111011001001,
//     0b10101110011110101101011110110101,
//     0b00000111100011010111011010010101,
//     0b01101100111010110011110111111001,
//     0b11001100111010001101001111110101,
//     0b01010000000000010101000010001111,
//     0b11101010111111110001010100101111};