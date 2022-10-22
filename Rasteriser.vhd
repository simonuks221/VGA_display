library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Rasteriser is
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
end entity;

architecture arc of Rasteriser is
type vector2D is array(0 to 1) of std_logic_vector(9 downto 0);
signal xx0 : signed(10 downto 0) := to_signed(0, 11);
signal yy0 : signed(10 downto 0) := to_signed(1, 11);
signal xx1 : signed(10 downto 0) := to_signed(6, 11);
signal yy1 : signed(10 downto 0) := to_signed(4, 11);
signal error : signed(10 downto 0);

signal newX01 : signed(10 downto 0);
signal newY01 : signed(10 downto 0);
signal newError1 : signed(10 downto 0);
signal newError2 : signed(10 downto 0);


signal inLoop: std_logic := '0';
signal dx, sx, sy, dy: signed(10 downto 0);
begin

newError1 <= error + dy when error * 2 > dy and inLoop = '1' and xx0 /= xx1 else error;
newX01 <= xx0 + sx when error * 2 > dy and inLoop = '1' and xx0 /= xx1 else xx0;

newError2 <= newError1 + dx when error * 2 < dx and inLoop = '1' and yy0 /= yy1 else dx + dy when inLoop = '0' else newError1;
newY01 <= yy0 + sy when error * 2 < dx and inLoop = '1' and yy0 /= yy1 else yy0;

process (CLK)
begin
	if EN = '0' then
		inLoop <= '0';
		DONE_RASTERISATION <= '0';
		xx0 <= X0;
		yy0 <= Y0;
		xx1 <= X1;
		yy1 <= Y1;
	elsif rising_edge(CLK) then
		if EN = '1' then
			inLoop <= '1';
		end if;
		if inLoop <= '1' then
			xx0 <= newX01;
			yy0 <= newY01;
			error <= newError2;
			if xx0 = xx1 and yy0 = yy1 then
				inLoop <= '0';
				DONE_RASTERISATION <= '1';
			end if;
		end if;
	end if;
end process; 

dx <= abs(xx1 - xx0) when inLoop = '0'; --BLOGAI, bloagai ABS
sx <= to_signed(1, 11) when xx0 < xx1 else to_signed(-1, 11);
dy <= -abs(yy1 - yy0) when inLoop = '0';
sy <= to_signed(1, 11) when yy0 < yy1 else to_signed(-1, 11);

RGBout <= "100" when inLoop = '1' else "ZZZ";
Xout <= std_logic_vector(xx0(9 downto 0)) when inLoop = '1' else (others => 'Z');
Yout <= std_logic_vector(yy0(9 downto 0)) when inLoop = '1' else (others => 'Z');
WR <= inLoop;

--DONE_RASTERISATION <= '1' when inLoop = '0' and EN = '1' else '0';




end architecture;