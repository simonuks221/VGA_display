library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Graphics_pipeline_SM is
port(
EN : in std_logic;
RST: in std_logic;
CLK : in std_logic;

DONE_RASTERISATION: in std_logic;

EN_VGA: out std_logic;
EN_RASTERISATION: out std_logic
);
end entity;

architecture arc of Graphics_pipeline_SM is
type Gstate is (IDLE, RASTERISING, DISPLAYING);
signal state : Gstate := IDLE;
signal nextState : Gstate := RASTERISING;
begin

process (CLK)
begin
	if RST = '1' then
		state <= IDLE;
	elsif rising_edge(CLK) then
	report "CLK";
		state <= nextState; 
	end if;
end process;

process (state, DONE_RASTERISATION)
begin
	case state is
		when IDLE =>
			nextState <= RASTERISING;
		when RASTERISING =>
			EN_RASTERISATION <= '1';
			if Done_RASTERISATION = '1' then
				nextState <= DISPLAYING;
				EN_RASTERISATION <= '0';
			end if;
		when DISPLAYING => 
			EN_VGA <= '1';
			EN_RASTERISATION <= '0';
			--Do nothing for the time beeing
		when others =>
			nextState <= IDLE;
			EN_RASTERISATION <= '0';
			EN_VGA <= '0';
	end case;
end process;

end architecture;