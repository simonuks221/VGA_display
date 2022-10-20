library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity TB is

end entity;

architecture arc of TB is
signal VGACLK : std_logic;
signal R : std_logic;
signal G : std_logic;
signal B : std_logic;
signal V: std_logic;
signal H: std_logic;
signal Xcord: std_logic_vector(9 downto 0);
signal Ycord: std_logic_vector(9 downto 0);
signal X : std_logic_vector(15 downto 0);
signal Y : std_logic_vector(15 downto 0);

signal WR: std_logic;
signal Rin: std_logic;
signal Gin: std_logic;
signal Bin: std_logic;
signal Xin: std_logic_vector(9 downto 0);
signal Yin: std_logic_vector(9 downto 0);

signal DONE_RASTERISATION: std_logic;
signal EN_VGA: std_logic;
signal EN_RASTERISATION: std_logic;

signal DataRAMOut: std_logic_vector(2 downto 0);

component Frame_Buffer is
port(CLK: in std_logic;
Rout: out std_logic;
Gout: out std_logic;
Bout: out std_logic;
Xout: in std_logic_vector(9 downto 0);
Yout: in std_logic_vector(9 downto 0);

WR: in std_logic;
Rin: in std_logic;
Gin: in std_logic;
Bin: in std_logic;
Xin: in std_logic_vector(9 downto 0);
Yin: in std_logic_vector(9 downto 0)
);
end component;

component VGA_Sync is
port(
EN: in std_logic;
CLK: in std_logic;
X: out std_logic_vector(15 downto 0);
Y: out std_logic_vector(15 downto 0);
HS : out std_logic;
VS : out std_logic
);
end component;

component Rasteriser is
port(
EN: in std_logic;
CLK: in std_logic;
Rout: out std_logic;
Gout: out std_logic;
Bout: out std_logic;
Xout: out std_logic_vector(9 downto 0);
Yout: out std_logic_vector(9 downto 0);
WR: out std_logic;
DONE_RASTERISATION: out std_logic
);
end component;

component Graphics_pipeline_SM is
port(
EN : in std_logic;
RST: in std_logic;
CLK : in std_logic;

DONE_RASTERISATION: in std_logic;

EN_VGA: out std_logic;
EN_RASTERISATION: out std_logic
); 
end component;

component RAM is
generic(
ADDRESS_LENGTH: integer := 3;
DATA_LENGTH: integer := 3
);
port(
CLK: in std_logic;

ADDRESS_IN : in std_logic_vector(ADDRESS_LENGTH - 1 downto 0);
DATA_OUT : out std_logic_vector(DATA_LENGTH - 1 downto 0)
);
end component;

begin
DataRAM : RAM generic map(ADDRESS_LENGTH => 3, DATA_LENGTH => 3) port map(CLK => VGACLK, ADDRESS_IN => "000", DATA_OUT =>DataRAMOut);
GraphicsPipelineSM : Graphics_pipeline_SM port map(EN => '1', RST => '0', CLK => VGACLK, DONE_RASTERISATION => DONE_RASTERISATION, 
EN_VGA => EN_VGA, EN_RASTERISATION => EN_RASTERISATION);
lineRasteriser: Rasteriser port map(DONE_RASTERISATION => DONE_RASTERISATION, EN => EN_RASTERISATION, CLK => VGACLK, Rout => Rin, Gout => Gin, Bout => Bin, Xout => Xin, Yout => Yin, WR => WR);
vgaSync : VGA_Sync port map(EN => EN_VGA, X => X, Y => Y, VS => V, HS => H, CLK => VGACLK);
frameBuffer: Frame_Buffer port map(CLK => VGACLK, Rout => R, Gout => G, Bout => B, Xout => Xcord, Yout => Ycord, 
WR => WR, Rin => Rin, Gin => Gin, Bin => Bin, Xin => Xin, Yin => Yin);

Xcord <= X(9 downto 0);
Ycord <= Y(9 downto 0);

process
begin
	VGACLK <= '0';
	wait for 20ns;
	VGACLK <= '1';
	wait for 20ns;
end process;

end architecture;