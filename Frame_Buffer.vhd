library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Frame_Buffer is
port(
CLK: in std_logic;

RGBout: out std_logic_vector(0 to 2);

WR: in std_logic;
RGBin: in std_logic_vector(0 to 2);
Xin: in std_logic_vector(9 downto 0);
Yin: in std_logic_vector(9 downto 0);

Xout: in std_logic_vector(9 downto 0);
Yout: in std_logic_vector(9 downto 0)
);
end entity;

architecture arc of Frame_Buffer is
type f_data is array(0 to 640, 0 to 480) of std_logic_vector(0 to 2);
signal f_data_RGB: f_data := (others => (others => (others => '1'))); --Init white screen
begin

process(CLK)
begin
	if rising_edge(CLK) then
		if WR = '1' then
			f_data_RGB(to_integer(unsigned(Xin)), to_integer(unsigned(Yin))) <= RGBin;
		end if;
	end if;
end process;

RGBout <= f_data_RGB(to_integer(unsigned(Xout)), to_integer(unsigned(Yout)));


end architecture;