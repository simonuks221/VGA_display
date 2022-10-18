library ieee;
use ieee.std_logic_1164.all;
use ieee.Numeric_std.all;

entity VGA_SyncTimer is
generic(
resolution: integer := 640;
frontPorch: integer := 16;
syncPulse: integer := 96;
backPorch: integer := 48
);
port(
EN: in std_logic;
CLK: in std_logic;
pixel: out std_logic_vector(15 downto 0);
sync: out std_logic;
nextLine: out std_logic
);

end entity;

architecture arc of VGA_SyncTimer is
signal counter : integer := 0;
begin

process(CLK)
begin
 if rising_edge(CLK) and EN = '1' then
	counter <= counter + 1;
	pixel <= std_logic_vector(to_unsigned(counter, pixel'length));
	if counter = resolution - 1 then
		
		nextLine <= '1';
	else
		nextLine <= '0';
	end if;
	
	if counter = resolution + frontPorch + syncPulse + backPorch then
		counter <= 0;
	end if;
 end if;
end process;

 
sync <= '1' when counter < resolution + frontPorch + syncPulse and counter > resolution + frontPorch else '0';

end architecture;