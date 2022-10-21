library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity DataReadTB is
port (
RGBout: out std_logic_vector(0 to 2);
Xout: out std_logic_vector(9 downto 0);
Yout: out std_logic_vector(9 downto 0);
WR: out std_logic;
AllRasterisationDone : out std_logic
);
end entity;

architecture arc of DataReadTB is
signal VGACLK: std_logic;

component RAM is
generic(
ADDRESS_LENGTH: integer := 4;
DATA_LENGTH: integer := 10
);
port(
CLK: in std_logic;

ADDRESS_IN : in std_logic_vector(ADDRESS_LENGTH - 1 downto 0);
DATA_OUT : out std_logic_vector(DATA_LENGTH - 1 downto 0)
);
end component;

component Data_Read_Interface is
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
end component;

component Rasteriser is
port(
EN: in std_logic;
CLK: in std_logic;
RGBout: out std_logic_vector(0 to 2);
Xout: out std_logic_vector(9 downto 0);
Yout: out std_logic_vector(9 downto 0);
WR: out std_logic;
DONE_RASTERISATION: out std_logic;
x0 : in signed(10 downto 0);
y0 : in signed(10 downto 0);
x1 : in signed(10 downto 0);
y1 : in signed(10 downto 0)
);
end component;



signal DataRAMData : std_logic_vector(9 downto 0);
signal DataRAMAddress : std_logic_vector(3 downto 0);
--Line rasteriser
signal LineDONE : std_logic;
signal StartLine : std_logic;
signal LineX0 : std_logic_vector(10 downto 0);
signal LineY0 : std_logic_vector(10 downto 0);
signal LineX1 : std_logic_vector(10 downto 0);
signal LineY1 : std_logic_vector(10 downto 0);

begin

dataReadInterface : Data_Read_Interface port map (CLK => VGACLK, DataRAMData => DataRAMData, DataRAMAddress => DataRAMAddress,
LineDONE => LineDONE, StartLine => StartLine, LineX0 => LineX0, LineY0 => LineY0, LineX1 => LineX1, LineY1 => LineY1, 
AllDone => AllRasterisationDone);

DataRAM : RAM port map(CLK => VGACLK, ADDRESS_IN => DataRAMAddress, DATA_OUT => DataRAMData);

Rast : Rasteriser port map(CLK => VGACLK, EN => StartLine, RGBout => RGBout, Xout => Xout, Yout => Yout, WR => WR, 
DONE_RASTERISATION => LineDONE, x0 => signed(LineX0), x1 => signed(LineX1), y0 => signed(Liney0), y1 => signed(Liney1));

process
begin
	VGACLK <= '0';
	wait for 20 ns;
	VGACLK <= '1';
	wait for 20 ns;
end process;

end architecture;