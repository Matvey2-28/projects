name = 'M_A_T_V_E_Y__M_A_L_I_K_'

for symbol in name:
    print(ord(symbol), end = ', ')
print()

a = [77, 95, 65, 95, 84, 95, 86, 95, 69, 95, 89, 95, 95, 77, 95, 65, 95, 76, 95, 73, 95, 75, 95, ]


name1 = 'm_a_t_v_e_y__m_a_l_i_k_'

for symbol in name1:
    print(ord(symbol), end = ', ')
print()

b = [109, 95, 97, 95, 116, 95, 118, 95, 101, 95, 121, 95, 95, 109, 95, 97, 95, 108, 95, 105, 95, 107, 95, ]

print(min(min(a), min(b)))
print(max(max(a), max(b)))