library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity VGA_Sync is
port(
CLK: in std_logic;
R: out std_logic;
G: out std_logic;
B: out std_logic;
VS: out std_logic;
HS : out std_logic
);
end entity;

architecture arc of VGA_Sync is
component VGA_SyncTimer is
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
end component;

signal horizontal: std_logic_vector(15 downto 0);
signal horizontalSync: std_logic;
signal horizontalNextLine: std_logic;

signal vertical: std_logic_vector(15 downto 0);
signal verticalSync: std_logic;
signal verticalNextLine: std_logic;

begin

horizontalSyncTimer : VGA_SyncTimer generic map(resolution => 640, frontPorch => 16, syncPulse => 96, backPorch => 48) port map(EN => '1', CLK => CLK, pixel => horizontal, sync => HS, nextLine => horizontalNextLine);
verticalSyncTimer : VGA_SyncTimer generic map(resolution => 480, frontPorch => 11, syncPulse => 2, backPorch => 33) port map(EN => horizontalNextLine,CLK => CLK, pixel => vertical, sync => VS, nextLine => verticalNextLine);

R <= '0' when unsigned(horizontal) < 100 else '1';
--R <= '0';
G <= '1';
B <= '1';
--process
--begin
	--CLK <= '0';
	--wait for 10ps;
	--CLK <= '1';
	--wait for 10ps;
--end process;
end architecture;