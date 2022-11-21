library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity mealy is
        Port ( clk : in STD_LOGIC;
               rst : in STD_LOGIC;
               button: in STD_LOGIC;
               s1: out STD_LOGIC;
               s2: out STD_LOGIC);
end mealy;

architecture Behavioral of mealy is

type states is (A,B,C);
signal acts,nxts:states:=A;

begin
stateReg:process(clk,rst)
begin
    if rst = '1' then
        acts <= A;
    elsif rising_edge(clk) then
        acts <= nxts;    
    end if;
end process;

combLogic:process(acts,button)
begin

case acts is
   when A=>
       if button='1' then 
          nxts<= B;
       else
          nxts<=A;
       end if;
   when B=>
       if button='1' then 
          nxts<= C;
       else
          nxts<=A;
       end if;
   when C=>
       if button='0' then 
          nxts<= A;
       else
          nxts<=C;
       end if;
   when others=>
       nxts<= A;
end case;
end process;

outputLogic:process(acts,button)
begin

case acts is
   when A=>

       if button='1' then 
             s1<='0';
             s2<='1';
       else
             s1<='0';
             s2<='0';
       end if;
   when B=>

       if button='1' then 
             s1<='1';
             s2<='0';
       else
             s1<='0';
             s2<='1';
       end if;
   when C=>

       if button='0' then 
             s1<='0';
             s2<='1';
       else
             s1<='1';
             s2<='0';
       end if;
   when others=>
       s1<='0';
       s2<='0';
end case;
end process;
end Behavioral;