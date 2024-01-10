import sympy

hailstones = [tuple(map(int, line.replace("@", ",").split(","))) for line in open("input.txt") ]

xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr, yr, zr, vxr, vyr, vzr")

equations = []

for sx, sy, sz, vx, vy, vz in hailstones:
    equations.append((xr - sx) * (vy - vyr) - (yr - sy) * (vx - vxr))
    equations.append((yr - sy) * (vz - vzr) - (zr - sz) * (vy - vyr))

result_l = sympy.solve(equations)
print(result_l)
result = result_l.pop()
answer = result[xr] + result[yr]+ result[zr]
print(f"Answer 2: {answer}")
