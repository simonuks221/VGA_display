library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity RAM is
generic(
ADDRESS_LENGTH: integer := 3;
DATA_LENGTH: integer := 3
);
port(
CLK: in std_logic;

ADDRESS_IN : in std_logic_vector(ADDRESS_LENGTH - 1 downto 0);
DATA_OUT : out std_logic_vector(DATA_LENGTH - 1 downto 0)
);
end entity;

architecture arc of RAM is
type dataType is array(((ADDRESS_LENGTH**2) - 1) downto 0) of std_logic_vector(((DATA_LENGTH**2) - 1) downto 0);

function InitDummyData return dataType is
	variable returnData : dataType;
begin
	returnData := (others => (others => '0'));
	returnData(0) := "000000101";
	return returnData;
end function;


signal data: dataType := InitDummyData;
begin

DATA_OUT <= data(to_integer(unsigned(ADDRESS_IN)));


end architecture;