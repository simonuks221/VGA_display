library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Data_Read_Interface is
port (
CLK: in std_logic;

--RAM in
DataRAMData : in std_logic_vector(9 downto 0);
DataRAMAddress : out std_logic_vector(2 downto 0);

--Line rasteriser
LineDONE : in std_logic;
StartLine : out std_logic;
LineX0 : out std_logic_vector(10 downto 0);
LineY0 : out std_logic_vector(10 downto 0);
LineX1 : out std_logic_vector(10 downto 0);
LineY1 : out std_logic_vector(10 downto 0)

);
end entity;

architecture arc of Data_Read_Interface is
signal lineAmount : integer := 0;
signal currentLine : integer := 0;
signal start : std_logic := '1';
signal running: std_logic := '0';
begin

process (CLK)
begin
	if rising_edge(CLK) then
		if start = '1' then
			start <= '0';
			running <= '1';
			DataRAMAddress <= std_logic_vector(to_unsigned(0, DataRAMAddress'length));
		end if;
		
		if running = '1' then
			if lineAmount = 0 then --No lines found, means read ram 0
				lineAmount <= to_integer(unsigned(DataRAMData));
			else --Running line reader
				DataRAMAddress <= std_logic_vector(to_unsigned(currentLine, DataRAMAddress'length));
				
			end if;
		end if;
	end if;
end process;

process (LineDONE)
begin
	if rising_edge(LineDONE) then
		
	end if;
end process;

end architecture;