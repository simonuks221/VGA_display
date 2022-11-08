library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use STD.textio.all;
use ieee.std_logic_textio.all;

entity TrigLUT is
port(
address: in std_logic_vector(8 downto 0); --9bits of data
data: out std_logic_vector(15 downto 0)
);
end entity;

architecture SinLUT of TrigLUT is
	subtype ram_t is std_logic_vector(15 downto 0);
	type ram_a is array (0 to 360) of ram_t;
	
	function PreloadSIN return ram_a is
		variable returnArray: ram_a;
		file FileHandle       : TEXT open READ_MODE is "C:\Users\simon\Desktop\UNI\VHDL\VGA\sine.txt"; --100 multiplied
		variable TempWord: integer;
		variable CurrentLine  : LINE;
	begin
	for i in 0 to (360-1) loop
		readline(FileHandle, CurrentLine);
		read(CurrentLine, TempWord);
		returnArray(i) := std_logic_vector(to_signed(TempWord, ram_t'length));
	end loop;
	return returnArray;
	end function;

	signal anglesSIN : ram_a := PreloadSIN;
	signal angleIndex : integer := 0;
begin
	--angleIndex <= to_integer(unsigned(address)) rem 360; --Rem not synthesizable
	angleIndex <= to_integer(unsigned(address));
	data <= anglesSIN(angleIndex);

end architecture;