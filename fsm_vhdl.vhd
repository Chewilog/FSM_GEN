library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity fsm_vhdl is
        Port ( clk : in STD_LOGIC;
               rst : in STD_LOGIC;
               start: in STD_LOGIC;
               x: out STD_LOGIC);
end fsm_vhdl;

architecture Behavioral of fsm_vhdl is

type states is (DES,LIG1,LIG2,LIG3);
signal acts,nxts:states:=DES;

begin
stateReg:process(clk,rst)
begin
    if rst = '1' then
        acts <= DES;
    elsif rising_edge(clk) then
        acts <= nxts;    
    end if;
end process;

combLogic:process(acts,start)
begin

case acts is
   when DES=>
       if start='1' then 
          nxts<= LIG1;
       else
          nxts<=DES;
       end if;
   when LIG1=>
       nxts<=LIG2;
   when LIG2=>
       nxts<=LIG3;
   when LIG3=>
       nxts<=DES;
end case;
end process;

outputLogic:process(acts,start)
begin

case acts is
   when DES=>
       x<='0';
   when LIG1=>
       x<='1';
   when LIG2=>
       x<='1';
   when LIG3=>
       x<='1';
end case;
end process;
end Behavioral;