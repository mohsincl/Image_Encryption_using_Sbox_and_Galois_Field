#Elements of Cyclic Group, G 

a=2
b=1
mod=2**8

G=[[0 for i in xrange(16)] for i in xrange(16)]
flag=[[0 for i in xrange(16)] for i in xrange(16)]

for i in xrange(16):
	for j in xrange(16):
		if i==0 and j==0:
			matrix[i][j] = 0	
		else:		
			p=0
			for counter in xrange(8):
				if b&1 == 1: 
					p=p^a
				b>>=1	
				carry = a&0x80
				a<<=1
				if carry == 128:
					a = a^0x71
			p=p%mod					
			flag[p/16][p%16] = 1
			matrix[i][j]=p
			a=p
			b=2
									
print('\n'.join([''.join(['{:4}'.format(i) for i in j]) for j in matrix]))
