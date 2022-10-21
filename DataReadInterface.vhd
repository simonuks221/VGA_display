library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Data_Read_Interface is
port (
CLK: in std_logic;

--RAM in
DataRAMData : in std_logic_vector(9 downto 0);
DataRAMAddress : out std_logic_vector(3 downto 0);

--Line rasteriser
LineDONE : in std_logic;
StartLine : out std_logic;
LineX0 : out std_logic_vector(10 downto 0);
LineY0 : out std_logic_vector(10 downto 0);
LineX1 : out std_logic_vector(10 downto 0);
LineY1 : out std_logic_vector(10 downto 0);
AllDone : out std_logic
);
end entity;

architecture arc of Data_Read_Interface is
signal start : std_logic := '1';
signal inLoop : std_logic := '0';
signal lineAmount : integer := 0;
signal lineIndex : integer := 0;
signal coordIndex : integer := 0;
signal doLine : std_logic := '0';
begin

process(CLK)
begin
	if rising_edge(CLK) then
		if doLine = '1' and LineDONE = '1' then
			doLine <= '0';
			if lineIndex + 1 = lineAmount then --Completed all lines
				AllDone <= '1'; --CHANGE HERE FOR MULTPLE FRAMES
				lineIndex <= 0;
			else
				--Didnt complete all lines yet
				lineIndex <= lineIndex + 1;
				inLoop <= '1';
				coordIndex <= 1;
				DataRAMAddress <= std_logic_vector(to_unsigned(1 + (lineIndex + 1) * 4, DataRAMAddress'length));
			end if;
		end if;
		if start = '1' then
			start <= '0';
			inLoop <= '1';
			DataRAMAddress <= std_logic_vector(to_unsigned(0, DataRAMAddress'length));
		else 
			if inLoop = '1' then
				if coordIndex = 0 then
					lineAmount <= to_integer(unsigned(DataRAMData));
					coordIndex <= 1;
					DataRAMAddress <= std_logic_vector(to_unsigned(1, DataRAMAddress'length));
				elsif coordIndex = 4 then
					coordIndex <= 0;
					inLoop <= '0';
					doLine <= '1';
				else
					DataRAMAddress <= std_logic_vector(to_unsigned(1 + coordIndex + lineIndex * 4, DataRAMAddress'length));
					coordIndex <= coordIndex + 1;
				end if;
			end if;
		end if;
	end if;
end process;

StartLine <= doLine;
LineX0 <= '0' & DataRAMData when inLoop = '1' and coordIndex = 1;
LineY0 <= '0' & DataRAMData when inLoop = '1' and coordIndex = 2;
LineX1 <= '0' & DataRAMData when inLoop = '1' and coordIndex = 3;
LineY1 <= '0' & DataRAMData when inLoop = '1' and coordIndex = 4;

end architecture;