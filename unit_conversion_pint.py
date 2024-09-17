import pint

ureg = pint.UnitRegistry(auto_reduce_dimensions=True, system='mks')
ureg.default_format = '.2f'

# distanza = 24 * ureg.meter + 3*ureg.cm
# print(distanza)
# print(distanza.magnitude, distanza.units)

Q_ = ureg.Quantity

distanza = Q_(24, "meter")+Q_(3, "cm")
print(distanza)
print(distanza.magnitude, distanza.units)

distanza = Q_(24, "km")

velocita = Q_(60, "m/s")
velocita = velocita.to("km/hour")
print(velocita)

velocita = Q_(61, "km/hour")
velocita = velocita.to("knot")
print(velocita)

tempo = Q_(1, "s")+Q_(1, "min")+Q_(1, "hour")
print(tempo.to("hour"))

velocita = distanza/tempo
velocita = velocita.to("m/s")  # .format_babel(locale='it_IT')
print("velocita", velocita)

home = Q_(0, ureg.degC)
print(home, home.to(ureg.degF))
home = Q_(100, ureg.degC)
print(home, home.to(ureg.degF))
