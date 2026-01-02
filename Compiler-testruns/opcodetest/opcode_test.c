// opcode_test.c - Testovaci skript pro mapovani vsech opcodes
// Zkompilovat: scmp opcode_test.c opcode_test.scr

#include <inc\sc_global.h>
#include <inc\sc_def.h>

// Globalni promenne pro testovani
int g_int1, g_int2, g_int3;
float g_float1, g_float2;
char g_char1, g_char2;
short g_short1, g_short2;
unsigned int g_uint1, g_uint2;
double g_double1, g_double2;

// Test aritmetickych operaci
void test_arithmetic() {
    int a, b, c;
    float f1, f2, f3;

    // Int operace
    a = 10;
    b = 3;
    c = a + b;      // ADD
    c = a - b;      // SUB
    c = a * b;      // MUL
    c = a / b;      // DIV
    c = a % b;      // MOD
    c = -a;         // NEG

    // Increment/Decrement - pro opcodes 13, 16
    a++;            // post-increment
    ++a;            // pre-increment
    b--;            // post-decrement
    --b;            // pre-decrement
    c = a++;        // post-inc s prirazenim
    c = ++a;        // pre-inc s prirazenim
    c = b--;        // post-dec s prirazenim
    c = --b;        // pre-dec s prirazenim

    // Float operace
    f1 = 10.5;
    f2 = 3.2;
    f3 = f1 + f2;   // FADD
    f3 = f1 - f2;   // FSUB
    f3 = f1 * f2;   // FMUL
    f3 = f1 / f2;   // FDIV
    f3 = -f1;       // FNEG
}

// Test DOUBLE operaci - chybejici opcodes 41, 42, atd.
void test_double_ops() {
    double d1, d2, d3;
    int i;
    float f;

    // Double aritmetika
    d1 = 10.5;
    d2 = 3.2;
    d3 = d1 + d2;   // DADD
    d3 = d1 - d2;   // DSUB
    d3 = d1 * d2;   // DMUL
    d3 = d1 / d2;   // DDIV
    d3 = -d1;       // DNEG

    // Double porovnani
    if (d1 < d2) d3 = 1.0;    // DLES
    if (d1 <= d2) d3 = 1.0;   // DLEQ
    if (d1 > d2) d3 = 1.0;    // DGRE
    if (d1 >= d2) d3 = 1.0;   // DGEQ
    if (d1 == d2) d3 = 1.0;   // DEQU
    if (d1 != d2) d3 = 1.0;   // DNEQ

    // Konverze z/do double
    i = 42;
    d1 = (double)i;   // ITOD
    i = (int)d1;      // DTOI

    f = 3.14;
    d1 = (double)f;   // FTOD
    f = (float)d1;    // DTOF
}

// Test porovnavacich operaci
void test_comparisons() {
    int a, b, result;
    float f1, f2;
    unsigned int u1, u2;

    a = 5; b = 10;

    // Int porovnani
    result = (a < b);    // LES
    result = (a <= b);   // LEQ
    result = (a > b);    // GRE
    result = (a >= b);   // GEQ
    result = (a == b);   // EQU
    result = (a != b);   // NEQ

    // Float porovnani
    f1 = 5.0; f2 = 10.0;
    result = (f1 < f2);   // FLES
    result = (f1 <= f2);  // FLEQ
    result = (f1 > f2);   // FGRE
    result = (f1 >= f2);  // FGEQ
    result = (f1 == f2);  // FEQU
    result = (f1 != f2);  // FNEQ

    // Unsigned porovnani
    u1 = 5; u2 = 10;
    result = (u1 < u2);   // ULES
    result = (u1 <= u2);  // ULEQ
    result = (u1 > u2);   // UGRE
    result = (u1 >= u2);  // UGEQ
}

// Test logickych operaci - opcodes 3 a 6
void test_logical() {
    int a, b, c, result;

    a = 1; b = 0; c = 1;

    // Logicke AND - opcode 3
    result = a && b;
    result = (a > 0) && (b > 0);
    result = a && b && c;

    // Logicke OR - opcode 6
    result = a || b;
    result = (a > 0) || (b > 0);
    result = a || b || c;

    // Logicke NOT
    result = !a;
    result = !b;
    result = !(a && b);
    result = !(a || b);

    // Kombinace
    result = (a && b) || c;
    result = a || (b && c);
    result = !a && b;
    result = a && !b;
}

// Test bitovych operaci
void test_bitwise() {
    int a, b, result;

    a = 0xFF00;
    b = 0x0F0F;

    result = a & b;      // BA (bitwise AND)
    result = a | b;      // BO (bitwise OR)
    result = a ^ b;      // BX (bitwise XOR)
    result = ~a;         // BN (bitwise NOT)
    result = a << 4;     // LS (left shift)
    result = a >> 4;     // RS (right shift)

    // Dalsi bitove kombinace
    result = (a & b) | 0x0001;
    result = (a | b) & 0xFFFF;
    result = a ^ b ^ 0x1111;
}

// Test typovych konverzi
void test_conversions() {
    int i;
    float f;
    char c;
    short s;
    unsigned int u;

    i = 42;
    f = (float)i;        // ITOF
    c = (char)i;         // ITOC
    s = (short)i;        // ITOS
    u = (unsigned int)i; // ITOu

    f = 3.14;
    i = (int)f;          // FTOI

    c = 65;
    i = (int)c;          // CTOI (signed)
    u = (unsigned int)c; // CTOu

    s = 1000;
    i = (int)s;          // STOI (signed)
    u = (unsigned int)s; // STOu

    u = 0xFFFFFFFF;
    i = (int)u;          // uTOI
}

// Test char operaci
void test_char_ops() {
    char a, b, c;
    unsigned char ua, ub, uc;

    a = 10;
    b = 3;
    c = a + b;      // CADD
    c = a - b;      // CSUB
    c = a * b;      // CMUL
    c = a / b;      // CDIV
    c = a % b;      // CMOD
    c = -a;         // CNEG

    if (a < b) c = 1;   // CLES
    if (a <= b) c = 1;  // CLEQ
    if (a > b) c = 1;   // CGRE
    if (a >= b) c = 1;  // CGEQ
    if (a == b) c = 1;  // CEQU
    if (a != b) c = 1;  // CNEQ

    // Unsigned char operace
    ua = 200;
    ub = 50;
    uc = ua + ub;
    uc = ua - ub;
    uc = ua * 2;
    uc = ua / 2;
    uc = ua % 3;
}

// Test short operaci
void test_short_ops() {
    short a, b, c;
    unsigned short ua, ub, uc;

    a = 100;
    b = 30;
    c = a + b;      // SADD
    c = a - b;      // SSUB
    c = a * b;      // SMUL
    c = a / b;      // SDIV
    c = a % b;      // SMOD
    c = -a;         // SNEG

    if (a < b) c = 1;   // SLES
    if (a <= b) c = 1;  // SLEQ
    if (a > b) c = 1;   // SGRE
    if (a >= b) c = 1;  // SGEQ
    if (a == b) c = 1;  // SEQU
    if (a != b) c = 1;  // SNEQ

    // Unsigned short operace
    ua = 50000;
    ub = 10000;
    uc = ua + ub;
    uc = ua - ub;
    uc = ua * 2;
    uc = ua / 2;
    uc = ua % 7;
}

// Test poli a indexovani
void test_arrays() {
    int arr[10];
    int i, sum;
    char str[20];

    // Pristup k poli
    arr[0] = 1;
    arr[1] = 2;
    arr[5] = arr[0] + arr[1];

    // Indexovani promennou
    i = 3;
    arr[i] = 100;
    sum = arr[i] + arr[i-1];

    // Retezec
    str[0] = 'H';
    str[1] = 'i';
    str[2] = 0;
}

// Test struktur a pointeru
typedef struct {
    int x;
    int y;
    float z;
    char name[16];
} TestStruct;

void test_structs() {
    TestStruct ts;
    TestStruct *pts;
    int val;

    ts.x = 10;
    ts.y = 20;
    ts.z = 3.14;
    ts.name[0] = 'A';

    pts = &ts;
    pts->x = 100;
    pts->y = 200;
    pts->z = 6.28;

    val = ts.x + ts.y;
    val = pts->x + pts->y;
}

// Test switch/case
void test_switch() {
    int x, result;

    x = 2;

    switch(x) {
        case 0:
            result = 100;
            break;
        case 1:
            result = 200;
            break;
        case 2:
            result = 300;
            break;
        case 3:
            result = 400;
            break;
        default:
            result = -1;
            break;
    }
}

// Test cyklu
void test_loops() {
    int i, sum;

    // For cyklus
    sum = 0;
    for (i = 0; i < 10; i++) {
        sum = sum + i;
    }

    // While cyklus
    i = 0;
    while (i < 5) {
        sum = sum + 1;
        i++;
    }

    // Do-while cyklus
    i = 0;
    do {
        sum = sum - 1;
        i++;
    } while (i < 3);
}

// Test slozitych vyrazu
void test_complex_expressions() {
    int a, b, c, d, result;
    float f1, f2, f3;

    a = 10; b = 20; c = 30; d = 40;

    // Slozite aritmeticke vyrazy
    result = a + b * c - d;
    result = (a + b) * (c - d);
    result = a * b + c * d;
    result = (a + b + c + d) / 4;

    // Slozite logicke vyrazy
    result = (a > b) && (c < d);
    result = (a == 10) || (b == 20);
    result = !(a > b) && (c <= d);
    result = ((a > 0) && (b > 0)) || ((c > 0) && (d > 0));

    // Ternary operator (pokud je podporovan)
    // result = (a > b) ? a : b;

    // Float vyrazy
    f1 = 1.5; f2 = 2.5; f3 = 3.5;
    f3 = f1 + f2 * f3;
    f3 = (f1 + f2) * f3;
}

// Test volani funkci s parametry
int add_numbers(int x, int y) {
    return x + y;
}

float add_floats(float x, float y) {
    return x + y;
}

// Funkce s vice parametry ruznych typu - pro opcodes 41, 42
int multi_param(int a, float b, char c, short d, int e) {
    return a + (int)b + c + d + e;
}

double double_param(double d1, double d2, int i) {
    return d1 + d2 + (double)i;
}

// Funkce prijimajici pointer na strukturu
int accept_struct_ptr(TestStruct *ts) {
    return ts->x + ts->y;
}

void test_function_calls() {
    int a, b, c;
    float f1, f2, f3;

    a = 5;
    b = 10;
    c = add_numbers(a, b);
    c = add_numbers(1, 2);
    c = add_numbers(a + 1, b - 1);

    f1 = 1.5;
    f2 = 2.5;
    f3 = add_floats(f1, f2);
}

// Test slozitejsich volani funkci - pro opcodes 41, 42
void test_multi_param_calls() {
    int result;
    float f;
    char c;
    short s;
    double d1, d2, d3;
    TestStruct ts;

    f = 3.14;
    c = 65;
    s = 100;

    // Volani s vice parametry ruznych typu
    result = multi_param(1, 2.5, 'A', 10, 100);
    result = multi_param(result, f, c, s, result);

    // Volani s double parametry
    d1 = 1.5;
    d2 = 2.5;
    d3 = double_param(d1, d2, 42);
    d3 = double_param(1.0, 2.0, result);

    // Volani se strukturami (pres pointer)
    ts.x = 10;
    ts.y = 20;
    result = accept_struct_ptr(&ts);
}

// Test pointeru a adresovani - pro opcodes 13, 28, 30
void test_pointers() {
    int arr[10];
    int *p;
    int i, val;
    char *str;
    char buffer[32];

    // Pointer aritmetika
    p = arr;
    *p = 100;
    p++;
    *p = 200;
    p = p + 3;
    *p = 500;

    // Indexovani pres pointer
    p = arr;
    for (i = 0; i < 10; i++) {
        p[i] = i * 10;
    }

    // Cteni pres pointer
    val = *p;
    val = *(p + 1);
    val = p[5];

    // Char pointer
    str = buffer;
    *str = 'H';
    str++;
    *str = 'i';
    str[1] = 0;
}

// Test globalnich promennych - pro opcodes 16, 33, 34
void test_globals() {
    int local;
    float f_local;

    // Cteni a zapis globalnich
    g_int1 = 100;
    g_int2 = 200;
    g_int3 = g_int1 + g_int2;

    local = g_int1;
    g_int1 = local * 2;

    // Float globalni
    g_float1 = 1.5;
    g_float2 = 2.5;
    f_local = g_float1 + g_float2;
    g_float1 = f_local;

    // Char a short globalni
    g_char1 = 'A';
    g_char2 = g_char1 + 1;

    g_short1 = 1000;
    g_short2 = g_short1 * 2;

    // Unsigned globalni
    g_uint1 = 0xFFFFFFFF;
    g_uint2 = g_uint1 >> 8;

    // Double globalni
    g_double1 = 3.14159265359;
    g_double2 = g_double1 * 2.0;
}

// Test unsigned operaci - pro opcodes 75, 98
void test_unsigned_ops() {
    unsigned int u1, u2, u3;
    unsigned char uc1, uc2;
    unsigned short us1, us2;
    int i;

    // Unsigned int aritmetika
    u1 = 0xFFFFFFFF;
    u2 = 0x00000001;
    u3 = u1 + u2;   // overflow test
    u3 = u1 - u2;
    u3 = u1 * 2;
    u3 = u1 / 2;
    u3 = u1 % 3;

    // Unsigned shifty
    u3 = u1 >> 16;  // unsigned right shift
    u3 = u1 << 8;

    // Unsigned char
    uc1 = 255;
    uc2 = uc1 + 1;  // overflow

    // Unsigned short
    us1 = 65535;
    us2 = us1 + 1;  // overflow

    // Konverze unsigned <-> signed
    i = (int)u1;
    u1 = (unsigned int)i;
    u1 = (unsigned int)(-1);
}

// Test specialnich konstrukci - pro opcodes 11, 120, 143, 149
void test_special() {
    int a, b, c;
    int arr[5];
    int *p;
    char str1[16], str2[16];

    // Vnorene podminky
    a = 5; b = 10; c = 15;
    if (a > 0) {
        if (b > 0) {
            if (c > 0) {
                a = 1;
            }
        }
    }

    // Slozite short-circuit evaluace
    if ((a > 0) && (b > 0) && (c > 0)) {
        a = 100;
    }

    if ((a < 0) || (b < 0) || (c < 0)) {
        a = 200;
    }

    // Kombinovane podminky
    if (((a > 0) && (b > 0)) || ((c > 0) && (a < 100))) {
        a = 300;
    }

    // Switch s ruznymi hodnotami
    switch (a) {
        case 100:
        case 200:
        case 300:
            b = 1;
            break;
        case 400:
            b = 2;
            // fall through
        case 500:
            b = 3;
            break;
    }

    // Vnoreny switch
    switch (a) {
        case 1:
            switch (b) {
                case 1: c = 10; break;
                case 2: c = 20; break;
            }
            break;
        case 2:
            c = 30;
            break;
    }

    // Vnorene cykly
    for (a = 0; a < 3; a++) {
        for (b = 0; b < 3; b++) {
            arr[0] = a * b;
        }
    }

    // Break a continue
    for (a = 0; a < 10; a++) {
        if (a == 3) continue;
        if (a == 7) break;
        b = a;
    }
}

// Test extern funkci (XFN) - pro opcodes 3, 6, 41, 42
void test_extern_calls() {
    int result;
    void *ptr;
    char *str1, *str2;
    float f;

    // Volani extern funkci se stringy - generuje opcode 3
    SC_message("Test message 1");
    SC_message("Test message 2");
    SC_message("Another test");

    // Volani s vice parametry
    str1 = "string1";
    str2 = "string2";
    f = 3.14;

    // Dalsi extern volani
    SC_P_GetName(0);

    // Pouziti NULL pointeru
    ptr = 0;
    if (ptr == 0) {
        result = 1;
    }
}

// Test rekurzivniho volani
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

void test_recursion() {
    int result;
    result = factorial(5);
    result = factorial(10);
}

// Entry point
int ScriptMain(void *info) {
    test_arithmetic();
    test_double_ops();
    test_comparisons();
    test_logical();
    test_bitwise();
    test_conversions();
    test_char_ops();
    test_short_ops();
    test_arrays();
    test_structs();
    test_switch();
    test_loops();
    test_complex_expressions();
    test_function_calls();
    test_multi_param_calls();
    test_pointers();
    test_globals();
    test_unsigned_ops();
    test_special();
    test_extern_calls();
    test_recursion();
    return 0;
}
