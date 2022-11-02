library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity VGA_Sync is
port(
EN: in std_logic;
CLK: in std_logic;
X: out std_logic_vector(15 downto 0);
Y: out std_logic_vector(15 downto 0);
VS: out std_logic;
HS : out std_logic;
DONE: out std_logic
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

signal horizontal: std_logic_vector(15 downto 0) := (others => 'Z');
signal horizontalSync: std_logic;
signal horizontalNextLine: std_logic;

signal vertical: std_logic_vector(15 downto 0) := (others => 'Z');
signal verticalSync: std_logic;
signal verticalNextLine: std_logic;
signal view: std_logic;
signal horizontalDone:integer := 0;

begin

horizontalSyncTimer : VGA_SyncTimer generic map(resolution => 640, frontPorch => 16, syncPulse => 96, backPorch => 48) port map(EN => EN, CLK => CLK, pixel => horizontal, sync => HS, nextLine => horizontalNextLine);
verticalSyncTimer : VGA_SyncTimer generic map(resolution => 480, frontPorch => 11, syncPulse => 2, backPorch => 33) port map(EN => horizontalNextLine,CLK => CLK, pixel => vertical, sync => VS, nextLine => verticalNextLine);

process
begin
	wait on CLK, EN;
	if EN = '0' then
		horizontalDone <= 0;
	elsif rising_edge(CLK) then
		if EN = '1' and to_integer(unsigned(vertical)) = 0 and horizontalDone > 10 then
			wait until rising_edge(CLK);
			--DONE <= '1';
		else
			DONE <= '0';
		end if;
		
		if horizontalNextLine = '1' then
			horizontalDone <= horizontalDone + 1;
		end if;
		--horizontalDone <= 0 when EN = '0' else horizontalDone + 1 when horizontalNextLine = '1';
		--DONE <= '1' when EN = '1' and to_integer(unsigned(vertical)) = 0 and horizontalDone > 10 else '0';
	end if;
end process;

--horizontalDone <= 0 when EN = '0' else horizontalDone + 1 when horizontalNextLine = '1';

view <= '0' when to_integer(unsigned(horizontal)) > 639 or to_integer(unsigned(vertical)) > 479 else '1';


X <= horizontal when view = '1' and EN = '1' else (others => 'Z');
Y <= vertical when view = '1' and EN = '1' else (others => 'Z');

--process
--begin
	--CLK <= '0';
	--wait for 10ps;
	--CLK <= '1';
	--wait for 10ps;
--end process;
end architecture;