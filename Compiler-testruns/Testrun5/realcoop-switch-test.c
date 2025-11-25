// VC Script Decompiler - Python (Structured)
// enter_ip: 0x-e70

#include <inc/sc_global.h>
#include <inc/sc_def.h>

// Data segment
// Jump table at data[2] with 128 entries
void* jt_2[128] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x0,  // case 2: jump to L0
    (void*)0x0,  // case 3: jump to L0
    (void*)0x0,  // case 4: jump to L0
    (void*)0x0,  // case 5: jump to L0
    (void*)0x0,  // case 6: jump to L0
    (void*)0x0,  // case 7: jump to L0
    (void*)0x0,  // case 8: jump to L0
    (void*)0x0,  // case 9: jump to L0
    (void*)0x0,  // case 10: jump to L0
    (void*)0x0,  // case 11: jump to L0
    (void*)0x0,  // case 12: jump to L0
    (void*)0x0,  // case 13: jump to L0
    (void*)0x0,  // case 14: jump to L0
    (void*)0x0,  // case 15: jump to L0
    (void*)0x0,  // case 16: jump to L0
    (void*)0x0,  // case 17: jump to L0
    (void*)0x0,  // case 18: jump to L0
    (void*)0x0,  // case 19: jump to L0
    (void*)0x0,  // case 20: jump to L0
    (void*)0x0,  // case 21: jump to L0
    (void*)0x0,  // case 22: jump to L0
    (void*)0x0,  // case 23: jump to L0
    (void*)0x0,  // case 24: jump to L0
    (void*)0x0,  // case 25: jump to L0
    (void*)0x0,  // case 26: jump to L0
    (void*)0x0,  // case 27: jump to L0
    (void*)0x0,  // case 28: jump to L0
    (void*)0x0,  // case 29: jump to L0
    (void*)0x0,  // case 30: jump to L0
    (void*)0x0,  // case 31: jump to L0
    (void*)0x0,  // case 32: jump to L0
    (void*)0x0,  // case 33: jump to L0
    (void*)0x0,  // case 34: jump to L0
    (void*)0x0,  // case 35: jump to L0
    (void*)0x0,  // case 36: jump to L0
    (void*)0x0,  // case 37: jump to L0
    (void*)0x0,  // case 38: jump to L0
    (void*)0x0,  // case 39: jump to L0
    (void*)0x0,  // case 40: jump to L0
    (void*)0x0,  // case 41: jump to L0
    (void*)0x0,  // case 42: jump to L0
    (void*)0x0,  // case 43: jump to L0
    (void*)0x0,  // case 44: jump to L0
    (void*)0x0,  // case 45: jump to L0
    (void*)0x0,  // case 46: jump to L0
    (void*)0x0,  // case 47: jump to L0
    (void*)0x0,  // case 48: jump to L0
    (void*)0x0,  // case 49: jump to L0
    (void*)0x0,  // case 50: jump to L0
    (void*)0x0,  // case 51: jump to L0
    (void*)0x0,  // case 52: jump to L0
    (void*)0x0,  // case 53: jump to L0
    (void*)0x0,  // case 54: jump to L0
    (void*)0x0,  // case 55: jump to L0
    (void*)0x0,  // case 56: jump to L0
    (void*)0x0,  // case 57: jump to L0
    (void*)0x0,  // case 58: jump to L0
    (void*)0x0,  // case 59: jump to L0
    (void*)0x0,  // case 60: jump to L0
    (void*)0x0,  // case 61: jump to L0
    (void*)0x0,  // case 62: jump to L0
    (void*)0x0,  // case 63: jump to L0
    (void*)0x0,  // case 64: jump to L0
    (void*)0x0,  // case 65: jump to L0
    (void*)0x0,  // case 66: jump to L0
    (void*)0x0,  // case 67: jump to L0
    (void*)0x0,  // case 68: jump to L0
    (void*)0x0,  // case 69: jump to L0
    (void*)0x0,  // case 70: jump to L0
    (void*)0x0,  // case 71: jump to L0
    (void*)0x0,  // case 72: jump to L0
    (void*)0x0,  // case 73: jump to L0
    (void*)0x0,  // case 74: jump to L0
    (void*)0x0,  // case 75: jump to L0
    (void*)0x0,  // case 76: jump to L0
    (void*)0x0,  // case 77: jump to L0
    (void*)0x0,  // case 78: jump to L0
    (void*)0x0,  // case 79: jump to L0
    (void*)0x0,  // case 80: jump to L0
    (void*)0x0,  // case 81: jump to L0
    (void*)0x0,  // case 82: jump to L0
    (void*)0x0,  // case 83: jump to L0
    (void*)0x0,  // case 84: jump to L0
    (void*)0x0,  // case 85: jump to L0
    (void*)0x0,  // case 86: jump to L0
    (void*)0x0,  // case 87: jump to L0
    (void*)0x0,  // case 88: jump to L0
    (void*)0x0,  // case 89: jump to L0
    (void*)0x0,  // case 90: jump to L0
    (void*)0x0,  // case 91: jump to L0
    (void*)0x0,  // case 92: jump to L0
    (void*)0x0,  // case 93: jump to L0
    (void*)0x0,  // case 94: jump to L0
    (void*)0x0,  // case 95: jump to L0
    (void*)0x0,  // case 96: jump to L0
    (void*)0x0,  // case 97: jump to L0
    (void*)0x0,  // case 98: jump to L0
    (void*)0x0,  // case 99: jump to L0
    (void*)0x0,  // case 100: jump to L0
    (void*)0x0,  // case 101: jump to L0
    (void*)0x0,  // case 102: jump to L0
    (void*)0x0,  // case 103: jump to L0
    (void*)0x0,  // case 104: jump to L0
    (void*)0x0,  // case 105: jump to L0
    (void*)0x0,  // case 106: jump to L0
    (void*)0x0,  // case 107: jump to L0
    (void*)0x0,  // case 108: jump to L0
    (void*)0x0,  // case 109: jump to L0
    (void*)0x0,  // case 110: jump to L0
    (void*)0x0,  // case 111: jump to L0
    (void*)0x0,  // case 112: jump to L0
    (void*)0x0,  // case 113: jump to L0
    (void*)0x0,  // case 114: jump to L0
    (void*)0x0,  // case 115: jump to L0
    (void*)0x0,  // case 116: jump to L0
    (void*)0x0,  // case 117: jump to L0
    (void*)0x0,  // case 118: jump to L0
    (void*)0x0,  // case 119: jump to L0
    (void*)0x0,  // case 120: jump to L0
    (void*)0x0,  // case 121: jump to L0
    (void*)0x0,  // case 122: jump to L0
    (void*)0x0,  // case 123: jump to L0
    (void*)0x0,  // case 124: jump to L0
    (void*)0x0,  // case 125: jump to L0
    (void*)0x0,  // case 126: jump to L0
    (void*)0x1,  // case 127: jump to L1
};

// Jump table at data[131] with 15 entries
void* jt_131[15] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x0,  // case 2: jump to L0
    (void*)0x0,  // case 3: jump to L0
    (void*)0x0,  // case 4: jump to L0
    (void*)0x0,  // case 5: jump to L0
    (void*)0x0,  // case 6: jump to L0
    (void*)0x0,  // case 7: jump to L0
    (void*)0x0,  // case 8: jump to L0
    (void*)0x0,  // case 9: jump to L0
    (void*)0x0,  // case 10: jump to L0
    (void*)0x0,  // case 11: jump to L0
    (void*)0x0,  // case 12: jump to L0
    (void*)0x0,  // case 13: jump to L0
    (void*)0x40,  // case 14: jump to L64
};

// Jump table at data[147] with 20 entries
void* jt_147[20] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x10,  // case 1: jump to L16
    (void*)0x10,  // case 2: jump to L16
    (void*)0x1,  // case 3: jump to L1
    (void*)0x0,  // case 4: jump to L0
    (void*)0x10,  // case 5: jump to L16
    (void*)0x2,  // case 6: jump to L2
    (void*)0x0,  // case 7: jump to L0
    (void*)0x10,  // case 8: jump to L16
    (void*)0x3,  // case 9: jump to L3
    (void*)0x0,  // case 10: jump to L0
    (void*)0x10,  // case 11: jump to L16
    (void*)0x4,  // case 12: jump to L4
    (void*)0x0,  // case 13: jump to L0
    (void*)0x10,  // case 14: jump to L16
    (void*)0x5,  // case 15: jump to L5
    (void*)0x0,  // case 16: jump to L0
    (void*)0x1,  // case 17: jump to L1
    (void*)0x0,  // case 18: jump to L0
    (void*)0x1,  // case 19: jump to L1
};

// Jump table at data[177] with 8 entries
void* jt_177[8] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
    (void*)0x0,  // case 3: jump to L0
    (void*)0x0,  // case 4: jump to L0
    (void*)0x0,  // case 5: jump to L0
    (void*)0x1,  // case 6: jump to L1
    (void*)0x0,  // case 7: jump to L0
};

// Jump table at data[196] with 91 entries
void* jt_196[91] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x5,  // case 1: jump to L5
    (void*)0x1,  // case 2: jump to L1
    (void*)0x1,  // case 3: jump to L1
    (void*)0x1,  // case 4: jump to L1
    (void*)0x64,  // case 5: jump to L100
    (void*)0x5,  // case 6: jump to L5
    (void*)0x1,  // case 7: jump to L1
    (void*)0x2,  // case 8: jump to L2
    (void*)0x1,  // case 9: jump to L1
    (void*)0x64,  // case 10: jump to L100
    (void*)0x1,  // case 11: jump to L1
    (void*)0x1,  // case 12: jump to L1
    (void*)0x5,  // case 13: jump to L5
    (void*)0x1,  // case 14: jump to L1
    (void*)0x64,  // case 15: jump to L100
    (void*)0x1,  // case 16: jump to L1
    (void*)0x1,  // case 17: jump to L1
    (void*)0x5,  // case 18: jump to L5
    (void*)0x2,  // case 19: jump to L2
    (void*)0x64,  // case 20: jump to L100
    (void*)0x1,  // case 21: jump to L1
    (void*)0x1,  // case 22: jump to L1
    (void*)0x5,  // case 23: jump to L5
    (void*)0x3,  // case 24: jump to L3
    (void*)0x64,  // case 25: jump to L100
    (void*)0x1,  // case 26: jump to L1
    (void*)0x1,  // case 27: jump to L1
    (void*)0x5,  // case 28: jump to L5
    (void*)0x4,  // case 29: jump to L4
    (void*)0x64,  // case 30: jump to L100
    (void*)0x1,  // case 31: jump to L1
    (void*)0x1,  // case 32: jump to L1
    (void*)0x6,  // case 33: jump to L6
    (void*)0x1,  // case 34: jump to L1
    (void*)0x64,  // case 35: jump to L100
    (void*)0x1,  // case 36: jump to L1
    (void*)0x1,  // case 37: jump to L1
    (void*)0x6,  // case 38: jump to L6
    (void*)0x2,  // case 39: jump to L2
    (void*)0x64,  // case 40: jump to L100
    (void*)0x1,  // case 41: jump to L1
    (void*)0x1,  // case 42: jump to L1
    (void*)0x6,  // case 43: jump to L6
    (void*)0x3,  // case 44: jump to L3
    (void*)0x64,  // case 45: jump to L100
    (void*)0x1,  // case 46: jump to L1
    (void*)0x1,  // case 47: jump to L1
    (void*)0x6,  // case 48: jump to L6
    (void*)0x4,  // case 49: jump to L4
    (void*)0x64,  // case 50: jump to L100
    (void*)0x1,  // case 51: jump to L1
    (void*)0x1,  // case 52: jump to L1
    (void*)0x8,  // case 53: jump to L8
    (void*)0x1,  // case 54: jump to L1
    (void*)0x64,  // case 55: jump to L100
    (void*)0x1,  // case 56: jump to L1
    (void*)0x1,  // case 57: jump to L1
    (void*)0x8,  // case 58: jump to L8
    (void*)0x2,  // case 59: jump to L2
    (void*)0x64,  // case 60: jump to L100
    (void*)0x1,  // case 61: jump to L1
    (void*)0x1,  // case 62: jump to L1
    (void*)0x8,  // case 63: jump to L8
    (void*)0x3,  // case 64: jump to L3
    (void*)0x64,  // case 65: jump to L100
    (void*)0x1,  // case 66: jump to L1
    (void*)0x1,  // case 67: jump to L1
    (void*)0x8,  // case 68: jump to L8
    (void*)0x4,  // case 69: jump to L4
    (void*)0x64,  // case 70: jump to L100
    (void*)0x1,  // case 71: jump to L1
    (void*)0x1,  // case 72: jump to L1
    (void*)0x9,  // case 73: jump to L9
    (void*)0x1,  // case 74: jump to L1
    (void*)0x64,  // case 75: jump to L100
    (void*)0x1,  // case 76: jump to L1
    (void*)0x1,  // case 77: jump to L1
    (void*)0x9,  // case 78: jump to L9
    (void*)0x2,  // case 79: jump to L2
    (void*)0x64,  // case 80: jump to L100
    (void*)0x1,  // case 81: jump to L1
    (void*)0x1,  // case 82: jump to L1
    (void*)0x9,  // case 83: jump to L9
    (void*)0x3,  // case 84: jump to L3
    (void*)0x64,  // case 85: jump to L100
    (void*)0x1,  // case 86: jump to L1
    (void*)0x1,  // case 87: jump to L1
    (void*)0x9,  // case 88: jump to L9
    (void*)0x4,  // case 89: jump to L4
    (void*)0x64,  // case 90: jump to L100
};

// Jump table at data[290] with 5 entries
void* jt_290[5] = {
    (void*)0x2,  // case 0: jump to L2
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
    (void*)0x1,  // case 3: jump to L1
    (void*)0x64,  // case 4: jump to L100
};

// Jump table at data[300] with 7 entries
void* jt_300[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x2,  // case 3: jump to L2
    (void*)0x1,  // case 4: jump to L1
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[312] with 7 entries
void* jt_312[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x5,  // case 3: jump to L5
    (void*)0x1,  // case 4: jump to L1
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[324] with 7 entries
void* jt_324[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x5,  // case 3: jump to L5
    (void*)0x2,  // case 4: jump to L2
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[336] with 7 entries
void* jt_336[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x5,  // case 3: jump to L5
    (void*)0x3,  // case 4: jump to L3
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[348] with 7 entries
void* jt_348[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x5,  // case 3: jump to L5
    (void*)0x4,  // case 4: jump to L4
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[360] with 21 entries
void* jt_360[21] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x1,  // case 3: jump to L1
    (void*)0x1,  // case 4: jump to L1
    (void*)0x1,  // case 5: jump to L1
    (void*)0x1,  // case 6: jump to L1
    (void*)0x2,  // case 7: jump to L2
    (void*)0x1,  // case 8: jump to L1
    (void*)0x1,  // case 9: jump to L1
    (void*)0x5,  // case 10: jump to L5
    (void*)0x1,  // case 11: jump to L1
    (void*)0x1,  // case 12: jump to L1
    (void*)0x5,  // case 13: jump to L5
    (void*)0x2,  // case 14: jump to L2
    (void*)0x1,  // case 15: jump to L1
    (void*)0x5,  // case 16: jump to L5
    (void*)0x3,  // case 17: jump to L3
    (void*)0x1,  // case 18: jump to L1
    (void*)0x5,  // case 19: jump to L5
    (void*)0x4,  // case 20: jump to L4
};

// Jump table at data[384] with 5 entries
void* jt_384[5] = {
    (void*)0x2,  // case 0: jump to L2
    (void*)0x6,  // case 1: jump to L6
    (void*)0x1,  // case 2: jump to L1
    (void*)0x1,  // case 3: jump to L1
    (void*)0x64,  // case 4: jump to L100
};

// Jump table at data[394] with 7 entries
void* jt_394[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x6,  // case 3: jump to L6
    (void*)0x2,  // case 4: jump to L2
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[406] with 7 entries
void* jt_406[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x6,  // case 3: jump to L6
    (void*)0x3,  // case 4: jump to L3
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[418] with 7 entries
void* jt_418[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x6,  // case 3: jump to L6
    (void*)0x4,  // case 4: jump to L4
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[430] with 15 entries
void* jt_430[15] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x1,  // case 3: jump to L1
    (void*)0x6,  // case 4: jump to L6
    (void*)0x1,  // case 5: jump to L1
    (void*)0x1,  // case 6: jump to L1
    (void*)0x6,  // case 7: jump to L6
    (void*)0x2,  // case 8: jump to L2
    (void*)0x1,  // case 9: jump to L1
    (void*)0x6,  // case 10: jump to L6
    (void*)0x3,  // case 11: jump to L3
    (void*)0x1,  // case 12: jump to L1
    (void*)0x6,  // case 13: jump to L6
    (void*)0x4,  // case 14: jump to L4
};

// Jump table at data[448] with 5 entries
void* jt_448[5] = {
    (void*)0x2,  // case 0: jump to L2
    (void*)0x8,  // case 1: jump to L8
    (void*)0x1,  // case 2: jump to L1
    (void*)0x1,  // case 3: jump to L1
    (void*)0x64,  // case 4: jump to L100
};

// Jump table at data[458] with 7 entries
void* jt_458[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x8,  // case 3: jump to L8
    (void*)0x2,  // case 4: jump to L2
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[470] with 7 entries
void* jt_470[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x8,  // case 3: jump to L8
    (void*)0x3,  // case 4: jump to L3
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[482] with 7 entries
void* jt_482[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x8,  // case 3: jump to L8
    (void*)0x4,  // case 4: jump to L4
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[494] with 15 entries
void* jt_494[15] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x1,  // case 3: jump to L1
    (void*)0x8,  // case 4: jump to L8
    (void*)0x1,  // case 5: jump to L1
    (void*)0x1,  // case 6: jump to L1
    (void*)0x8,  // case 7: jump to L8
    (void*)0x2,  // case 8: jump to L2
    (void*)0x1,  // case 9: jump to L1
    (void*)0x8,  // case 10: jump to L8
    (void*)0x3,  // case 11: jump to L3
    (void*)0x1,  // case 12: jump to L1
    (void*)0x8,  // case 13: jump to L8
    (void*)0x4,  // case 14: jump to L4
};

// Jump table at data[511] with 5 entries
void* jt_511[5] = {
    (void*)0x2,  // case 0: jump to L2
    (void*)0x9,  // case 1: jump to L9
    (void*)0x1,  // case 2: jump to L1
    (void*)0x1,  // case 3: jump to L1
    (void*)0x64,  // case 4: jump to L100
};

// Jump table at data[521] with 7 entries
void* jt_521[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x9,  // case 3: jump to L9
    (void*)0x2,  // case 4: jump to L2
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[533] with 7 entries
void* jt_533[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x9,  // case 3: jump to L9
    (void*)0x3,  // case 4: jump to L3
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[545] with 7 entries
void* jt_545[7] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x9,  // case 3: jump to L9
    (void*)0x4,  // case 4: jump to L4
    (void*)0x1,  // case 5: jump to L1
    (void*)0x64,  // case 6: jump to L100
};

// Jump table at data[557] with 38 entries
void* jt_557[38] = {
    (void*)0x5,  // case 0: jump to L5
    (void*)0x1,  // case 1: jump to L1
    (void*)0x0,  // case 2: jump to L0
    (void*)0x1,  // case 3: jump to L1
    (void*)0x9,  // case 4: jump to L9
    (void*)0x1,  // case 5: jump to L1
    (void*)0x1,  // case 6: jump to L1
    (void*)0x9,  // case 7: jump to L9
    (void*)0x2,  // case 8: jump to L2
    (void*)0x1,  // case 9: jump to L1
    (void*)0x9,  // case 10: jump to L9
    (void*)0x3,  // case 11: jump to L3
    (void*)0x1,  // case 12: jump to L1
    (void*)0x9,  // case 13: jump to L9
    (void*)0x4,  // case 14: jump to L4
    (void*)0x1f4,  // case 15: jump to L500
    (void*)0x0,  // case 16: jump to L0
    (void*)0x1,  // case 17: jump to L1
    (void*)0x14,  // case 18: jump to L20
    (void*)0x1,  // case 19: jump to L1
    (void*)0x14,  // case 20: jump to L20
    (void*)0x0,  // case 21: jump to L0
    (void*)0x1,  // case 22: jump to L1
    (void*)0x1,  // case 23: jump to L1
    (void*)0x1,  // case 24: jump to L1
    (void*)0x0,  // case 25: jump to L0
    (void*)0x0,  // case 26: jump to L0
    (void*)0x14,  // case 27: jump to L20
    (void*)0x0,  // case 28: jump to L0
    (void*)0x14,  // case 29: jump to L20
    (void*)0x1,  // case 30: jump to L1
    (void*)0x1,  // case 31: jump to L1
    (void*)0x1,  // case 32: jump to L1
    (void*)0x1,  // case 33: jump to L1
    (void*)0x0,  // case 34: jump to L0
    (void*)0x40,  // case 35: jump to L64
    (void*)0x0,  // case 36: jump to L0
    (void*)0x0,  // case 37: jump to L0
};

// Jump table at data[596] with 54 entries
void* jt_596[54] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x41,  // case 1: jump to L65
    (void*)0x10,  // case 2: jump to L16
    (void*)0x0,  // case 3: jump to L0
    (void*)0x10,  // case 4: jump to L16
    (void*)0x1,  // case 5: jump to L1
    (void*)0x10,  // case 6: jump to L16
    (void*)0x2,  // case 7: jump to L2
    (void*)0x1,  // case 8: jump to L1
    (void*)0x1,  // case 9: jump to L1
    (void*)0x7,  // case 10: jump to L7
    (void*)0x3,  // case 11: jump to L3
    (void*)0x1,  // case 12: jump to L1
    (void*)0x1,  // case 13: jump to L1
    (void*)0x40,  // case 14: jump to L64
    (void*)0x1,  // case 15: jump to L1
    (void*)0x3df,  // case 16: jump to L991
    (void*)0x0,  // case 17: jump to L0
    (void*)0x1,  // case 18: jump to L1
    (void*)0x0,  // case 19: jump to L0
    (void*)0x2,  // case 20: jump to L2
    (void*)0x0,  // case 21: jump to L0
    (void*)0x3,  // case 22: jump to L3
    (void*)0x0,  // case 23: jump to L0
    (void*)0x4,  // case 24: jump to L4
    (void*)0x0,  // case 25: jump to L0
    (void*)0x5,  // case 26: jump to L5
    (void*)0x0,  // case 27: jump to L0
    (void*)0x6,  // case 28: jump to L6
    (void*)0x0,  // case 29: jump to L0
    (void*)0x7,  // case 30: jump to L7
    (void*)0x0,  // case 31: jump to L0
    (void*)0x8,  // case 32: jump to L8
    (void*)0x0,  // case 33: jump to L0
    (void*)0x9,  // case 34: jump to L9
    (void*)0x0,  // case 35: jump to L0
    (void*)0x1,  // case 36: jump to L1
    (void*)0x1,  // case 37: jump to L1
    (void*)0x0,  // case 38: jump to L0
    (void*)0x1,  // case 39: jump to L1
    (void*)0x0,  // case 40: jump to L0
    (void*)0x0,  // case 41: jump to L0
    (void*)0x1,  // case 42: jump to L1
    (void*)0x2,  // case 43: jump to L2
    (void*)0x0,  // case 44: jump to L0
    (void*)0x1,  // case 45: jump to L1
    (void*)0x40,  // case 46: jump to L64
    (void*)0x0,  // case 47: jump to L0
    (void*)0x1,  // case 48: jump to L1
    (void*)0x0,  // case 49: jump to L0
    (void*)0x1,  // case 50: jump to L1
    (void*)0x0,  // case 51: jump to L0
    (void*)0x1,  // case 52: jump to L1
    (void*)0x0,  // case 53: jump to L0
};

// Jump table at data[658] with 3 entries
void* jt_658[3] = {
    (void*)0x9,  // case 0: jump to L9
    (void*)0x3a,  // case 1: jump to L58
    (void*)0x40,  // case 2: jump to L64
};

// Jump table at data[665] with 3 entries
void* jt_665[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x10,  // case 1: jump to L16
    (void*)0x10,  // case 2: jump to L16
};

// Jump table at data[698] with 3 entries
void* jt_698[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x10,  // case 1: jump to L16
    (void*)0x10,  // case 2: jump to L16
};

// Jump table at data[702] with 6 entries
void* jt_702[6] = {
    (void*)0x10,  // case 0: jump to L16
    (void*)0x0,  // case 1: jump to L0
    (void*)0x0,  // case 2: jump to L0
    (void*)0x3df,  // case 3: jump to L991
    (void*)0x1,  // case 4: jump to L1
    (void*)0x40,  // case 5: jump to L64
};

// Jump table at data[720] with 5 entries
void* jt_720[5] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x10,  // case 1: jump to L16
    (void*)0x10,  // case 2: jump to L16
    (void*)0x0,  // case 3: jump to L0
    (void*)0x10,  // case 4: jump to L16
};

// Jump table at data[726] with 28 entries
void* jt_726[28] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x5,  // case 1: jump to L5
    (void*)0x1,  // case 2: jump to L1
    (void*)0x1,  // case 3: jump to L1
    (void*)0x5,  // case 4: jump to L5
    (void*)0x2,  // case 5: jump to L2
    (void*)0x1,  // case 6: jump to L1
    (void*)0x5,  // case 7: jump to L5
    (void*)0x3,  // case 8: jump to L3
    (void*)0x1,  // case 9: jump to L1
    (void*)0x5,  // case 10: jump to L5
    (void*)0x4,  // case 11: jump to L4
    (void*)0x1,  // case 12: jump to L1
    (void*)0x6,  // case 13: jump to L6
    (void*)0x1,  // case 14: jump to L1
    (void*)0x1,  // case 15: jump to L1
    (void*)0x6,  // case 16: jump to L6
    (void*)0x2,  // case 17: jump to L2
    (void*)0x1,  // case 18: jump to L1
    (void*)0x6,  // case 19: jump to L6
    (void*)0x3,  // case 20: jump to L3
    (void*)0x1,  // case 21: jump to L1
    (void*)0x6,  // case 22: jump to L6
    (void*)0x4,  // case 23: jump to L4
    (void*)0x0,  // case 24: jump to L0
    (void*)0x3e0,  // case 25: jump to L992
    (void*)0x1,  // case 26: jump to L1
    (void*)0x40,  // case 27: jump to L64
};

// Jump table at data[761] with 5 entries
void* jt_761[5] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x10,  // case 1: jump to L16
    (void*)0x10,  // case 2: jump to L16
    (void*)0x0,  // case 3: jump to L0
    (void*)0x10,  // case 4: jump to L16
};

// Jump table at data[767] with 3 entries
void* jt_767[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x3e1,  // case 2: jump to L993
};

// Jump table at data[771] with 5 entries
void* jt_771[5] = {
    (void*)0x14,  // case 0: jump to L20
    (void*)0x0,  // case 1: jump to L0
    (void*)0x3e1,  // case 2: jump to L993
    (void*)0x1,  // case 3: jump to L1
    (void*)0x40,  // case 4: jump to L64
};

// Jump table at data[780] with 5 entries
void* jt_780[5] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x10,  // case 1: jump to L16
    (void*)0x10,  // case 2: jump to L16
    (void*)0x0,  // case 3: jump to L0
    (void*)0x10,  // case 4: jump to L16
};

// Jump table at data[786] with 5 entries
void* jt_786[5] = {
    (void*)0x2,  // case 0: jump to L2
    (void*)0x0,  // case 1: jump to L0
    (void*)0x3e2,  // case 2: jump to L994
    (void*)0x1,  // case 3: jump to L1
    (void*)0x40,  // case 4: jump to L64
};

// Jump table at data[795] with 5 entries
void* jt_795[5] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x10,  // case 1: jump to L16
    (void*)0x10,  // case 2: jump to L16
    (void*)0x0,  // case 3: jump to L0
    (void*)0x10,  // case 4: jump to L16
};

// Jump table at data[801] with 5 entries
void* jt_801[5] = {
    (void*)0x3,  // case 0: jump to L3
    (void*)0x0,  // case 1: jump to L0
    (void*)0x3e3,  // case 2: jump to L995
    (void*)0x1,  // case 3: jump to L1
    (void*)0x40,  // case 4: jump to L64
};

// Jump table at data[810] with 5 entries
void* jt_810[5] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x10,  // case 1: jump to L16
    (void*)0x10,  // case 2: jump to L16
    (void*)0x0,  // case 3: jump to L0
    (void*)0x10,  // case 4: jump to L16
};

// Jump table at data[820] with 11 entries
void* jt_820[11] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x2,  // case 1: jump to L2
    (void*)0x1,  // case 2: jump to L1
    (void*)0x0,  // case 3: jump to L0
    (void*)0x2,  // case 4: jump to L2
    (void*)0x2,  // case 5: jump to L2
    (void*)0x4,  // case 6: jump to L4
    (void*)0x0,  // case 7: jump to L0
    (void*)0x3e4,  // case 8: jump to L996
    (void*)0x1,  // case 9: jump to L1
    (void*)0x40,  // case 10: jump to L64
};

// Jump table at data[835] with 5 entries
void* jt_835[5] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x10,  // case 1: jump to L16
    (void*)0x10,  // case 2: jump to L16
    (void*)0x0,  // case 3: jump to L0
    (void*)0x10,  // case 4: jump to L16
};

// Jump table at data[841] with 4 entries
void* jt_841[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x3e5,  // case 1: jump to L997
    (void*)0x1,  // case 2: jump to L1
    (void*)0x40,  // case 3: jump to L64
};

// Jump table at data[849] with 5 entries
void* jt_849[5] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x10,  // case 1: jump to L16
    (void*)0x10,  // case 2: jump to L16
    (void*)0x0,  // case 3: jump to L0
    (void*)0x10,  // case 4: jump to L16
};

// Jump table at data[855] with 20 entries
void* jt_855[20] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x3,  // case 1: jump to L3
    (void*)0x1,  // case 2: jump to L1
    (void*)0x0,  // case 3: jump to L0
    (void*)0x0,  // case 4: jump to L0
    (void*)0x0,  // case 5: jump to L0
    (void*)0x0,  // case 6: jump to L0
    (void*)0x0,  // case 7: jump to L0
    (void*)0x0,  // case 8: jump to L0
    (void*)0x3,  // case 9: jump to L3
    (void*)0x0,  // case 10: jump to L0
    (void*)0x2,  // case 11: jump to L2
    (void*)0x0,  // case 12: jump to L0
    (void*)0x4,  // case 13: jump to L4
    (void*)0x30,  // case 14: jump to L48
    (void*)0x4,  // case 15: jump to L4
    (void*)0x30,  // case 16: jump to L48
    (void*)0x4,  // case 17: jump to L4
    (void*)0x1,  // case 18: jump to L1
    (void*)0x1,  // case 19: jump to L1
};

// Jump table at data[876] with 6 entries
void* jt_876[6] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x0,  // case 2: jump to L0
    (void*)0x8,  // case 3: jump to L8
    (void*)0x40,  // case 4: jump to L64
    (void*)0x0,  // case 5: jump to L0
};

// Jump table at data[883] with 10 entries
void* jt_883[10] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x0,  // case 2: jump to L0
    (void*)0x0,  // case 3: jump to L0
    (void*)0x0,  // case 4: jump to L0
    (void*)0x0,  // case 5: jump to L0
    (void*)0x10,  // case 6: jump to L16
    (void*)0x1,  // case 7: jump to L1
    (void*)0x10,  // case 8: jump to L16
    (void*)0x1,  // case 9: jump to L1
};

// Jump table at data[900] with 35 entries
void* jt_900[35] = {
    (void*)0x10,  // case 0: jump to L16
    (void*)0x2,  // case 1: jump to L2
    (void*)0x1,  // case 2: jump to L1
    (void*)0x10,  // case 3: jump to L16
    (void*)0x4,  // case 4: jump to L4
    (void*)0x10,  // case 5: jump to L16
    (void*)0x0,  // case 6: jump to L0
    (void*)0x10,  // case 7: jump to L16
    (void*)0x1,  // case 8: jump to L1
    (void*)0x0,  // case 9: jump to L0
    (void*)0x1,  // case 10: jump to L1
    (void*)0x10,  // case 11: jump to L16
    (void*)0x1,  // case 12: jump to L1
    (void*)0x10,  // case 13: jump to L16
    (void*)0x1,  // case 14: jump to L1
    (void*)0x0,  // case 15: jump to L0
    (void*)0x1,  // case 16: jump to L1
    (void*)0x10,  // case 17: jump to L16
    (void*)0x0,  // case 18: jump to L0
    (void*)0x10,  // case 19: jump to L16
    (void*)0x2,  // case 20: jump to L2
    (void*)0x10,  // case 21: jump to L16
    (void*)0x1,  // case 22: jump to L1
    (void*)0x0,  // case 23: jump to L0
    (void*)0x1,  // case 24: jump to L1
    (void*)0x10,  // case 25: jump to L16
    (void*)0x1,  // case 26: jump to L1
    (void*)0x10,  // case 27: jump to L16
    (void*)0x2,  // case 28: jump to L2
    (void*)0x10,  // case 29: jump to L16
    (void*)0x1,  // case 30: jump to L1
    (void*)0x0,  // case 31: jump to L0
    (void*)0x1,  // case 32: jump to L1
    (void*)0x1,  // case 33: jump to L1
    (void*)0x3,  // case 34: jump to L3
};

// Jump table at data[945] with 4 entries
void* jt_945[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x4,  // case 1: jump to L4
    (void*)0x5,  // case 2: jump to L5
    (void*)0x3,  // case 3: jump to L3
};

// Jump table at data[951] with 18 entries
void* jt_951[18] = {
    (void*)0x2,  // case 0: jump to L2
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
    (void*)0x0,  // case 3: jump to L0
    (void*)0x1,  // case 4: jump to L1
    (void*)0x7,  // case 5: jump to L7
    (void*)0x0,  // case 6: jump to L0
    (void*)0x2,  // case 7: jump to L2
    (void*)0x3df,  // case 8: jump to L991
    (void*)0x3e0,  // case 9: jump to L992
    (void*)0x3e1,  // case 10: jump to L993
    (void*)0x3e2,  // case 11: jump to L994
    (void*)0x3e3,  // case 12: jump to L995
    (void*)0x3e4,  // case 13: jump to L996
    (void*)0x3e5,  // case 14: jump to L997
    (void*)0x0,  // case 15: jump to L0
    (void*)0x0,  // case 16: jump to L0
    (void*)0x2,  // case 17: jump to L2
};

// Jump table at data[980] with 10 entries
void* jt_980[10] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x0,  // case 3: jump to L0
    (void*)0x0,  // case 4: jump to L0
    (void*)0x0,  // case 5: jump to L0
    (void*)0x0,  // case 6: jump to L0
    (void*)0x0,  // case 7: jump to L0
    (void*)0x4,  // case 8: jump to L4
    (void*)0x2,  // case 9: jump to L2
};

// Jump table at data[996] with 5 entries
void* jt_996[5] = {
    (void*)0x2,  // case 0: jump to L2
    (void*)0x2,  // case 1: jump to L2
    (void*)0x0,  // case 2: jump to L0
    (void*)0x4,  // case 3: jump to L4
    (void*)0x2,  // case 4: jump to L2
};

// Jump table at data[1008] with 3 entries
void* jt_1008[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1012] with 4 entries
void* jt_1012[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x2,  // case 3: jump to L2
};

// Jump table at data[1017] with 4 entries
void* jt_1017[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x3,  // case 3: jump to L3
};

// Jump table at data[1022] with 4 entries
void* jt_1022[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x4,  // case 3: jump to L4
};

// Jump table at data[1027] with 4 entries
void* jt_1027[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x5,  // case 3: jump to L5
};

// Jump table at data[1032] with 6 entries
void* jt_1032[6] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x1f4,  // case 1: jump to L500
    (void*)0x3df,  // case 2: jump to L991
    (void*)0x0,  // case 3: jump to L0
    (void*)0x4,  // case 4: jump to L4
    (void*)0x2,  // case 5: jump to L2
};

// Jump table at data[1045] with 3 entries
void* jt_1045[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1049] with 3 entries
void* jt_1049[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x2,  // case 1: jump to L2
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1053] with 3 entries
void* jt_1053[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1057] with 4 entries
void* jt_1057[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x2,  // case 3: jump to L2
};

// Jump table at data[1062] with 4 entries
void* jt_1062[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x3,  // case 3: jump to L3
};

// Jump table at data[1067] with 4 entries
void* jt_1067[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x4,  // case 3: jump to L4
};

// Jump table at data[1072] with 4 entries
void* jt_1072[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x5,  // case 3: jump to L5
};

// Jump table at data[1077] with 5 entries
void* jt_1077[5] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3e0,  // case 1: jump to L992
    (void*)0x0,  // case 2: jump to L0
    (void*)0x4,  // case 3: jump to L4
    (void*)0x2,  // case 4: jump to L2
};

// Jump table at data[1089] with 3 entries
void* jt_1089[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1093] with 3 entries
void* jt_1093[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x2,  // case 1: jump to L2
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1097] with 3 entries
void* jt_1097[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3,  // case 1: jump to L3
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1101] with 3 entries
void* jt_1101[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x4,  // case 1: jump to L4
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1105] with 3 entries
void* jt_1105[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1109] with 4 entries
void* jt_1109[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x2,  // case 3: jump to L2
};

// Jump table at data[1114] with 4 entries
void* jt_1114[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x3,  // case 3: jump to L3
};

// Jump table at data[1119] with 4 entries
void* jt_1119[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x4,  // case 3: jump to L4
};

// Jump table at data[1124] with 4 entries
void* jt_1124[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x5,  // case 3: jump to L5
};

// Jump table at data[1129] with 5 entries
void* jt_1129[5] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3e1,  // case 1: jump to L993
    (void*)0x0,  // case 2: jump to L0
    (void*)0x4,  // case 3: jump to L4
    (void*)0x2,  // case 4: jump to L2
};

// Jump table at data[1141] with 3 entries
void* jt_1141[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1145] with 3 entries
void* jt_1145[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x2,  // case 1: jump to L2
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1149] with 3 entries
void* jt_1149[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3,  // case 1: jump to L3
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1153] with 3 entries
void* jt_1153[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x4,  // case 1: jump to L4
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1157] with 3 entries
void* jt_1157[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1161] with 4 entries
void* jt_1161[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x2,  // case 3: jump to L2
};

// Jump table at data[1166] with 4 entries
void* jt_1166[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x3,  // case 3: jump to L3
};

// Jump table at data[1171] with 4 entries
void* jt_1171[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x4,  // case 3: jump to L4
};

// Jump table at data[1176] with 4 entries
void* jt_1176[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x5,  // case 3: jump to L5
};

// Jump table at data[1181] with 5 entries
void* jt_1181[5] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3e2,  // case 1: jump to L994
    (void*)0x0,  // case 2: jump to L0
    (void*)0x4,  // case 3: jump to L4
    (void*)0x2,  // case 4: jump to L2
};

// Jump table at data[1193] with 3 entries
void* jt_1193[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1197] with 3 entries
void* jt_1197[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x2,  // case 1: jump to L2
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1201] with 3 entries
void* jt_1201[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3,  // case 1: jump to L3
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1205] with 3 entries
void* jt_1205[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x4,  // case 1: jump to L4
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1209] with 3 entries
void* jt_1209[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1213] with 4 entries
void* jt_1213[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x2,  // case 3: jump to L2
};

// Jump table at data[1218] with 4 entries
void* jt_1218[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x3,  // case 3: jump to L3
};

// Jump table at data[1223] with 4 entries
void* jt_1223[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x4,  // case 3: jump to L4
};

// Jump table at data[1228] with 4 entries
void* jt_1228[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x5,  // case 3: jump to L5
};

// Jump table at data[1233] with 5 entries
void* jt_1233[5] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3e3,  // case 1: jump to L995
    (void*)0x0,  // case 2: jump to L0
    (void*)0x4,  // case 3: jump to L4
    (void*)0x2,  // case 4: jump to L2
};

// Jump table at data[1245] with 3 entries
void* jt_1245[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1249] with 3 entries
void* jt_1249[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x2,  // case 1: jump to L2
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1253] with 3 entries
void* jt_1253[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3,  // case 1: jump to L3
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1257] with 3 entries
void* jt_1257[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x4,  // case 1: jump to L4
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1261] with 3 entries
void* jt_1261[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1265] with 4 entries
void* jt_1265[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x2,  // case 3: jump to L2
};

// Jump table at data[1270] with 4 entries
void* jt_1270[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x3,  // case 3: jump to L3
};

// Jump table at data[1275] with 4 entries
void* jt_1275[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x4,  // case 3: jump to L4
};

// Jump table at data[1280] with 4 entries
void* jt_1280[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x5,  // case 3: jump to L5
};

// Jump table at data[1285] with 5 entries
void* jt_1285[5] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3e4,  // case 1: jump to L996
    (void*)0x0,  // case 2: jump to L0
    (void*)0x4,  // case 3: jump to L4
    (void*)0x2,  // case 4: jump to L2
};

// Jump table at data[1297] with 3 entries
void* jt_1297[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1301] with 3 entries
void* jt_1301[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x2,  // case 1: jump to L2
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1305] with 3 entries
void* jt_1305[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3,  // case 1: jump to L3
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1309] with 3 entries
void* jt_1309[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x4,  // case 1: jump to L4
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1313] with 3 entries
void* jt_1313[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1317] with 4 entries
void* jt_1317[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x2,  // case 3: jump to L2
};

// Jump table at data[1322] with 4 entries
void* jt_1322[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x3,  // case 3: jump to L3
};

// Jump table at data[1327] with 4 entries
void* jt_1327[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x4,  // case 3: jump to L4
};

// Jump table at data[1332] with 4 entries
void* jt_1332[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x5,  // case 3: jump to L5
};

// Jump table at data[1337] with 5 entries
void* jt_1337[5] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3e5,  // case 1: jump to L997
    (void*)0x0,  // case 2: jump to L0
    (void*)0x4,  // case 3: jump to L4
    (void*)0x2,  // case 4: jump to L2
};

// Jump table at data[1349] with 3 entries
void* jt_1349[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1353] with 3 entries
void* jt_1353[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x2,  // case 1: jump to L2
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1357] with 3 entries
void* jt_1357[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3,  // case 1: jump to L3
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1361] with 3 entries
void* jt_1361[3] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x4,  // case 1: jump to L4
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1365] with 3 entries
void* jt_1365[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
};

// Jump table at data[1369] with 4 entries
void* jt_1369[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x2,  // case 3: jump to L2
};

// Jump table at data[1374] with 4 entries
void* jt_1374[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x3,  // case 3: jump to L3
};

// Jump table at data[1379] with 4 entries
void* jt_1379[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x4,  // case 3: jump to L4
};

// Jump table at data[1384] with 4 entries
void* jt_1384[4] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x1,  // case 2: jump to L1
    (void*)0x5,  // case 3: jump to L5
};

// Jump table at data[1389] with 5 entries
void* jt_1389[5] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x3,  // case 1: jump to L3
    (void*)0x0,  // case 2: jump to L0
    (void*)0x0,  // case 3: jump to L0
    (void*)0x2,  // case 4: jump to L2
};

// Jump table at data[1403] with 4 entries
void* jt_1403[4] = {
    (void*)0x4,  // case 0: jump to L4
    (void*)0x0,  // case 1: jump to L0
    (void*)0x0,  // case 2: jump to L0
    (void*)0x2,  // case 3: jump to L2
};

// Jump table at data[1416] with 9 entries
void* jt_1416[9] = {
    (void*)0x4,  // case 0: jump to L4
    (void*)0x1,  // case 1: jump to L1
    (void*)0x9,  // case 2: jump to L9
    (void*)0x1f3,  // case 3: jump to L499
    (void*)0x7,  // case 4: jump to L7
    (void*)0x0,  // case 5: jump to L0
    (void*)0x1,  // case 6: jump to L1
    (void*)0x1,  // case 7: jump to L1
    (void*)0x1,  // case 8: jump to L1
};

// Jump table at data[1426] with 27 entries
void* jt_1426[27] = {
    (void*)0x3,  // case 0: jump to L3
    (void*)0x1,  // case 1: jump to L1
    (void*)0xc,  // case 2: jump to L12
    (void*)0x3,  // case 3: jump to L3
    (void*)0x0,  // case 4: jump to L0
    (void*)0x12,  // case 5: jump to L18
    (void*)0x0,  // case 6: jump to L0
    (void*)0x13,  // case 7: jump to L19
    (void*)0x0,  // case 8: jump to L0
    (void*)0x27,  // case 9: jump to L39
    (void*)0x0,  // case 10: jump to L0
    (void*)0x15,  // case 11: jump to L21
    (void*)0x2,  // case 12: jump to L2
    (void*)0x16,  // case 13: jump to L22
    (void*)0x0,  // case 14: jump to L0
    (void*)0x17,  // case 15: jump to L23
    (void*)0x0,  // case 16: jump to L0
    (void*)0x18,  // case 17: jump to L24
    (void*)0x0,  // case 18: jump to L0
    (void*)0x19,  // case 19: jump to L25
    (void*)0x0,  // case 20: jump to L0
    (void*)0x1a,  // case 21: jump to L26
    (void*)0x0,  // case 22: jump to L0
    (void*)0x3c,  // case 23: jump to L60
    (void*)0x44a,  // case 24: jump to L1098
    (void*)0x3,  // case 25: jump to L3
    (void*)0x0,  // case 26: jump to L0
};

// Jump table at data[1456] with 5 entries
void* jt_1456[5] = {
    (void*)0x8,  // case 0: jump to L8
    (void*)0x1,  // case 1: jump to L1
    (void*)0x1,  // case 2: jump to L1
    (void*)0x3f2,  // case 3: jump to L1010
    (void*)0x0,  // case 4: jump to L0
};

// Jump table at data[1462] with 3 entries
void* jt_1462[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x3f3,  // case 1: jump to L1011
    (void*)0x4,  // case 2: jump to L4
};

// Jump table at data[1466] with 26 entries
void* jt_1466[26] = {
    (void*)0x4,  // case 0: jump to L4
    (void*)0x0,  // case 1: jump to L0
    (void*)0x0,  // case 2: jump to L0
    (void*)0x2,  // case 3: jump to L2
    (void*)0x1,  // case 4: jump to L1
    (void*)0x1,  // case 5: jump to L1
    (void*)0x1,  // case 6: jump to L1
    (void*)0x1,  // case 7: jump to L1
    (void*)0x0,  // case 8: jump to L0
    (void*)0x12,  // case 9: jump to L18
    (void*)0x0,  // case 10: jump to L0
    (void*)0x13,  // case 11: jump to L19
    (void*)0x0,  // case 12: jump to L0
    (void*)0x27,  // case 13: jump to L39
    (void*)0x0,  // case 14: jump to L0
    (void*)0x0,  // case 15: jump to L0
    (void*)0x6,  // case 16: jump to L6
    (void*)0x1,  // case 17: jump to L1
    (void*)0x4,  // case 18: jump to L4
    (void*)0x15,  // case 19: jump to L21
    (void*)0x4,  // case 20: jump to L4
    (void*)0x1,  // case 21: jump to L1
    (void*)0x3c,  // case 22: jump to L60
    (void*)0x44a,  // case 23: jump to L1098
    (void*)0x3,  // case 24: jump to L3
    (void*)0x0,  // case 25: jump to L0
};

// Jump table at data[1495] with 5 entries
void* jt_1495[5] = {
    (void*)0x8,  // case 0: jump to L8
    (void*)0x19,  // case 1: jump to L25
    (void*)0x1,  // case 2: jump to L1
    (void*)0x3f2,  // case 3: jump to L1010
    (void*)0x0,  // case 4: jump to L0
};

// Jump table at data[1501] with 3 entries
void* jt_1501[3] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x3f3,  // case 1: jump to L1011
    (void*)0x4,  // case 2: jump to L4
};

// Jump table at data[1505] with 10 entries
void* jt_1505[10] = {
    (void*)0x4,  // case 0: jump to L4
    (void*)0x1,  // case 1: jump to L1
    (void*)0x2,  // case 2: jump to L2
    (void*)0x1,  // case 3: jump to L1
    (void*)0x1,  // case 4: jump to L1
    (void*)0x1,  // case 5: jump to L1
    (void*)0x1,  // case 6: jump to L1
    (void*)0x1,  // case 7: jump to L1
    (void*)0x1,  // case 8: jump to L1
    (void*)0x0,  // case 9: jump to L0
};

// Jump table at data[1516] with 5 entries
void* jt_1516[5] = {
    (void*)0x1f4,  // case 0: jump to L500
    (void*)0x8,  // case 1: jump to L8
    (void*)0x64,  // case 2: jump to L100
    (void*)0xc,  // case 3: jump to L12
    (void*)0x64,  // case 4: jump to L100
};

// Jump table at data[1525] with 18 entries
void* jt_1525[18] = {
    (void*)0x3,  // case 0: jump to L3
    (void*)0x0,  // case 1: jump to L0
    (void*)0x0,  // case 2: jump to L0
    (void*)0x10,  // case 3: jump to L16
    (void*)0x0,  // case 4: jump to L0
    (void*)0x0,  // case 5: jump to L0
    (void*)0x1,  // case 6: jump to L1
    (void*)0x0,  // case 7: jump to L0
    (void*)0x1,  // case 8: jump to L1
    (void*)0xc,  // case 9: jump to L12
    (void*)0x0,  // case 10: jump to L0
    (void*)0xb,  // case 11: jump to L11
    (void*)0x0,  // case 12: jump to L0
    (void*)0x0,  // case 13: jump to L0
    (void*)0x10,  // case 14: jump to L16
    (void*)0x0,  // case 15: jump to L0
    (void*)0x0,  // case 16: jump to L0
    (void*)0x3,  // case 17: jump to L3
};

// Jump table at data[1550] with 4 entries
void* jt_1550[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x3,  // case 1: jump to L3
    (void*)0x0,  // case 2: jump to L0
    (void*)0x0,  // case 3: jump to L0
};

// Jump table at data[1562] with 5 entries
void* jt_1562[5] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x0,  // case 1: jump to L0
    (void*)0x64,  // case 2: jump to L100
    (void*)0xc,  // case 3: jump to L12
    (void*)0x64,  // case 4: jump to L100
};

// Jump table at data[1571] with 18 entries
void* jt_1571[18] = {
    (void*)0x3,  // case 0: jump to L3
    (void*)0xc0,  // case 1: jump to L192
    (void*)0x4,  // case 2: jump to L4
    (void*)0x10,  // case 3: jump to L16
    (void*)0x4,  // case 4: jump to L4
    (void*)0x4,  // case 5: jump to L4
    (void*)0x1,  // case 6: jump to L1
    (void*)0x4,  // case 7: jump to L4
    (void*)0x1,  // case 8: jump to L1
    (void*)0xc,  // case 9: jump to L12
    (void*)0x4,  // case 10: jump to L4
    (void*)0xf,  // case 11: jump to L15
    (void*)0xc0,  // case 12: jump to L192
    (void*)0x4,  // case 13: jump to L4
    (void*)0x10,  // case 14: jump to L16
    (void*)0x4,  // case 15: jump to L4
    (void*)0x4,  // case 16: jump to L4
    (void*)0x3,  // case 17: jump to L3
};

// Jump table at data[1596] with 4 entries
void* jt_1596[4] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x3,  // case 1: jump to L3
    (void*)0x4,  // case 2: jump to L4
    (void*)0x0,  // case 3: jump to L0
};

// Jump table at data[1608] with 17 entries
void* jt_1608[17] = {
    (void*)0x1,  // case 0: jump to L1
    (void*)0x60,  // case 1: jump to L96
    (void*)0x40,  // case 2: jump to L64
    (void*)0x1,  // case 3: jump to L1
    (void*)0x0,  // case 4: jump to L0
    (void*)0x10,  // case 5: jump to L16
    (void*)0x309,  // case 6: jump to L777
    (void*)0x0,  // case 7: jump to L0
    (void*)0x1,  // case 8: jump to L1
    (void*)0x2,  // case 9: jump to L2
    (void*)0x1f4,  // case 10: jump to L500
    (void*)0x3,  // case 11: jump to L3
    (void*)0x44b,  // case 12: jump to L1099
    (void*)0x4,  // case 13: jump to L4
    (void*)0x419,  // case 14: jump to L1049
    (void*)0x0,  // case 15: jump to L0
    (void*)0x0,  // case 16: jump to L0
};

// Jump table at data[1640] with 4 entries
void* jt_1640[4] = {
    (void*)0x6,  // case 0: jump to L6
    (void*)0xc0,  // case 1: jump to L192
    (void*)0x4,  // case 2: jump to L4
    (void*)0x30,  // case 3: jump to L48
};

// Jump table at data[1646] with 10 entries
void* jt_1646[10] = {
    (void*)0x30,  // case 0: jump to L48
    (void*)0x4,  // case 1: jump to L4
    (void*)0xc0,  // case 2: jump to L192
    (void*)0x10,  // case 3: jump to L16
    (void*)0x7,  // case 4: jump to L7
    (void*)0xa,  // case 5: jump to L10
    (void*)0x60,  // case 6: jump to L96
    (void*)0x0,  // case 7: jump to L0
    (void*)0x0,  // case 8: jump to L0
    (void*)0x1,  // case 9: jump to L1
};

// Jump table at data[1657] with 8 entries
void* jt_1657[8] = {
    (void*)0x0,  // case 0: jump to L0
    (void*)0x0,  // case 1: jump to L0
    (void*)0x0,  // case 2: jump to L0
    (void*)0x0,  // case 3: jump to L0
    (void*)0x0,  // case 4: jump to L0
    (void*)0xb,  // case 5: jump to L11
    (void*)0x0,  // case 6: jump to L0
    (void*)0x1,  // case 7: jump to L1
};

char str_167[] = "\"EndRule unsopported: %d\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L0 = (void*)0x0;  // points to code
char str_185[] = "\"US-%01d-%01d-%01d\"";
void* code_L5 = (void*)0x5;  // points to code
char str_191[] = "\"VC-%01d-%01d-%01d\"";
char str_287[] = "\"SPOUSTEC2\"";
char str_295[] = "\"VC-%01d-%01d-%01d\"";
char str_307[] = "\"VC-%01d-%01d-%01d\"";
char str_319[] = "\"VC-%01d-%01d-%01d\"";
char str_331[] = "\"VC-%01d-%01d-%01d\"";
char str_343[] = "\"VC-%01d-%01d-%01d\"";
char str_355[] = "\"VC-%01d-%01d-%01d\"";
char str_381[] = "\"SNIPERPOS\"";
char str_389[] = "\"VC-%01d-%01d-%01d\"";
char str_401[] = "\"VC-%01d-%01d-%01d\"";
char str_413[] = "\"VC-%01d-%01d-%01d\"";
char str_425[] = "\"VC-%01d-%01d-%01d\"";
char str_445[] = "\"SPOUSTEC4\"";
char str_453[] = "\"VC-%01d-%01d-%01d\"";
char str_465[] = "\"VC-%01d-%01d-%01d\"";
char str_477[] = "\"VC-%01d-%01d-%01d\"";
char str_489[] = "\"VC-%01d-%01d-%01d\"";
char str_509[] = "\"MAPA\"";
char str_516[] = "\"VC-%01d-%01d-%01d\"";
char str_528[] = "\"VC-%01d-%01d-%01d\"";
char str_540[] = "\"VC-%01d-%01d-%01d\"";
char str_552[] = "\"VC-%01d-%01d-%01d\"";
char str_650[] = "\"HideMap\"";
char str_652[] = "\"MAPA\"";
void* code_L9 = (void*)0x9;  // points to code
void* code_L0 = (void*)0x0;  // points to code
char str_661[] = "\"burnsphere\"";
void* code_L16 = (void*)0x10;  // points to code
void* code_L0 = (void*)0x0;  // points to code
void* code_L16 = (void*)0x10;  // points to code
void* code_L4 = (void*)0x4;  // points to code
void* code_L16 = (void*)0x10;  // points to code
void* code_L5 = (void*)0x5;  // points to code
void* code_L1 = (void*)0x1;  // points to code
char str_679[] = "\"burnsphere\"";
void* code_L16 = (void*)0x10;  // points to code
void* code_L16 = (void*)0x10;  // points to code
void* code_L0 = (void*)0x0;  // points to code
void* code_L16 = (void*)0x10;  // points to code
void* code_L4 = (void*)0x4;  // points to code
void* code_L16 = (void*)0x10;  // points to code
void* code_L5 = (void*)0x5;  // points to code
void* code_L64 = (void*)0x40;  // points to code
char str_694[] = "\"SPOUSTEC0\"";
char str_708[] = "\"ATTACK1\"";
char str_710[] = "\"ATTACK2\"";
char str_712[] = "\"ATTACK3\"";
char str_714[] = "\"ATTACK4\"";
char str_716[] = "\"SPOUSTEC1\"";
char str_754[] = "\"SPOUSTEC2\"";
char str_757[] = "\"SPOUSTEC2A\"";
char str_776[] = "\"SPOUSTEC3\"";
char str_791[] = "\"SPOUSTEC4\"";
char str_806[] = "\"SPOUSTEC5\"";
char str_815[] = "\" APILOT1\"";
char str_818[] = "\"PILOT2\"";
char str_831[] = "\"SPOUSTEC6\"";
char str_845[] = "\"SPOUSTEC7\"";
char str_893[] = "\"coop script wrong side: %d\"";
char str_935[] = "\"Enum, v[0]: %d   v[1]: %d  alldeath: %d\"";
char str_949[] = "\"NoEnum\"";
char str_969[] = "\"Set GPHASE_FAILED\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L4 = (void*)0x4;  // points to code
char str_990[] = "\"Set GPHASE_GAME\"";
void* code_L2 = (void*)0x2;  // points to code
char str_1001[] = "\"Set GPHASE_DONE\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L3 = (void*)0x3;  // points to code
char str_1038[] = "\"Set GPHASE_DONE\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L3 = (void*)0x3;  // points to code
char str_1082[] = "\"Set GPHASE_DONE\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L3 = (void*)0x3;  // points to code
char str_1134[] = "\"Set GPHASE_DONE\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L3 = (void*)0x3;  // points to code
char str_1186[] = "\"Set GPHASE_DONE\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L3 = (void*)0x3;  // points to code
char str_1238[] = "\"Set GPHASE_DONE\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L3 = (void*)0x3;  // points to code
char str_1290[] = "\"Set GPHASE_DONE\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L3 = (void*)0x3;  // points to code
char str_1342[] = "\"Set GPHASE_DONE\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L3 = (void*)0x3;  // points to code
char str_1394[] = "\"SC_MP_RestartMission\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L1 = (void*)0x1;  // points to code
char str_1407[] = "\"SC_MP_RestartMission\"";
void* code_L2 = (void*)0x2;  // points to code
void* code_L1 = (void*)0x1;  // points to code
void* code_L4 = (void*)0x4;  // points to code
void* code_L4 = (void*)0x4;  // points to code
char str_1521[] = "\"USSpawn_coop_%d\"";
char str_1543[] = "\"ATG UsBomb respawns us: %d\"";
char str_1554[] = "\"no US recover place defined!\"";
char str_1567[] = "\"VCSpawn_coop_%d\"";
char str_1589[] = "\"ATG UsBomb respawns vc: %d\"";
char str_1600[] = "\"no VC recover place defined!\"";
void* code_L5 = (void*)0x5;  // points to code
void* code_L0 = (void*)0x0;  // points to code
void* code_L0 = (void*)0x0;  // points to code
void* code_L0 = (void*)0x0;  // points to code

void func_28(void) {
  int local_1;
  int local_11;
  int local_18;
  int local_19;
  int local_259;
  int local_269;
  int local_3;
  int local_4;

  SC_P_IsReady(stack_tmp_0 + 1 + 147);  // 32
  while (1) {
    func_108();  // 36
    data[1] = (void*)0x94;  // 41
    SC_P_IsReady(local_259);  // 47
    func_99();  // 48
    *SC_P_IsReady(local_259) = (void*)0x95;  // 52
    SC_MP_EndRule_SetTimeLeft();  // 58
    *SC_MP_EndRule_SetTimeLeft() = (void*)0x98;  // 62
    SC_MP_EndRule_SetTimeLeft();  // 68
    *SC_MP_EndRule_SetTimeLeft() = (void*)0x9b;  // 72
    SC_MP_EndRule_SetTimeLeft();  // 78
    *SC_MP_EndRule_SetTimeLeft() = (void*)0x9e;  // 82
    SC_MP_EndRule_SetTimeLeft();  // 88
    *SC_MP_EndRule_SetTimeLeft() = (void*)0xa1;  // 92
    SC_MP_EndRule_SetTimeLeft();  // 98
    SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 163.0);  // 105
    SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 163.0));  // 106
    if (SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 163.0))) break;  // 107
  }
    func_146();  // 115
  func_124();  // 117
  SC_P_IsReady(259.0 + jt_2_case125);  // 123
  SC_P_ChangeWeapon();  // 127
  SRS(0, 0);  // 131
  func_137();  // 132
  if (local_3 + 1) {
    SC_P_IsReady(166u);  // 147
  }
  if (SC_P_ChangeWeapon()) {
    SC_P_IsReady(166u);  // 147
  }
    SC_P_IsReady(166u);  // 147
  SC_P_ChangeWeapon();  // 189
  SC_P_IsReady(local_1 + SC_P_ChangeWeapon());  // 192
  func_200();  // 196
  SC_P_ChangeWeapon();  // 203
  func_226();  // 212
  if (SC_P_IsReady(SC_message())) {
    SC_P_ChangeWeapon();  // 244
    SC_P_IsReady(SC_P_ChangeWeapon());  // 245
  }
  SC_message();  // 236
  SC_P_IsReady(SC_message());  // 237
  SC_MP_EndRule_SetTimeLeft();  // 253
  SC_P_ChangeWeapon();  // 256
  SC_P_IsReady(local_1);  // 264
  SC_P_IsReady((197 != &data[1]) + SC_P_IsReady(local_1));  // 267
  *(void*)0xc8 = (void*)0xc9;  // 274
  SC_MP_LoadNextMap();  // 277
  SC_P_IsReady(local_1);  // 283
  SC_P_IsReady((202 != &data[1]) + SC_P_IsReady(local_1));  // 286
  *(void*)0xcd = (void*)0xce;  // 293
  SC_MP_LoadNextMap();  // 296
  SC_P_IsReady(local_1);  // 302
  SC_P_IsReady((207 != &data[1]) + SC_P_IsReady(local_1));  // 305
  *(void*)0xd2 = (void*)0xd3;  // 312
  SC_MP_LoadNextMap();  // 315
  SC_P_IsReady(local_1);  // 321
  SC_P_IsReady((212 != &data[1]) + SC_P_IsReady(local_1));  // 324
  *(void*)0xd7 = (void*)0xd8;  // 331
  SC_MP_LoadNextMap();  // 334
  SC_P_IsReady(local_1);  // 340
  SC_P_IsReady((217 != &data[1]) + SC_P_IsReady(local_1));  // 343
  *(void*)0xdc = (void*)0xdd;  // 350
  SC_MP_LoadNextMap();  // 353
  SC_P_IsReady(local_1);  // 359
  SC_P_IsReady((222 != &data[1]) + SC_P_IsReady(local_1));  // 362
  *(void*)0xe1 = (void*)0xe2;  // 369
  SC_MP_LoadNextMap();  // 372
  SC_P_IsReady(local_1);  // 378
  SC_P_IsReady((227 != &data[1]) + SC_P_IsReady(local_1));  // 381
  *(void*)0xe6 = (void*)0xe7;  // 388
  SC_MP_LoadNextMap();  // 391
  SC_P_IsReady(local_1);  // 397
  SC_P_IsReady((232 != &data[1]) + SC_P_IsReady(local_1));  // 400
  *(void*)0xeb = (void*)0xec;  // 407
  SC_MP_LoadNextMap();  // 410
  SC_P_IsReady(local_1);  // 416
  SC_P_IsReady((237 != &data[1]) + SC_P_IsReady(local_1));  // 419
  *(void*)0xf0 = (void*)0xf1;  // 426
  SC_MP_LoadNextMap();  // 429
  SC_P_IsReady(local_1);  // 435
  SC_P_IsReady((242 != &data[1]) + SC_P_IsReady(local_1));  // 438
  *(void*)0xf5 = (void*)0xf6;  // 445
  SC_MP_LoadNextMap();  // 448
  SC_P_IsReady(local_1);  // 454
  SC_P_IsReady((247 != &data[1]) + SC_P_IsReady(local_1));  // 457
  *(void*)0xfa = (void*)0xfb;  // 464
  SC_MP_LoadNextMap();  // 467
  SC_P_IsReady(local_1);  // 473
  SC_P_IsReady((252 != &data[1]) + SC_P_IsReady(local_1));  // 476
  *(void*)0xff = (void*)0x100;  // 483
  SC_MP_LoadNextMap();  // 486
  SC_P_IsReady(local_1);  // 492
  SC_P_IsReady((257 != &data[1]) + SC_P_IsReady(local_1));  // 495
  *(void*)0x104 = (void*)0x105;  // 502
  SC_MP_LoadNextMap();  // 505
  SC_P_IsReady(local_1);  // 511
  SC_P_IsReady((262 != &data[1]) + SC_P_IsReady(local_1));  // 514
  *(void*)0x109 = (void*)0x10a;  // 521
  SC_MP_LoadNextMap();  // 524
  SC_P_IsReady(local_1);  // 530
  SC_P_IsReady((267 != &data[1]) + SC_P_IsReady(local_1));  // 533
  *(void*)0x10e = (void*)0x10f;  // 540
  SC_MP_LoadNextMap();  // 543
  SC_P_IsReady(local_1);  // 549
  SC_P_IsReady((272 != &data[1]) + SC_P_IsReady(local_1));  // 552
  *(void*)0x113 = (void*)0x114;  // 559
  SC_MP_LoadNextMap();  // 562
  SC_P_IsReady(local_1);  // 568
  SC_P_IsReady((277 != &data[1]) + SC_P_IsReady(local_1));  // 571
  *(void*)0x118 = (void*)0x119;  // 578
  SC_MP_LoadNextMap();  // 581
  SC_P_IsReady(local_1);  // 587
  SC_P_IsReady((282 != &data[1]) + SC_P_IsReady(local_1));  // 590
  *(void*)0x11d = (void*)0x11e;  // 597
  SC_MP_LoadNextMap();  // 600
  SC_P_ChangeWeapon();  // 616
  SC_P_IsReady(SC_P_ChangeWeapon());  // 617
  SC_P_ChangeWeapon();  // 624
  SC_P_IsReady(SC_P_ChangeWeapon());  // 625
  SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 291);  // 629
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 291) + 292);  // 633
  SC_P_IsReady(local_18);  // 639
  *SC_P_IsReady(local_18) = (void*)0x126;  // 642
  SC_P_IsReady(&data[1] + (293 != &data[1]) - 1.0);  // 646
  SC_message();  // 657
  SC_P_IsReady(SC_message());  // 658
  SC_P_ChangeWeapon();  // 665
  SC_P_IsReady(SC_P_ChangeWeapon());  // 666
  SC_MP_EndRule_SetTimeLeft();  // 675
  SC_MP_EndRule_SetTimeLeft();  // 681
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 682
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 303);  // 686
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 303) + 304);  // 690
  SC_P_IsReady(local_18);  // 696
  *SC_P_IsReady(local_18) = (void*)0x132;  // 699
  SC_P_IsReady(&data[1] + (305 != &data[1]) - 1.0);  // 703
  SC_message();  // 714
  SC_P_IsReady(SC_message());  // 715
  SC_P_ChangeWeapon();  // 722
  SC_P_IsReady(SC_P_ChangeWeapon());  // 723
  SC_MP_EndRule_SetTimeLeft();  // 732
  SC_MP_EndRule_SetTimeLeft();  // 738
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 739
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 315);  // 743
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 315) + 316);  // 747
  SC_P_IsReady(local_18);  // 753
  *SC_P_IsReady(local_18) = (void*)0x13e;  // 756
  SC_P_IsReady(&data[1] + (317 != &data[1]) - 1.0);  // 760
  SC_message();  // 771
  SC_P_IsReady(SC_message());  // 772
  SC_P_ChangeWeapon();  // 779
  SC_P_IsReady(SC_P_ChangeWeapon());  // 780
  SC_MP_EndRule_SetTimeLeft();  // 789
  SC_MP_EndRule_SetTimeLeft();  // 795
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 796
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 327);  // 800
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 327) + 328);  // 804
  SC_P_IsReady(local_18);  // 810
  *SC_P_IsReady(local_18) = (void*)0x14a;  // 813
  SC_P_IsReady(&data[1] + (329 != &data[1]) - 1.0);  // 817
  SC_message();  // 828
  SC_P_IsReady(SC_message());  // 829
  SC_P_ChangeWeapon();  // 836
  SC_P_IsReady(SC_P_ChangeWeapon());  // 837
  SC_MP_EndRule_SetTimeLeft();  // 846
  SC_MP_EndRule_SetTimeLeft();  // 852
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 853
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 339);  // 857
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 339) + 340);  // 861
  SC_P_IsReady(local_18);  // 867
  *SC_P_IsReady(local_18) = (void*)0x156;  // 870
  SC_P_IsReady(&data[1] + (341 != &data[1]) - 1.0);  // 874
  SC_message();  // 885
  SC_P_IsReady(SC_message());  // 886
  SC_P_ChangeWeapon();  // 893
  SC_P_IsReady(SC_P_ChangeWeapon());  // 894
  SC_MP_EndRule_SetTimeLeft();  // 903
  SC_MP_EndRule_SetTimeLeft();  // 909
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 910
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 351);  // 914
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 351) + 352);  // 918
  SC_P_IsReady(local_18);  // 924
  *SC_P_IsReady(local_18) = (void*)0x162;  // 927
  SC_P_IsReady(&data[1] + (353 != &data[1]) - 1.0);  // 931
  SC_message();  // 942
  SC_P_IsReady(SC_message());  // 943
  SC_P_ChangeWeapon();  // 950
  SC_P_IsReady(SC_P_ChangeWeapon());  // 951
  SC_MP_EndRule_SetTimeLeft();  // 960
  SC_MP_EndRule_SetTimeLeft();  // 966
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 967
  SC_MP_EndRule_SetTimeLeft();  // 975
  SC_P_ChangeWeapon();  // 978
  SC_MP_EndRule_SetTimeLeft();  // 986
  SC_P_ChangeWeapon();  // 989
  SC_MP_EndRule_SetTimeLeft();  // 997
  SC_P_ChangeWeapon();  // 1000
  SC_MP_EndRule_SetTimeLeft();  // 1008
  SC_P_ChangeWeapon();  // 1011
  SC_MP_EndRule_SetTimeLeft();  // 1019
  SC_P_ChangeWeapon();  // 1022
  SC_MP_EndRule_SetTimeLeft();  // 1030
  SC_P_ChangeWeapon();  // 1033
  SC_P_ChangeWeapon();  // 1049
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1050
  SC_P_ChangeWeapon();  // 1057
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1058
  SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 385);  // 1062
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 385) + 386);  // 1066
  SC_P_IsReady(local_18);  // 1072
  *SC_P_IsReady(local_18) = (void*)0x184;  // 1075
  SC_P_IsReady(&data[1] + (387 != &data[1]) - 1.0);  // 1079
  SC_message();  // 1090
  SC_P_IsReady(SC_message());  // 1091
  SC_P_ChangeWeapon();  // 1098
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1099
  SC_MP_EndRule_SetTimeLeft();  // 1108
  SC_MP_EndRule_SetTimeLeft();  // 1114
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1115
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 397);  // 1119
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 397) + 398);  // 1123
  SC_P_IsReady(local_18);  // 1129
  *SC_P_IsReady(local_18) = (void*)0x190;  // 1132
  SC_P_IsReady(&data[1] + (399 != &data[1]) - 1.0);  // 1136
  SC_message();  // 1147
  SC_P_IsReady(SC_message());  // 1148
  SC_P_ChangeWeapon();  // 1155
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1156
  SC_MP_EndRule_SetTimeLeft();  // 1165
  SC_MP_EndRule_SetTimeLeft();  // 1171
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1172
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 409);  // 1176
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 409) + 410);  // 1180
  SC_P_IsReady(local_18);  // 1186
  *SC_P_IsReady(local_18) = (void*)0x19c;  // 1189
  SC_P_IsReady(&data[1] + (411 != &data[1]) - 1.0);  // 1193
  SC_message();  // 1204
  SC_P_IsReady(SC_message());  // 1205
  SC_P_ChangeWeapon();  // 1212
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1213
  SC_MP_EndRule_SetTimeLeft();  // 1222
  SC_MP_EndRule_SetTimeLeft();  // 1228
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1229
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 421);  // 1233
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 421) + 422);  // 1237
  SC_P_IsReady(local_18);  // 1243
  *SC_P_IsReady(local_18) = (void*)0x1a8;  // 1246
  SC_P_IsReady(&data[1] + (423 != &data[1]) - 1.0);  // 1250
  SC_message();  // 1261
  SC_P_IsReady(SC_message());  // 1262
  SC_P_ChangeWeapon();  // 1269
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1270
  SC_MP_EndRule_SetTimeLeft();  // 1279
  SC_MP_EndRule_SetTimeLeft();  // 1285
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1286
  SC_MP_EndRule_SetTimeLeft();  // 1294
  SC_P_ChangeWeapon();  // 1297
  SC_MP_EndRule_SetTimeLeft();  // 1305
  SC_P_ChangeWeapon();  // 1308
  SC_MP_EndRule_SetTimeLeft();  // 1316
  SC_P_ChangeWeapon();  // 1319
  SC_MP_EndRule_SetTimeLeft();  // 1327
  SC_P_ChangeWeapon();  // 1330
  SC_P_ChangeWeapon();  // 1346
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1347
  SC_P_ChangeWeapon();  // 1354
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1355
  SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 449);  // 1359
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + 449) + 450);  // 1363
  SC_P_IsReady(local_18);  // 1369
  *SC_P_IsReady(local_18) = (void*)0x1c4;  // 1372
  SC_P_IsReady(&data[1] + (451 != &data[1]) - 1.0);  // 1376
  SC_message();  // 1387
  SC_P_IsReady(SC_message());  // 1388
  SC_P_ChangeWeapon();  // 1395
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1396
  SC_MP_EndRule_SetTimeLeft();  // 1405
  SC_MP_EndRule_SetTimeLeft();  // 1411
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1412
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 461);  // 1416
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 461) + 462);  // 1420
  SC_P_IsReady(local_18);  // 1426
  *SC_P_IsReady(local_18) = (void*)0x1d0;  // 1429
  SC_P_IsReady(&data[1] + (463 != &data[1]) - 1.0);  // 1433
  SC_message();  // 1444
  SC_P_IsReady(SC_message());  // 1445
  SC_P_ChangeWeapon();  // 1452
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1453
  SC_MP_EndRule_SetTimeLeft();  // 1462
  SC_MP_EndRule_SetTimeLeft();  // 1468
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1469
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 473);  // 1473
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 473) + 474);  // 1477
  SC_P_IsReady(local_18);  // 1483
  *SC_P_IsReady(local_18) = (void*)0x1dc;  // 1486
  SC_P_IsReady(&data[1] + (475 != &data[1]) - 1.0);  // 1490
  SC_message();  // 1501
  SC_P_IsReady(SC_message());  // 1502
  SC_P_ChangeWeapon();  // 1509
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1510
  SC_MP_EndRule_SetTimeLeft();  // 1519
  SC_MP_EndRule_SetTimeLeft();  // 1525
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1526
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 485);  // 1530
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 485) + 486);  // 1534
  SC_P_IsReady(local_18);  // 1540
  *SC_P_IsReady(local_18) = (void*)0x1e8;  // 1543
  SC_P_IsReady(&data[1] + (487 != &data[1]) - 1.0);  // 1547
  SC_message();  // 1558
  SC_P_IsReady(SC_message());  // 1559
  SC_P_ChangeWeapon();  // 1566
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1567
  SC_MP_EndRule_SetTimeLeft();  // 1576
  SC_MP_EndRule_SetTimeLeft();  // 1582
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1583
  SC_MP_EndRule_SetTimeLeft();  // 1591
  SC_P_ChangeWeapon();  // 1594
  SC_MP_EndRule_SetTimeLeft();  // 1602
  SC_P_ChangeWeapon();  // 1605
  SC_MP_EndRule_SetTimeLeft();  // 1613
  SC_P_ChangeWeapon();  // 1616
  SC_MP_EndRule_SetTimeLeft();  // 1624
  SC_P_ChangeWeapon();  // 1627
  SC_P_ChangeWeapon();  // 1643
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1644
  SC_P_ChangeWeapon();  // 1651
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1652
  SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + UP_RLS_COLUMNS);  // 1656
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_ChangeWeapon()) + UP_RLS_COLUMNS) + 513);  // 1660
  SC_P_IsReady(local_18);  // 1666
  *SC_P_IsReady(local_18) = (void*)0x203;  // 1669
  SC_P_IsReady(&data[1] + (514 != &data[1]) - 1.0);  // 1673
  SC_message();  // 1684
  SC_P_IsReady(SC_message());  // 1685
  SC_P_ChangeWeapon();  // 1692
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1693
  SC_MP_EndRule_SetTimeLeft();  // 1702
  SC_MP_EndRule_SetTimeLeft();  // 1708
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1709
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 524);  // 1713
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 524) + 525);  // 1717
  SC_P_IsReady(local_18);  // 1723
  *SC_P_IsReady(local_18) = (void*)0x20f;  // 1726
  SC_P_IsReady(&data[1] + (526 != &data[1]) - 1.0);  // 1730
  SC_message();  // 1741
  SC_P_IsReady(SC_message());  // 1742
  SC_P_ChangeWeapon();  // 1749
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1750
  SC_MP_EndRule_SetTimeLeft();  // 1759
  SC_MP_EndRule_SetTimeLeft();  // 1765
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1766
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 536);  // 1770
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 536) + 537);  // 1774
  SC_P_IsReady(local_18);  // 1780
  *SC_P_IsReady(local_18) = (void*)0x21b;  // 1783
  SC_P_IsReady(&data[1] + (538 != &data[1]) - 1.0);  // 1787
  SC_message();  // 1798
  SC_P_IsReady(SC_message());  // 1799
  SC_P_ChangeWeapon();  // 1806
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1807
  SC_MP_EndRule_SetTimeLeft();  // 1816
  SC_MP_EndRule_SetTimeLeft();  // 1822
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1823
  SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 548);  // 1827
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft()) + 548) + 549);  // 1831
  SC_P_IsReady(local_18);  // 1837
  *SC_P_IsReady(local_18) = (void*)0x227;  // 1840
  SC_P_IsReady(&data[1] + (GVAR_RESTART != &data[1]) - 1.0);  // 1844
  SC_message();  // 1855
  SC_P_IsReady(SC_message());  // 1856
  SC_P_ChangeWeapon();  // 1863
  SC_P_IsReady(SC_P_ChangeWeapon());  // 1864
  SC_MP_EndRule_SetTimeLeft();  // 1873
  SC_MP_EndRule_SetTimeLeft();  // 1879
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft());  // 1880
  SC_MP_EndRule_SetTimeLeft();  // 1888
  SC_P_ChangeWeapon();  // 1891
  SC_MP_EndRule_SetTimeLeft();  // 1899
  SC_P_ChangeWeapon();  // 1902
  SC_MP_EndRule_SetTimeLeft();  // 1910
  SC_P_ChangeWeapon();  // 1913
  SC_MP_EndRule_SetTimeLeft();  // 1921
  SC_P_ChangeWeapon();  // 1924
  func_1938();  // 1929
  SC_P_IsReady(129 + jt_131_case0);  // 1933
  SC_P_ChangeWeapon();  // 1937
  SC_P_IsReady(&data[1] + 573);  // 1945
  SC_P_IsReady(SC_P_IsReady(&data[1] + 573) + 574);  // 1949
  while (1) {
    func_2002();  // 1953
    SC_P_IsReady((SC_P_IsReady(SC_P_IsReady(&data[1] + 573) + 574) <= 575) + 576);  // 1957
    func_1993();  // 1961
    break;  // 1968 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 1970
    break;  // 1972 (always true)
    SC_P_IsReady(local_3);  // 1974
    func_1984();  // 1975
    SC_P_IsReady(SC_P_IsReady(local_3) + 578.0);  // 1982
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 578.0));  // 1983
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 578.0)) + 579.0);  // 1990
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 578.0)) + 579.0));  // 1991
    if (SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 578.0)) + 579.0))) break;  // 1992
    SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 580.0);  // 1999
    SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 580.0));  // 2000
    if (SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 580.0))) break;  // 2001
  }
  SC_P_IsReady(&data[1] + 582);  // 2011
  SC_P_IsReady(SC_P_IsReady(&data[1] + 582) + 583);  // 2015
  while (1) {
    func_2068();  // 2019
    SC_P_IsReady((SC_P_IsReady(SC_P_IsReady(&data[1] + 582) + 583) <= 584) + 585);  // 2023
    func_2059();  // 2027
    break;  // 2034 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 2036
    break;  // 2038 (always true)
    SC_P_IsReady(local_3);  // 2040
    func_2050();  // 2041
    SC_P_IsReady(SC_P_IsReady(local_3) + 587.0);  // 2048
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 587.0));  // 2049
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 587.0)) + 588.0);  // 2056
    SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 587.0)) + 588.0));  // 2057
    if (SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(local_3) + 587.0)) + 588.0))) break;  // 2058
    SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 589.0);  // 2065
    SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 589.0));  // 2066
    if (SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 589.0))) break;  // 2067
  }
  SC_P_IsReady(&data[1] + 591);  // 2084
  SC_P_IsReady(SC_P_IsReady(&data[1] + 591) + 592);  // 2088
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(&data[1] + 591) + 592) + 593);  // 2092
  SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(SC_P_IsReady(&data[1] + 591) + 592) + 593) + 594);  // 2096
  SC_MP_EndRule_SetTimeLeft();  // 2104
  func_2162();  // 2105
  SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 596);  // 2109
  func_2162();  // 2113
  *(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 596) <= 597) = (void*)0x256;  // 2117
}
void main(void) {
  int local_17;

  func_2497();  // 2488
  SC_MP_EndRule_SetTimeLeft();  // 2496
}
void func_2497(void) {
  int local_17;

  SC_MP_EndRule_SetTimeLeft();  // 2504
  func_2514();  // 2505
  SC_MP_EndRule_SetTimeLeft();  // 2513
}
void func_2514(void) {
  int local_265;

  SC_P_IsReady(&jt_196_case60 + 660);  // 2524
  SC_P_ChangeWeapon();  // 2531
  SC_P_IsReady(SC_P_ChangeWeapon());  // 2532
  SC_MP_EndRule_SetTimeLeft();  // 2540
  func_2543();  // 2541
}
void func_2543(void) {
  int local_265;
  int local_271;

  SC_P_IsReady(stack_tmp_0 + 1 + 665);  // 2547
  while (1) {
    func_2621();  // 2551
    data[1] = (void*)0x29a;  // 2556
    SC_P_IsReady(local_265);  // 2562
    func_2612();  // 2563
    *SC_P_IsReady(local_265) = (void*)0x29b;  // 2567
    break;  // 2571 (always true)
    SC_P_ChangeWeapon();  // 2572
    break;  // 2578 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 2580
    func_2612();  // 2581
    *SC_MP_EndRule_SetTimeLeft() = (void*)0x29d;  // 2585
    break;  // 2590 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 2591
    *SC_MP_EndRule_SetTimeLeft() = (void*)0x2a0;  // 2595
    break;  // 2600 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 2601
    *SC_MP_EndRule_SetTimeLeft() = (void*)0x2a3;  // 2605
    break;  // 2610 (always true)
    SC_MP_EndRule_SetTimeLeft();  // 2611
    SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 677.0);  // 2618
    SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 677.0));  // 2619
    if (SC_P_IsReady(SC_P_IsReady(SC_MP_EndRule_SetTimeLeft() + 677.0))) break;  // 2620
  }
  SC_P_ChangeWeapon();  // 2636
}