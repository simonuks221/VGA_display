library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Rasteriser is
port(
CLK: in std_logic;
Rout: out std_logic;
Gout: out std_logic;
Bout: out std_logic;
Xout: out std_logic_vector(9 downto 0);
Yout: out std_logic_vector(9 downto 0)
);
end entity;

architecture arc of Rasteriser is
type vector2D is array(0 to 1) of std_logic_vector(9 downto 0);
signal x0 : signed(10 downto 0) := to_signed(0, 11);
signal y0 : signed(10 downto 0) := to_signed(0, 11);
signal x1 : signed(10 downto 0) := to_signed(7, 11);
signal y1 : signed(10 downto 0) := to_signed(4, 11);


signal inLoop: std_logic := '0';
signal start : std_logic := '1';
signal dx, sx, sy, dy: signed(10 downto 0);
begin

process (CLK)
variable error: integer := 0;
variable e2 : integer := 0;
begin
	if rising_edge(CLK) then
		if start = '1' then
			inLoop <= '1';
			start <= '0';
			error := to_integer(dx + dy);
		end if;
		
		if inLoop = '1' then
			start <= '0';
			if x0 = x1 and y0 = y1 then
				inLoop <= '0';
			else
				e2 := error * 2;
				if e2 >= dy then
					if x0 = x1 then
					
					else
						error := to_integer(error + dy);
						report "error1 "& integer'image(error);
						x0 <= x0 + sx;
					end if;
				end if;
				if e2 <= dx then
					if y0 = y1 then
					
					else
						error := to_integer(error + dx);
						report "error2 "& integer'image(error);
						y0 <= y0 + sy;
					end if;
				end if;
			end if;
			--report "error "& integer'image(error);
		end if;
	end if;
end process;

dx <= abs(x1 - x0) when start = '1'; --BLOGAI, nera ABS
sx <= to_signed(1, 11) when x0 < x1 else to_signed(-1, 11);
dy <= -(y1 - y0) when start = '1';
sy <= to_signed(1, 11) when y0 < y1 else to_signed(-1, 11);
--error <= to_signed(7, 11);




end architecture;