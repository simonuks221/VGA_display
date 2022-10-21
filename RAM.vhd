library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity RAM is
generic(
ADDRESS_LENGTH: integer := 4; --bits
DATA_LENGTH: integer := 10 --bits
);
port(
CLK: in std_logic;

ADDRESS_IN : in std_logic_vector(ADDRESS_LENGTH - 1 downto 0);
DATA_OUT : out std_logic_vector(DATA_LENGTH - 1 downto 0)
);
end entity;

architecture arc of RAM is
type dataType is array(((ADDRESS_LENGTH**2) - 1) downto 0) of std_logic_vector((DATA_LENGTH - 1) downto 0);

function InitDummyData return dataType is
	variable returnData : dataType;
begin
	returnData := (others => (others => '0')); --Init all data to 0
	
	returnData(0) := std_logic_vector(to_unsigned(2, DATA_LENGTH)); --We will have 3 lines
	
	returnData(1) := std_logic_vector(to_unsigned(0, DATA_LENGTH));
	returnData(2) := std_logic_vector(to_unsigned(0, DATA_LENGTH));
	returnData(3) := std_logic_vector(to_unsigned(7, DATA_LENGTH));
	returnData(4) := std_logic_vector(to_unsigned(4, DATA_LENGTH));
	
	returnData(5) := std_logic_vector(to_unsigned(0, DATA_LENGTH));
	returnData(6) := std_logic_vector(to_unsigned(0, DATA_LENGTH));
	returnData(7) := std_logic_vector(to_unsigned(7, DATA_LENGTH));
	returnData(8) := std_logic_vector(to_unsigned(4, DATA_LENGTH));
	
	return returnData;
end function;


signal data: dataType := InitDummyData;
begin

DATA_OUT <= data(to_integer(unsigned(ADDRESS_IN)));


end architecture;