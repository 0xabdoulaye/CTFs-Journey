from Crypto.Util.number import *

grocery = bytes_to_long(open("grocery-list.out", "rb").read())
many_time = bytes_to_long(open("many-time-pad.out", "rb").read())

groceries = b"I need to buy 15 eggs, 1.7 kiloliters of milk, 11000 candles, 12 cans of asbestos-free cereal, and 0.7 watermelons."
groceries = bytes_to_long(groceries)


flag = (grocery ^ many_time) ^ groceries
flag = long_to_bytes(flag)

print("grocery : ", grocery)
print("many_time : ", many_time)

print("FLAG : ", flag)
