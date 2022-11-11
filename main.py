# This is a sample Python script.
import xml.etree.ElementTree as ET
import sys
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
AND_OP = "&"
OR_OP = "|"


# a -> 0 ; A -> 1 | a = not A


def translate_expression(expression, variables):
    expression = expression.replace("amp;", '')
    aux = ''
    var_dict = {}
    for i in variables:
        a = i.split('=')
        var_dict[a[0]] = a[1]
    for i in expression:
        if i.lower() in var_dict.keys():
            if i.islower():
                aux += var_dict[i.lower()] + '=\'0\''
            else:
                aux += var_dict[i.lower()] + '=\'1\''

        elif i=='|':
            aux += ' or '
            
        elif i=='&':
            
            aux += ' and '
        else:
            aux += i


    #for i in expression



    return aux


def generate(file2open, name_of_fsm):
    # Use a breakpoint in the code line below to debug your script.
    entity = '''library IEEE;\nuse IEEE.STD_LOGIC_1164.ALL;\n\n'''
    entity += '''entity FSM is
        Port ( clk : in STD_LOGIC;
               rst : in STD_LOGIC;'''
    entity += '\n'
    entity_end = "end FSM;\n"
    behave_begin = "\narchitecture Behavioral of FSM is\n"
    statereg_begin = '''stateReg:process(clk,rst)
begin
    if rst = '1' then
        acts <= '''
    statereg_end = '''elsif rising_edge(clk) then
        acts <= nxts;    
    end if;
end process;'''

    states = {}
    states_transitions = {}
    transitions = {}
    inout = {}

    name = name_of_fsm
    entity = entity.replace("FSM", name)

    entity_end = entity_end.replace("FSM", name)
    behave_begin = behave_begin.replace("FSM", name)

    tree = ET.parse(file2open)
    # root = ET.fromstring(country_data_as_string)  --Direto da string
    root = tree.getroot()

    list_of_outputs = []
    list_of_inputs = []
    for child in root[0]:
        dict_child = child.attrib
        if len(dict_child['id']) > 5:
            if 'whiteSpace=wrap' in dict_child['style']:

                try:
                    states[dict_child['id']] = dict_child['value']
                except:
                    states[dict_child['id']] = "000000"
                states_transitions[dict_child['id']] = []
            elif 'endArrow' in dict_child['style'] or 'orthogonalEdgeStyle' in dict_child['style']:

                try:
                    transitions[dict_child['id']] = (dict_child['source'], dict_child['target'], dict_child['value'])
                except:
                    transitions[dict_child['id']] = (dict_child['source'], dict_child['target'], '000000')

            elif 'swimlane' in dict_child['style']:

                inout[dict_child['id']] = (dict_child['value'], [])

            elif 'text' in dict_child['style']:
                inout[dict_child['parent']][1].append(dict_child['value'])
                if inout[dict_child['parent']][0] != 'Variables':
                    list_of_outputs.append(dict_child['value'].split('=')[0])
                if inout[dict_child['parent']][0] == 'Variables':
                    list_of_inputs.append(dict_child['value'].split('=')[1])
                    var_location = dict_child['parent']

    list_of_outputs = set(list_of_outputs)
    list_of_inputs = set(list_of_inputs)

    for key in transitions.keys():
        states_transitions[transitions[key][0]].append(key)


    # my_inverted_dict = dict(map(reversed, my_dict.items()))

    for key in inout.keys():
        if 'Variables' == inout[key][0]:
            for i in inout[key][1]:
                entity += '               ' + i.split('=')[1]+': in STD_LOGIC;\n'
    for i in list_of_outputs:
        entity += '               ' + i[:-1] + ': out STD_LOGIC;\n'
    entity = entity[:-2]
    entity +=');\n'+ entity_end+behave_begin+'\n'
    entity += 'type states is ('

    for key in states.keys():
        entity += states[key]+','
    entity = entity[:-1]+');\n'
    entity.replace('<', '')
    entity += 'signal acts,nxts:states:='+states[list(states.keys())[0]] + ';\n'

    entity += '\nbegin\n'
    entity += statereg_begin+states[list(states.keys())[0]] + ';\n    '
    entity += statereg_end+'\n'

    process_head = "\ncombLogic:process(acts,"
    for i in list_of_inputs:
        process_head += i+','
    process_head = process_head[:-1] + ")\nbegin\n"
    entity += process_head

    entity += "\ncase acts is\n"

    for key in states.keys():
        entity += "   when " + states[key] + "=>\n"
        if len(states_transitions[key]) == 1:
            entity += "       nxts<=" + states[transitions[states_transitions[key][0]][1]] + ";\n"
        else:
            cnt = 0
            size = len(list(states_transitions[key]))

            for transition in states_transitions[key]:

                if transitions[transition][2] == 'else':
                    aux = transitions[transition][1]
                    
                else:
                    if cnt == 0:
                        entity += '       if ' + translate_expression(transitions[transition][2], inout[var_location][1]) + ' then \n'
                        entity += '          nxts<= ' + states[transitions[transition][1]] + ';\n'
                        cnt += 1
                        
                    elif cnt<size-1 and cnt>0:
                        entity += '       elsif ' + translate_expression(transitions[transition][2], inout[var_location][1]) + ' then\n'
                        entity += '          nxts<= ' + states[transitions[transition][1]] + ';\n'
                        cnt += 1

            entity += '       else\n          nxts<='+states[aux]+';\n'
            entity += '       end if;\n'
    print(states[list(states.keys())[0]])
    entity += "   when others=>\n"
    entity += '       nxts<= '+states[list(states.keys())[0]]+';\n'
    entity += 'end case;\n'
    entity += 'end process;\n'

    process_head = "\noutputLogic:process(acts,"
    for i in list_of_inputs:
        process_head += i + ','
    process_head = process_head[:-1] + ")\nbegin\n"
    entity += process_head
    entity += "\ncase acts is\n"

    for key in states.keys():

        entity += "   when " + states[key] + "=>\n"
        for i in inout.keys():
            if inout[i][0] == states[key]:
                for output in inout[i][1]:
                    entity+='       ' + output+';\n'

    entity += "   when others=>\n"
    for i in inout[list(inout.keys())[1]][1]:#possivel fonte de erro
        #print(i.split("<=")[0]+"<='0';")
        entity += "       "+i.split("<=")[0]+"<='0';\n"
    #print(inout[list(inout.keys())[0]][1])
    #print(entity)
    entity += 'end case;\n'
    entity += 'end process;\n'
    entity+='end Behavioral;'

    file = open(name+'.vhd', 'w')
    print(entity)
    file.write(entity)
    file.close()


#generate(str(sys.argv[1]), str(sys.argv[2]))
print("File ready! Please check the reset state as it is \"randomly\" chosen.")
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
     generate('teste.xml', 'fsm')
