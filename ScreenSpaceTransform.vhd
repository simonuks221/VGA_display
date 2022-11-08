library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ScreenSpaceTransform is
	port(
	pointX: in std_logic_vector(15 downto 0);
	pointY: in std_logic_vector(15 downto 0);
	pointZ: in std_logic_vector(15 downto 0);
	
	screenPointX: out std_logic_vector(15 downto 0);
	screenPointY: out std_logic_vector(15 downto 0);
	screenPointZ: out std_logic_vector(15 downto 0);
	
	CLK: in std_logic
	);
end entity;

architecture arc of ScreenSpaceTransform is
signal cameraX: std_logic_vector(15 downto 0) := std_logic_vector(to_signed(1, pointX'length));
signal cameraY: std_logic_vector(15 downto 0) := std_logic_vector(to_signed(1, pointX'length));
signal cameraZ: std_logic_vector(15 downto 0) := std_logic_vector(to_signed(1, pointX'length));

signal displaySurfaceX: std_logic_vector(15 downto 0) := std_logic_vector(to_signed(100, pointX'length));
signal displaySurfaceY: std_logic_vector(15 downto 0) := std_logic_vector(to_signed(100, pointX'length));
signal displaySurfaceZ: std_logic_vector(15 downto 0) := std_logic_vector(to_signed(150, pointX'length));

signal cameraAngleX: std_logic_vector(15 downto 0) := std_logic_vector(to_signed(0, pointX'length));
signal cameraAngleY: std_logic_vector(15 downto 0) := std_logic_vector(to_signed(0, pointX'length));
signal cameraAngleZ: std_logic_vector(15 downto 0) := std_logic_vector(to_signed(0, pointX'length));

signal x, y, z : std_logic_vector(15 downto 0) := (others => '1');
signal cx, cy, cz, sx, sy, sz : integer := 1;

signal dx, dy, dz : integer := 1;

signal bx, by : integer := 1;

begin

 x <= std_logic_vector(signed(pointX) - signed(cameraX));
 y <= std_logic_vector(signed(pointY) - signed(cameraY));
 z <= std_logic_vector(signed(pointZ) - signed(cameraZ));
 
 cx <= 1;
 cy <= 1; --Get cos
 cz <= 1;
 
 sx <= 0;
 sy <= 0; --Get sin
 sz <= 0;
 
 dx <= cy * (sz * to_integer(signed(y)) + cz * to_integer(signed(x))) - sy * to_integer(signed(z));
 dy <= sx * (cy * to_integer(signed(z)) + sy*(sz*to_integer(signed(y))+cz*to_integer(signed(x)))) + cx*(cz*to_integer(signed(y))-sz*to_integer(signed(x)));
 dz <= cx*(cy*to_integer(signed(z))+sy*(sz*to_integer(signed(y))+cz*to_integer(signed(x)))) - sx*(cz*to_integer(signed(y))-sz*to_integer(signed(x)));
 
 bx <= to_integer(signed(displaySurfaceZ))/dz*dx + to_integer(signed(displaySurfaceX));
 by <= to_integer(signed(displaySurfaceZ))/dz*dy + to_integer(signed(displaySurfaceY));
 
 screenPointX <= std_logic_vector(to_signed(bx, screenPointX'length));
 screenPointY <= std_logic_vector(to_signed(by, screenPointX'length));
 screenPointZ <= std_logic_vector(to_signed(dz, screenPointX'length));
 
 process(CLK)
 begin
	if rising_edge(CLK) then
		--TODO: Gauti sin ir cos reiksmes
	end if;
 end process;
 

end architecture;