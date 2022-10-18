library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std;

entity TB is

end entity;

architecture arc of TB is
signal CLK : std_logic;
signal R : std_logic;
signal G : std_logic;
signal B : std_logic;
signal V: std_logic;
signal H: std_logic;

component VGA_Sync is
port(
CLK: in std_logic;
R: out std_logic;
G: out std_logic;
B: out std_logic;
HS : out std_logic;
VS : out std_logic
);
end component;
begin

vgaSync : VGA_Sync port map(R => R, G => G, B => B, VS => V, HS => H, CLK => CLK);



process
begin
	CLK <= '0';
	wait for 20ns;
	CLK <= '1';
	wait for 20ns;

end process;


end architecture;