library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Frame_Buffer is
port(
CLK: in std_logic;
--WR: in std_logic;

Rout: out std_logic;
Gout: out std_logic;
Bout: out std_logic;

--Rin: in std_logic;
--Gin: in std_logic;
--Bin: in std_logic;

Xout: in std_logic_vector(9 downto 0);
Yout: in std_logic_vector(9 downto 0)
);
end entity;

architecture arc of Frame_Buffer is
type f_data is array(0 to 640, 0 to 480) of std_logic;
signal f_data_r: f_data;
signal f_data_g: f_data;
signal f_data_b: f_data;
begin

process(CLK)
begin
	if rising_edge(CLK) then
		--if WR = '1' then
			
			--Rout <= '1';
		--end if;
	end if;
end process;

process
begin
	for x in 0 to 640 loop
		for y in 0 to 480 loop
			if x < 100 and y < 100 then
				f_data_r(x, y) <= '1';
				f_data_g(x, y) <= '0';
				f_data_b(x, y) <= '0';
				
			else
				f_data_r(x, y) <= '1';
				f_data_g(x, y) <= '1';
				f_data_b(x, y) <= '1';
			end if;
		end loop;
	end loop;
wait;
end process;

Rout <= f_data_r(to_integer(unsigned(Xout)), to_integer(unsigned(Yout)));
Gout <= f_data_g(to_integer(unsigned(Xout)), to_integer(unsigned(Yout)));
Bout <= f_data_b(to_integer(unsigned(Xout)), to_integer(unsigned(Yout)));


end architecture;