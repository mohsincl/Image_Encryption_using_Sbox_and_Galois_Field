# Generation of 8x8 S-box (and correspondingly, invertible S-box)
# Developed by AMS(c)

# Variable Initializations
a=1		# Initial condition
b=2		# Generator, g=2 (00000010)
mod=2**8	# Degree, n=8 ; S-box has g**n = 2**8 = 256 entries (8x8 S-box, meaning 8 inputs yields 8 outputs) 
dim=16		# Dimensions of S-box: 16x16

# Matrix Initializations
sbox=[[0 for i in xrange(dim)] for i in xrange(dim)]		# S-box
G=[[0 for i in xrange(dim)] for i in xrange(dim)]		# Multiplicative Cyclic Group, G
invert_G=[[0 for i in xrange(dim)] for i in xrange(dim)]	# Complement of G
flag=[[0 for i in xrange(dim)] for i in xrange(dim)]		# Flag matrix, to check if all values in range(0,255) are in group G
invert_sbox=[[0 for i in xrange(dim)] for i in xrange(dim)]	# Invertible S-box

# Computing elements of G (each value in G signify exponential representations of generator, g) 
for i in xrange(16):
	for j in xrange(16):
		if i==0 and j==0:			# Base case
			G[i][j] = 0			 
		else:
			# Compute Polynomial multiplication of a and b bit by bit
			p = 0				# Initializing product = 0
			for counter in xrange(8):	# Values a and b are in range(0,255) so we have 8 bits 
				if b&1 == 1:		# Check if the rightmost bit (LSB) in b equals 1
					p=p^a		# If true, XOR product with a
				b>>=1			# Right shift b (Divide b by 2)
				carry = a&0x80		# Before Left shifting a, store the Leftmost bit (MSB) in carry
				a<<=1			# Now Left shift a
				if carry == 0x80:	# Check if carry equals 1
					a = a^0x71	# If true, XOR a with 0x71; 0x71 (0111 0001) corresponds to irreducible polynomial f(x)
							# In the Research paper, f(x) = x^8+x^6+x^5+x^4+1 = (1 0111 0001) in binary, now you know :)  
			# Multiplication ends here

			p%=mod				# product mod 256
			flag[p/16][p%16]=1		# set flag corresponding to product
			G[p/16][p%16]=i*16+j		# update G
			a=p				# for the next iteration, use previously calculated product
			b=2				# reset b to 2 

# Invertible G (Swapped indexes of a with b in a:g^b)
for i in xrange(16):
	for j in xrange(16):
		index = G[i][j]
		invert_G[index/16][index%16] = 16*i+j

# Generation of S-box
phi = 1
for i in xrange(16):
	for j in xrange(16):
		if 16*i+j == 0:				# Base case in S-box, for index (16*i+j)=0, phi(0)=1 (as mentioned in Paper)  
			sbox[i][j] = phi 
		elif 16*i+j == 230:			# Exception case 1: index=230
			index = (phi+12+1)%mod		# At this point, phi = 255; adding 1 for adjusting index after mod
			phi = invert_G[index/16][index%16]
			sbox[i][j] = phi 
		elif 16*i+j == 234:			# Exception case 2: index=234
			index = (phi+18)%mod
			phi = invert_G[index/16][index%16]
			sbox[i][j] = phi
		elif 16*i+j == 255:			# Last element in S-box; phi(255)=0  
			sbox[i][j] = 0		 
		else:
			index = phi
			phi = invert_G[index/16][index%16]
			sbox[i][j] = phi 

# Invertible S-box
for i in xrange(16):
	for j in xrange(16):
		index = sbox[i][j]
		invert_sbox[index/16][index%16] = 16*i+j

# Display Matrices			
print '\nTABLE-1: CYCLIC MULTIPLICATIVE GROUP, G:'								
print('\n'.join([''.join(['{:4}'.format(i) for i in j]) for j in G]))
print '\nFLAG MATRIX:'								
print('\n'.join([''.join(['{:4}'.format(i) for i in j]) for j in flag]))
print '\nTABLE-1.5: INVERTIBLE G'								
print('\n'.join([''.join(['{:4}'.format(i) for i in j]) for j in invert_G]))
print '\nTABLE-2: GENERATED S-BOX:'								
print('\n'.join([''.join(['{:4}'.format(i) for i in j]) for j in sbox]))
print '\nTABLE-3: INVERTIBLE S-BOX:'								
print('\n'.join([''.join(['{:4}'.format(i) for i in j]) for j in invert_sbox]))

# S-Box Generation Complete :)
