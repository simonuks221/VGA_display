library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity TB is

end entity;

architecture arc of TB is
signal VGACLK : std_logic;
signal RGB : std_logic_vector(0 to 2);
signal V: std_logic;
signal H: std_logic;
signal Xcord: std_logic_vector(9 downto 0);
signal Ycord: std_logic_vector(9 downto 0);
signal X : std_logic_vector(15 downto 0);
signal Y : std_logic_vector(15 downto 0);

signal WR: std_logic;
signal RGBbuffer : std_logic_vector(0 to 2);
signal Xin: std_logic_vector(9 downto 0);
signal Yin: std_logic_vector(9 downto 0);

signal DONE_RASTERISATION: std_logic;
signal DONE_SYNC: std_logic;
signal EN_VGA: std_logic;
signal EN_RASTERISATION: std_logic;

component Frame_Buffer is
port(
CLK: in std_logic;
RGBout: out std_logic_vector(0 to 2);
Xout: in std_logic_vector(9 downto 0);
Yout: in std_logic_vector(9 downto 0);

WR: in std_logic;
RGBin: in std_logic_vector(0 to 2);
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
VS : out std_logic;
DONE : out std_logic
);
end component;

component Graphics_pipeline_SM is
port(
EN : in std_logic;
RST: in std_logic;
CLK : in std_logic;

DONE_RASTERISATION: in std_logic;
DONE_SYNC: in std_logic;
EN_VGA: out std_logic;
EN_RASTERISATION: out std_logic
); 
end component;

component DataReadTB is
port (
RGBout: out std_logic_vector(0 to 2);
Xout: out std_logic_vector(9 downto 0);
Yout: out std_logic_vector(9 downto 0);
WR: out std_logic;
AllRasterisationDone : out std_logic
);
end component;

begin

dataReadComponent : DataReadTB port map(RGBout => RGBbuffer, Xout => Xin, Yout => Yin, WR => WR, AllRasterisationDone => DONE_RASTERISATION);

GraphicsPipelineSM : Graphics_pipeline_SM port map(EN => '1', RST => '0', CLK => VGACLK, 
DONE_RASTERISATION => DONE_RASTERISATION, 
EN_VGA => EN_VGA, EN_RASTERISATION => EN_RASTERISATION, DONE_SYNC => DONE_SYNC); --EN RASTERISATION NOT FIGURING ANYWHERE

vgaSync : VGA_Sync port map(EN => EN_VGA, X => X, Y => Y, VS => V, HS => H, CLK => VGACLK, DONE => DONE_SYNC);
frameBuffer: Frame_Buffer port map(CLK => VGACLK, RGBout => RGB, Xout => Xcord, Yout => Ycord, 
WR => WR, RGBin => RGBbuffer, Xin => Xin, Yin => Yin);

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