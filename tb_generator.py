def generate_tb(entity, states, states_transitions, transitions, inout,list_of_outputs,list_of_inputs,name_of_fsm):
    entity_cp = ''
    entity_cp += entity
    clkfreq = 10  # clock frequency in ns

    print(entity)
    print(states)
    print(states_transitions)
    print(transitions)
    print(inout)

    testbench = ''
    testbench += 'library IEEE;\nuse IEEE.STD_LOGIC_1164.ALL;\n\n'
    testbench += 'entity ' + name_of_fsm + '_tb is\nend ' + name_of_fsm + '_tb;\n\n'
    testbench += 'architecture Behavioral of mealy_tb is\n\n'


    # Component
    start_aux = entity_cp.find('entity')
    end_aux = entity_cp.find('end')
    aux_str = entity_cp[start_aux+len('entity'):end_aux]
    testbench += 'component'

    testbench += aux_str.replace(name_of_fsm, name_of_fsm)
    testbench += 'end component;\n'

    # Create signals
    testbench+= 'signal '

    for i in list_of_inputs:
        testbench += 's'+i + ','

    testbench = testbench[:-1]+" :std_logic:='0';\n"

    testbench += 'signal '
    testbench += 'sclk,srst,'
    for i in list_of_outputs:
        testbench += 's'+i[:-1] + ','
    testbench = testbench[:-1] + " :std_logic:='0';\n\n"

    testbench += 'begin\n\n'
    #signal control

    testbench += f'sclk<= not sclk after {int(clkfreq/2)}ns;\n'
    testbench += f"srst<= '1','0' after {int(5*clkfreq)}ns;\n"

    # component instanciation

    testbench += '\nuut: '+name_of_fsm+' Port map(\n'
    testbench += '      clk=>sclk,\n'
    testbench += '      rst=>srst,\n'

    for i in list_of_outputs:
        testbench += '      '+i[:-1]+'=>s'+i[:-1]+',\n'

    for i in list_of_inputs:
        testbench += '      ' + i + '=>s' + i + ',\n'

    testbench = testbench[:-2]+');\n\n'
    testbench += 'end Behavioral;'

    print(testbench)




