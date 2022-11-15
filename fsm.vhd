library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity fsm is
        Port ( clk : in STD_LOGIC;
               rst : in STD_LOGIC;
               HAZ: in STD_LOGIC;
               LEFT: in STD_LOGIC;
               RIGHT: in STD_LOGIC;
               Q0: out STD_LOGIC;
               Q1: out STD_LOGIC;
               Q2: out STD_LOGIC);
end fsm;

architecture Behavioral of fsm is

type states is (IDLE,R1,L2,R3,L3,LR3,L1,R2);
signal acts,nxts:states:=IDLE;

begin
stateReg:process(clk,rst)
begin
    if rst = '1' then
        acts <= IDLE;
    elsif rising_edge(clk) then
        acts <= nxts;    
    end if;
end process;

combLogic:process(acts,HAZ,LEFT,RIGHT)
begin

case acts is
   when IDLE=>
       if LEFT='1' and HAZ='0' and RIGHT='0' then 
          nxts<= L1;
       elsif (LEFT='1' and RIGHT='1') or HAZ='1' then
          nxts<= LR3;
       elsif RIGHT='1' and HAZ='0' and LEFT='0' then
          nxts<= R1;
       else
          nxts<=IDLE;
       end if;
   when R1=>
       if HAZ='1' then 
          nxts<= LR3;
       else
          nxts<=R2;
       end if;
   when L2=>
       if HAZ='1' then 
          nxts<= LR3;
       else
          nxts<=L3;
       end if;
   when R3=>
       nxts<=IDLE;
   when L3=>
       nxts<=IDLE;
   when LR3=>
       nxts<=IDLE;
   when L1=>
       if HAZ='0' then 
          nxts<= L2;
       else
          nxts<=LR3;
       end if;
   when R2=>
       if HAZ='0' then 
          nxts<= R3;
       else
          nxts<=LR3;
       end if;
   when others=>
       nxts<= IDLE;
end case;
end process;

outputLogic:process(acts,HAZ,LEFT,RIGHT)
begin

case acts is
   when IDLE=>
       Q2<='0';
       Q1<='0';
       Q0<='0';
   when R1=>
       Q2<='1';
       Q1<='0';
       Q0<='1';
   when L2=>
       Q2<='0';
       Q1<='1';
       Q0<='1';
   when R3=>
       Q2<='1';
       Q1<='1';
       Q0<='0';
   when L3=>
       Q2<='0';
       Q1<='1';
       Q0<='0';
   when LR3=>
       Q2<='1';
       Q1<='0';
       Q0<='0';
   when L1=>
       Q2<='0';
       Q1<='0';
       Q0<='1';
   when R2=>
       Q2<='1';
       Q1<='1';
       Q0<='1';
   when others=>
       Q0<='0';
       Q1<='0';
       Q2<='0';
end case;
end process;
end Behavioral;