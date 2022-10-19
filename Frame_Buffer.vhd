library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Frame_Buffer is
port(
CLK: in std_logic;

Rout: out std_logic;
Gout: out std_logic;
Bout: out std_logic;

WR: in std_logic;
Rin: in std_logic;
Gin: in std_logic;
Bin: in std_logic;
Xin: in std_logic_vector(9 downto 0);
Yin: in std_logic_vector(9 downto 0);

Xout: in std_logic_vector(9 downto 0);
Yout: in std_logic_vector(9 downto 0)
);
end entity;

architecture arc of Frame_Buffer is
type f_data is array(0 to 640, 0 to 480) of std_logic;
signal f_data_r: f_data := (others => (others =>'1')); --Init white screen
signal f_data_g: f_data := (others => (others =>'1'));
signal f_data_b: f_data := (others => (others =>'1'));
begin

process(CLK)
begin
	if rising_edge(CLK) then
		if WR = '1' then
			f_data_r(to_integer(unsigned(Xin)), to_integer(unsigned(Yin))) <= Rin;
			f_data_g(to_integer(unsigned(Xin)), to_integer(unsigned(Yin))) <= Gin;
			f_data_b(to_integer(unsigned(Xin)), to_integer(unsigned(Yin))) <= Bin;
		end if;
	end if;
end process;

Rout <= f_data_r(to_integer(unsigned(Xout)), to_integer(unsigned(Yout)));
Gout <= f_data_g(to_integer(unsigned(Xout)), to_integer(unsigned(Yout)));
Bout <= f_data_b(to_integer(unsigned(Xout)), to_integer(unsigned(Yout)));


end architecture;