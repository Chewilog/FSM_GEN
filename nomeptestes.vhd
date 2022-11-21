library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity nomeptestes is
        Port ( clk : in STD_LOGIC;
               rst : in STD_LOGIC;
               valid: in STD_LOGIC;
               start: in STD_LOGIC;
               aux: in STD_LOGIC;
               nsei: in STD_LOGIC;
               clr: out STD_LOGIC;
               en: out STD_LOGIC;
               inc: out STD_LOGIC;
               s1: out STD_LOGIC;
               s2: out STD_LOGIC;
               s3: out STD_LOGIC);
end nomeptestes;

architecture Behavioral of nomeptestes is

type states is (E0,E1,E2,E4);
signal acts,nxts:states:=E0;

begin
stateReg:process(clk,rst)
begin
    if rst = '1' then
        acts <= E0;
    elsif rising_edge(clk) then
        acts <= nxts;    
    end if;
end process;

combLogic:process(acts,aux,nsei,start,valid)
begin

case acts is
   when E0=>
       if start='1' and aux='1' then 
          nxts<= E2;
       elsif ((valid='0' and start='0') or aux='0') and valid='1' then
          nxts<= E1;
       else
          nxts<=E0;
       end if;
   when E1=>
       nxts<=E2;
   when E2=>
       if nsei='1' then 
          nxts<= E4;
       else
          nxts<=E0;
       end if;
   when E4=>
       nxts<=E2;
   when others=>
       nxts<= E0;
end case;
end process;

outputLogic:process(acts,aux,nsei,start,valid)
begin

case acts is
   when E0=>
       clr<='1';
       en<='0';
       inc<='0';

       if start='1' and aux='1' then 
             s1<='0';
             s2<='1';
             s3<='1';
       elsif ((valid='0' and start='0') or aux='0') and valid='1' then
             s1<='1';
             s2<='1';
             s3<='1';
       else
             s1<='0';
             s2<='0';
             s3<='0';
       end if;
   when E1=>
       clr<='0';
       en<='1';
       inc<='0';
       s1<='0';
       s2<='0';
       s3<='0';
   when E2=>
       clr<='0';
       en<='0';
       inc<='1';

       if nsei='1' then 
             s1<='1';
             s2<='0';
             s3<='0';
       else
             s1<='1';
             s2<='1';
             s3<='0';
       end if;
   when E4=>
       clr<='0';
       en<='1';
       inc<='1';
       s1<='0';
       s2<='1';
       s3<='0';
   when others=>
       clr<='0';
       en<='0';
       inc<='0';
       s1<='0';
       s2<='0';
       s3<='0';
end case;
end process;
end Behavioral;