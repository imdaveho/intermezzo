from intermezzo import Intermezzo as mzo

K_ESC = [{"x": 1, "y": 1, "ch": 'E'}, {"x": 2, "y": 1, "ch": 'S'}, {"x": 3, "y": 1, "ch": 'C'}]
K_F1 = [{"x": 6, "y": 1, "ch": 'F'}, {"x": 7, "y": 1, "ch": '1'}]
K_F2 = [{"x": 9, "y": 1, "ch": 'F'}, {"x": 10, "y": 1, "ch": '2'}]
K_F3 = [{"x": 12, "y": 1, "ch": 'F'}, {"x": 13, "y": 1, "ch": '3'}]
K_F4 = [{"x": 15, "y": 1, "ch": 'F'}, {"x": 16, "y": 1, "ch": '4'}]
K_F5 = [{"x": 19, "y": 1, "ch": 'F'}, {"x": 20, "y": 1, "ch": '5'}]
K_F6 = [{"x": 22, "y": 1, "ch": 'F'}, {"x": 23, "y": 1, "ch": '6'}]
K_F7 = [{"x": 25, "y": 1, "ch": 'F'}, {"x": 26, "y": 1, "ch": '7'}]
K_F8 = [{"x": 28, "y": 1, "ch": 'F'}, {"x": 29, "y": 1, "ch": '8'}]
K_F9 = [{"x": 33, "y": 1, "ch": 'F'}, {"x": 34, "y": 1, "ch": '9'}]
K_F10 = [{"x": 36, "y": 1, "ch": 'F'}, {"x": 37, "y": 1, "ch": '1'}, {"x": 38, "y": 1, "ch": '0'}]
K_F11 = [{"x": 40, "y": 1, "ch": 'F'}, {"x": 41, "y": 1, "ch": '1'}, {"x": 42, "y": 1, "ch": '1'}]
K_F12 = [{"x": 44, "y": 1, "ch": 'F'}, {"x": 45, "y": 1, "ch": '1'}, {"x": 46, "y": 1, "ch": '2'}]
K_PRN = [{"x": 50, "y": 1, "ch": 'P'}, {"x": 51, "y": 1, "ch": 'R'}, {"x": 52, "y": 1, "ch": 'N'}]
K_SCR = [{"x": 54, "y": 1, "ch": 'S'}, {"x": 55, "y": 1, "ch": 'C'}, {"x": 56, "y": 1, "ch": 'R'}]
K_BRK = [{"x": 58, "y": 1, "ch": 'B'}, {"x": 59, "y": 1, "ch": 'R'}, {"x": 60, "y": 1, "ch": 'K'}]
K_LED1 = [{"x": 66, "y": 1, "ch": '-'}]
K_LED2 = [{"x": 70, "y": 1, "ch": '-'}]
K_LED3 = [{"x": 74, "y": 1, "ch": '-'}]
K_TILDE = [{"x": 1, "y": 4, "ch": '`'}]
K_TILDE_SHIFT = [{"x": 1, "y": 4, "ch": '~'}]
K_1 = [{"x": 4, "y": 4, "ch": '1'}]
K_1_SHIFT = [{"x": 4, "y": 4, "ch": '!'}]
K_2 = [{"x": 7, "y": 4, "ch": '2'}]
K_2_SHIFT = [{"x": 7, "y": 4, "ch": '@'}]
K_3 = [{"x": 10, "y": 4, "ch": '3'}]
K_3_SHIFT = [{"x": 10, "y": 4, "ch": '#'}]
K_4 = [{"x": 13, "y": 4, "ch": '4'}]
K_4_SHIFT = [{"x": 13, "y": 4, "ch": '$'}]
K_5 = [{"x": 16, "y": 4, "ch": '5'}]
K_5_SHIFT = [{"x": 16, "y": 4, "ch": '%'}]
K_6 = [{"x": 19, "y": 4, "ch": '6'}]
K_6_SHIFT = [{"x": 19, "y": 4, "ch": '^'}]
K_7 = [{"x": 22, "y": 4, "ch": '7'}]
K_7_SHIFT = [{"x": 22, "y": 4, "ch": '&'}]
K_8 = [{"x": 25, "y": 4, "ch": '8'}]
K_8_SHIFT = [{"x": 25, "y": 4, "ch": '*'}]
K_9 = [{"x": 28, "y": 4, "ch": '9'}]
K_9_SHIFT = [{"x": 28, "y": 4, "ch": '('}]
K_0 = [{"x": 31, "y": 4, "ch": '0'}]
K_0_SHIFT = [{"x": 31, "y": 4, "ch": ')'}]
K_MINUS = [{"x": 34, "y": 4, "ch": '-'}]
K_MINUS_SHIFT = [{"x": 34, "y": 4, "ch": '_'}]
K_EQUALS = [{"x": 37, "y": 4, "ch": '='}]
K_EQUALS_SHIFT = [{"x": 37, "y": 4, "ch": '+'}]
K_BACKSLASH = [{"x": 40, "y": 4, "ch": '\\'}]
K_BACKSLASH_SHIFT = [{"x": 40, "y": 4, "ch": '|'}]
K_BACKSPACE = [{"x": 44, "y": 4, "ch": chr(int("0x2190"))}, {"x": 45, "y": 4, "ch": chr(int("0x2190"))}, {"x": 46, "y": 4, "ch": chr(int("0x2190"))}]
K_INS = [{"x": 50, "y": 4, "ch": 'I'}, {"x": 51, "y": 4, "ch": 'N'}, {"x": 52, "y": 4, "ch": 'S'}]
K_HOM = [{"x": 54, "y": 4, "ch": 'H'}, {"x": 55, "y": 4, "ch": 'O'}, {"x": 56, "y": 4, "ch": 'M'}]
K_PGU = [{"x": 58, "y": 4, "ch": 'P'}, {"x": 59, "y": 4, "ch": 'G'}, {"x": 60, "y": 4, "ch": 'U'}]
K_K_NUMLOCK = [{"x": 65, "y": 4, "ch": 'N'}]
K_K_SLASH = [{"x": 68, "y": 4, "ch": '/'}]
K_K_STAR = [{"x": 71, "y": 4, "ch": '*'}]
K_K_MINUS = [{"x": 74, "y": 4, "ch": '-'}]
K_TAB = [{"x": 1, "y": 6, "ch": 'T'}, {"x": 2, "y": 6, "ch": 'A'}, {"x": 3, "y": 6, "ch": 'B'}]
K_q = [{"x": 6, "y": 6, "ch": 'q'}]
K_Q = [{"x": 6, "y": 6, "ch": 'Q'}]
K_w = [{"x": 9, "y": 6, "ch": 'w'}]
K_W = [{"x": 9, "y": 6, "ch": 'W'}]
K_e = [{"x": 12, "y": 6, "ch": 'e'}]
K_E = [{"x": 12, "y": 6, "ch": 'E'}]
K_r = [{"x": 15, "y": 6, "ch": 'r'}]
K_R = [{"x": 15, "y": 6, "ch": 'R'}]
K_t = [{"x": 18, "y": 6, "ch": 't'}]
K_T = [{"x": 18, "y": 6, "ch": 'T'}]
K_y = [{"x": 21, "y": 6, "ch": 'y'}]
K_Y = [{"x": 21, "y": 6, "ch": 'Y'}]
K_u = [{"x": 24, "y": 6, "ch": 'u'}]
K_U = [{"x": 24, "y": 6, "ch": 'U'}]
K_i = [{"x": 27, "y": 6, "ch": 'i'}]
K_I = [{"x": 27, "y": 6, "ch": 'I'}]
K_o = [{"x": 30, "y": 6, "ch": 'o'}]
K_O = [{"x": 30, "y": 6, "ch": 'O'}]
K_p = [{"x": 33, "y": 6, "ch": 'p'}]
K_P = [{"x": 33, "y": 6, "ch": 'P'}]
K_LSQB = [{"x": 36, "y": 6, "ch": '['}]
K_LCUB = [{"x": 36, "y": 6, "ch": '{"x": '}]
K_RSQB = [{"x": 39, "y": 6, "ch": ']'}]
K_RCUB = [{"x": 39, "y": 6, "ch": '}'}]
K_ENTER = [
	{"x": 43, "y": 6, "ch": chr(int("0x2591", 16))}, {"x": 44, "y": 6, "ch": chr(int("0x2591", 16))},
    {"x": 45, "y": 6, "ch": chr(int("0x2591", 16))}, {"x": 46, "y": 6, "ch": chr(int("0x2591", 16))},
	{"x": 43, "y": 7, "ch": chr(int("0x2591", 16))}, {"x": 44, "y": 7, "ch": chr(int("0x2591", 16))},
    {"x": 45, "y": 7, "ch": chr(int("0x21B5", 16))}, {"x": 46, "y": 7, "ch": chr(int("0x2591", 16))},
	{"x": 41, "y": 8, "ch": chr(int("0x2591", 16))}, {"x": 42, "y": 8, "ch": chr(int("0x2591", 16))},
    {"x": 43, "y": 8, "ch": chr(int("0x2591", 16))}, {"x": 44, "y": 8, "ch": chr(int("0x2591", 16))},
	{"x": 45, "y": 8, "ch": chr(int("0x2591", 16))}, {"x": 46, "y": 8, "ch": chr(int("0x2591", 16))},
]
K_DEL = [{"x": 50, "y": 6, "ch": 'D'}, {"x": 51, "y": 6, "ch": 'E'}, {"x": 52, "y": 6, "ch": 'L'}]
K_END = [{"x": 54, "y": 6, "ch": 'E'}, {"x": 55, "y": 6, "ch": 'N'}, {"x": 56, "y": 6, "ch": 'D'}]
K_PGD = [{"x": 58, "y": 6, "ch": 'P'}, {"x": 59, "y": 6, "ch": 'G'}, {"x": 60, "y": 6, "ch": 'D'}]
K_K_7 = [{"x": 65, "y": 6, "ch": '7'}]
K_K_8 = [{"x": 68, "y": 6, "ch": '8'}]
K_K_9 = [{"x": 71, "y": 6, "ch": '9'}]
K_K_PLUS = [{"x": 74, "y": 6, "ch": ' '}, {"x": 74, "y": 7, "ch": '+'}, {"x": 74, "y": 8, "ch": ' '}]
K_CAPS = [{"x": 1, "y": 8, "ch": 'C'}, {"x": 2, "y": 8, "ch": 'A'}, {"x": 3, "y": 8, "ch": 'P'}, {"x": 4, "y": 8, "ch": 'S'}]
K_a = [{"x": 7, "y": 8, "ch": 'a'}]
K_A = [{"x": 7, "y": 8, "ch": 'A'}]
K_s = [{"x": 10, "y": 8, "ch": 's'}]
K_S = [{"x": 10, "y": 8, "ch": 'S'}]
K_d = [{"x": 13, "y": 8, "ch": 'd'}]
K_D = [{"x": 13, "y": 8, "ch": 'D'}]
K_f = [{"x": 16, "y": 8, "ch": 'f'}]
K_F = [{"x": 16, "y": 8, "ch": 'F'}]
K_g = [{"x": 19, "y": 8, "ch": 'g'}]
K_G = [{"x": 19, "y": 8, "ch": 'G'}]
K_h = [{"x": 22, "y": 8, "ch": 'h'}]
K_H = [{"x": 22, "y": 8, "ch": 'H'}]
K_j = [{"x": 25, "y": 8, "ch": 'j'}]
K_J = [{"x": 25, "y": 8, "ch": 'J'}]
K_k = [{"x": 28, "y": 8, "ch": 'k'}]
K_K = [{"x": 28, "y": 8, "ch": 'K'}]
K_l = [{"x": 31, "y": 8, "ch": 'l'}]
K_L = [{"x": 31, "y": 8, "ch": 'L'}]
K_SEMICOLON = [{"x": 34, "y": 8, "ch": ';'}]
K_PARENTHESIS = [{"x": 34, "y": 8, "ch": ':'}]
K_QUOTE = [{"x": 37, "y": 8, "ch": '\''}]
K_DOUBLEQUOTE = [{"x": 37, "y": 8, "ch": '"'}]
K_K_4 = [{"x": 65, "y": 8, "ch": '4'}]
K_K_5 = [{"x": 68, "y": 8, "ch": '5'}]
K_K_6 = [{"x": 71, "y": 8, "ch": '6'}]
K_LSHIFT = [
    {"x": 1, "y": 10, "ch": 'S'},
    {"x": 2, "y": 10, "ch": 'H'},
    {"x": 3, "y": 10, "ch": 'I'},
    {"x": 4, "y": 10, "ch": 'F'},
    {"x": 5, "y": 10, "ch": 'T'}
]
K_z = [{"x": 9, "y": 10, "ch": 'z'}]
K_Z = [{"x": 9, "y": 10, "ch": 'Z'}]
K_x = [{"x": 12, "y": 10, "ch": 'x'}]
K_X = [{"x": 12, "y": 10, "ch": 'X'}]
K_c = [{"x": 15, "y": 10, "ch": 'c'}]
K_C = [{"x": 15, "y": 10, "ch": 'C'}]
K_v = [{"x": 18, "y": 10, "ch": 'v'}]
K_V = [{"x": 18, "y": 10, "ch": 'V'}]
K_b = [{"x": 21, "y": 10, "ch": 'b'}]
K_B = [{"x": 21, "y": 10, "ch": 'B'}]
K_n = [{"x": 24, "y": 10, "ch": 'n'}]
K_N = [{"x": 24, "y": 10, "ch": 'N'}]
K_m = [{"x": 27, "y": 10, "ch": 'm'}]
K_M = [{"x": 27, "y": 10, "ch": 'M'}]
K_COMMA = [{"x": 30, "y": 10, "ch": ','}]
K_LANB = [{"x": 30, "y": 10, "ch": '<'}]
K_PERIOD = [{"x": 33, "y": 10, "ch": '.'}]
K_RANB = [{"x": 33, "y": 10, "ch": '>'}]
K_SLASH = [{"x": 36, "y": 10, "ch": '/'}]
K_QUESTION = [{"x": 36, "y": 10, "ch": '?'}]
K_RSHIFT = [
    {"x": 42, "y": 10, "ch": 'S'},
    {"x": 43, "y": 10, "ch": 'H'},
    {"x": 44, "y": 10, "ch": 'I'},
    {"x": 45, "y": 10, "ch": 'F'},
    {"x": 46, "y": 10, "ch": 'T'}
]
K_ARROW_UP = [{"x": 54, "y": 10, "ch": '('}, {"x": 55, "y": 10, "ch": chr(int("0x2191", 16))}, {"x": 56, "y": 10, "ch": ')'}]
K_K_1 = [{"x": 65, "y": 10, "ch": '1'}]
K_K_2 = [{"x": 68, "y": 10, "ch": '2'}]
K_K_3 = [{"x": 71, "y": 10, "ch": '3'}]
K_K_ENTER = [
    {"x": 74, "y": 10, "ch": chr(int("0x2591", 16))},
    {"x": 74, "y": 11, "ch": chr(int("0x2591", 16))},
    {"x": 74, "y": 12, "ch": chr(int("0x2591", 16))}
]
K_LCTRL = [{"x": 1, "y": 12, "ch": 'C'}, {"x": 2, "y": 12, "ch": 'T'}, {"x": 3, "y": 12, "ch": 'R'}, {"x": 4, "y": 12, "ch": 'L'}]
K_LWIN = [{"x": 6, "y": 12, "ch": 'W'}, {"x": 7, "y": 12, "ch": 'I'}, {"x": 8, "y": 12, "ch": 'N'}]
K_LALT = [{"x": 10, "y": 12, "ch": 'A'}, {"x": 11, "y": 12, "ch": 'L'}, {"x": 12, "y": 12, "ch": 'T'}]
K_SPACE = [
	{"x": 14, "y": 12, "ch": ' '}, {"x": 15, "y": 12, "ch": ' '}, {"x": 16, "y": 12, "ch": ' '},
    {"x": 17, "y": 12, "ch": ' '}, {"x": 18, "y": 12, "ch": ' '}, {"x": 19, "y": 12, "ch": 'S'},
    {"x": 20, "y": 12, "ch": 'P'}, {"x": 21, "y": 12, "ch": 'A'}, {"x": 22, "y": 12, "ch": 'C'},
    {"x": 23, "y": 12, "ch": 'E'}, {"x": 24, "y": 12, "ch": ' '}, {"x": 25, "y": 12, "ch": ' '},
    {"x": 26, "y": 12, "ch": ' '}, {"x": 27, "y": 12, "ch": ' '}, {"x": 28, "y": 12, "ch": ' '},
]
K_RALT = [{"x": 30, "y": 12, "ch": 'A'}, {"x": 31, "y": 12, "ch": 'L'}, {"x": 32, "y": 12, "ch": 'T'}]
K_RWIN = [{"x": 34, "y": 12, "ch": 'W'}, {"x": 35, "y": 12, "ch": 'I'}, {"x": 36, "y": 12, "ch": 'N'}]
K_RPROP = [{"x": 38, "y": 12, "ch": 'P'}, {"x": 39, "y": 12, "ch": 'R'}, {"x": 40, "y": 12, "ch": 'O'}, {"x": 41, "y": 12, "ch": 'P'}]
K_RCTRL = [{"x": 43, "y": 12, "ch": 'C'}, {"x": 44, "y": 12, "ch": 'T'}, {"x": 45, "y": 12, "ch": 'R'}, {"x": 46, "y": 12, "ch": 'L'}]
K_ARROW_LEFT = [{"x": 50, "y": 12, "ch": '('}, {"x": 51, "y": 12, "ch": chr(int("0x2190", 16))}, {"x": 52, "y": 12, "ch": ')'}]
K_ARROW_DOWN = [{"x": 54, "y": 12, "ch": '('}, {"x": 55, "y": 12, "ch": chr(int("0x2193", 16))}, {"x": 56, "y": 12, "ch": ')'}]
K_ARROW_RIGHT = [{"x": 58, "y": 12, "ch": '('}, {"x": 59, "y": 12, "ch": chr(int("0x2192", 16))}, {"x": 60, "y": 12, "ch": ')'}]
K_K_0 = [{"x": 65, "y": 12, "ch": ' '}, {"x": 66, "y": 12, "ch": '0'}, {"x": 67, "y": 12, "ch": ' '}, {"x": 68, "y": 12, "ch": ' '}]
K_K_PERIOD = [{"x": 71, "y": 12, "ch": '.'}]

combos = [
    [K_TILDE, K_2, K_SPACE, K_LCTRL, K_RCTRL],
    [K_A, K_LCTRL, K_RCTRL]
    [K_B, K_LCTRL, K_RCTRL],
	[K_C, K_LCTRL, K_RCTRL],
	[K_D, K_LCTRL, K_RCTRL],
	[K_E, K_LCTRL, K_RCTRL],
	[K_F, K_LCTRL, K_RCTRL],
	[K_G, K_LCTRL, K_RCTRL],
	[K_H, K_BACKSPACE, K_LCTRL, K_RCTRL],
	[K_I, K_TAB, K_LCTRL, K_RCTRL],
	[K_J, K_LCTRL, K_RCTRL],
	[K_K, K_LCTRL, K_RCTRL],
	[K_L, K_LCTRL, K_RCTRL],
	[K_M, K_ENTER, K_K_ENTER, K_LCTRL, K_RCTRL],
	[K_N, K_LCTRL, K_RCTRL],
	[K_O, K_LCTRL, K_RCTRL],
	[K_P, K_LCTRL, K_RCTRL],
	[K_Q, K_LCTRL, K_RCTRL],
	[K_R, K_LCTRL, K_RCTRL],
	[K_S, K_LCTRL, K_RCTRL],
	[K_T, K_LCTRL, K_RCTRL],
	[K_U, K_LCTRL, K_RCTRL],
	[K_V, K_LCTRL, K_RCTRL],
	[K_W, K_LCTRL, K_RCTRL],
	[K_X, K_LCTRL, K_RCTRL],
	[K_Y, K_LCTRL, K_RCTRL],
	[K_Z, K_LCTRL, K_RCTRL],
	[K_LSQB, K_ESC, K_3, K_LCTRL, K_RCTRL],
	[K_4, K_BACKSLASH, K_LCTRL, K_RCTRL],
	[K_RSQB, K_5, K_LCTRL, K_RCTRL],
	[K_6, K_LCTRL, K_RCTRL],
	[K_7, K_SLASH, K_MINUS_SHIFT, K_LCTRL, K_RCTRL],
	[K_SPACE],
	[K_1_SHIFT, K_LSHIFT, K_RSHIFT],
	[K_DOUBLEQUOTE, K_LSHIFT, K_RSHIFT],
	[K_3_SHIFT, K_LSHIFT, K_RSHIFT],
	[K_4_SHIFT, K_LSHIFT, K_RSHIFT],
	[K_5_SHIFT, K_LSHIFT, K_RSHIFT],
	[K_7_SHIFT, K_LSHIFT, K_RSHIFT],
	[K_QUOTE],
	[K_9_SHIFT, K_LSHIFT, K_RSHIFT],
	[K_0_SHIFT, K_LSHIFT, K_RSHIFT],
	[K_8_SHIFT, K_K_STAR, K_LSHIFT, K_RSHIFT],
	[K_EQUALS_SHIFT, K_K_PLUS, K_LSHIFT, K_RSHIFT],
	[K_COMMA],
	[K_MINUS, K_K_MINUS],
	[K_PERIOD, K_K_PERIOD],
	[K_SLASH, K_K_SLASH],
	[K_0, K_K_0],
	[K_1, K_K_1],
	[K_2, K_K_2],
	[K_3, K_K_3],
	[K_4, K_K_4],
	[K_5, K_K_5],
	[K_6, K_K_6],
	[K_7, K_K_7],
	[K_8, K_K_8],
	[K_9, K_K_9],
	[K_PARENTHESIS, K_LSHIFT, K_RSHIFT],
	[K_SEMICOLON],
	[K_LANB, K_LSHIFT, K_RSHIFT],
	[K_EQUALS],
	[K_RANB, K_LSHIFT, K_RSHIFT],
	[K_QUESTION, K_LSHIFT, K_RSHIFT],
	[K_2_SHIFT, K_LSHIFT, K_RSHIFT],
	[K_A, K_LSHIFT, K_RSHIFT],
	[K_B, K_LSHIFT, K_RSHIFT],
	[K_C, K_LSHIFT, K_RSHIFT],
	[K_D, K_LSHIFT, K_RSHIFT],
	[K_E, K_LSHIFT, K_RSHIFT],
	[K_F, K_LSHIFT, K_RSHIFT],
	[K_G, K_LSHIFT, K_RSHIFT],
	[K_H, K_LSHIFT, K_RSHIFT],
	[K_I, K_LSHIFT, K_RSHIFT],
	[K_J, K_LSHIFT, K_RSHIFT],
	[K_K, K_LSHIFT, K_RSHIFT],
	[K_L, K_LSHIFT, K_RSHIFT],
	[K_M, K_LSHIFT, K_RSHIFT],
	[K_N, K_LSHIFT, K_RSHIFT],
	[K_O, K_LSHIFT, K_RSHIFT],
	[K_P, K_LSHIFT, K_RSHIFT],
	[K_Q, K_LSHIFT, K_RSHIFT],
	[K_R, K_LSHIFT, K_RSHIFT],
	[K_S, K_LSHIFT, K_RSHIFT],
	[K_T, K_LSHIFT, K_RSHIFT],
	[K_U, K_LSHIFT, K_RSHIFT],
	[K_V, K_LSHIFT, K_RSHIFT],
	[K_W, K_LSHIFT, K_RSHIFT],
	[K_X, K_LSHIFT, K_RSHIFT],
	[K_Y, K_LSHIFT, K_RSHIFT],
	[K_Z, K_LSHIFT, K_RSHIFT],
	[K_LSQB],
	[K_BACKSLASH],
	[K_RSQB],
	[K_6_SHIFT, K_LSHIFT, K_RSHIFT],
	[K_MINUS_SHIFT, K_LSHIFT, K_RSHIFT],
	[K_TILDE],
	[K_a],
	[K_b],
	[K_c],
	[K_d],
	[K_e],
	[K_f],
	[K_g],
	[K_h],
	[K_i],
	[K_j],
	[K_k],
	[K_l],
	[K_m],
	[K_n],
	[K_o],
	[K_p],
	[K_q],
	[K_r],
	[K_s],
	[K_t],
	[K_u],
	[K_v],
	[K_w],
	[K_x],
	[K_y],
	[K_z],
	[K_LCUB, K_LSHIFT, K_RSHIFT],
	[K_BACKSLASH_SHIFT, K_LSHIFT, K_RSHIFT],
	[K_RCUB, K_LSHIFT, K_RSHIFT],
	[K_TILDE_SHIFT, K_LSHIFT, K_RSHIFT],
    [K_8, K_BACKSPACE, K_LCTRL, K_RCTRL],
]

func_combos = [
    [K_F1],
	[K_F2],
	[K_F3],
	[K_F4],
	[K_F5],
	[K_F6],
	[K_F7],
	[K_F8],
	[K_F9],
	[K_F10],
	[K_F11],
	[K_F12],
	[K_INS],
	[K_DEL],
	[K_HOM],
	[K_END],
	[K_PGU],
	[K_PGD],
	[K_ARROW_UP],
	[K_ARROW_DOWN],
	[K_ARROW_LEFT],
    [K_ARROW_RIGHT],
]


def print_tb(x, y, fg, bg, msg):
    for c in msg:
        mzo.set_cell(x, y, c, fg, bg)
        x+=1

def printf_tb(x, y, fg, bg, fmt, *args):
    s = 
