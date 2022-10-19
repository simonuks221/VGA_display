library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity TB is

end entity;

architecture arc of TB is
signal VGACLK : std_logic;
signal CLK : std_logic;
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
CLK: in std_logic;
X: out std_logic_vector(15 downto 0);
Y: out std_logic_vector(15 downto 0);
HS : out std_logic;
VS : out std_logic
);
end component;

component Rasteriser is
port(
CLK: in std_logic;
Rout: out std_logic;
Gout: out std_logic;
Bout: out std_logic;
Xout: out std_logic_vector(9 downto 0);
Yout: out std_logic_vector(9 downto 0);
WR: out std_logic
);
end component;

begin

lineRasteriser: Rasteriser port map(CLK => VGACLK, Rout => Rin, Gout => Gin, Bout => Bin, Xout => Xin, Yout => Yin, WR => WR);
vgaSync : VGA_Sync port map(X => X, Y => Y, VS => V, HS => H, CLK => VGACLK);
frameBuffer: Frame_Buffer port map(CLK => VGACLK, Rout => R, Gout => G, Bout => B, Xout => Xcord, Yout => Ycord, 
WR => WR, Rin => Rin, Gin => Gin, Bin => Bin, Xin => Xin, Yin => Yin);

Xcord <= X(9 downto 0);
Ycord <= Y(9 downto 0);

--process
--begin
	--Xcord <= std_logic_vector(to_unsigned(1, Xcord'length));
	--Ycord <= std_logic_vector(to_unsigned(1, Ycord'length));
	--wait for 100ns;
	--Xcord <= std_logic_vector(to_unsigned(101, Xcord'length));
	--Ycord <= std_logic_vector(to_unsigned(101, Ycord'length));
	--wait;
--end process;

process
begin
	VGACLK <= '0';
	wait for 20ns;
	VGACLK <= '1';
	wait for 20ns;
end process;

--process 
--begin
	--for i in 0 to 100 loop
		--CLK <= '0';
		--wait for 10ps;
		--CLK <= '1';
		--wait for 10ps;
	--end loop;
--end process;


end architecture;