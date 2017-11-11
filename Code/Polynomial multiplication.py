# Example of Polynomial Multiplication

a=226
b=2
p=0
for counter in xrange(8):
	if (b&1) == 1: 
		p = p^a
	b >>= 1	
	carry = (a & 0x80)
	a <<= 1
	if carry == 128:
		a = a^0x71		

p%=256
print p
