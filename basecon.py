import math
import numpy as np

## TODO: negative numbers - need support for subtraction and onwards

class Num(object):
    ''' `Num` instance takes two semioptional* inputs: number (str), which is a base-n representation of a number, and base (int), which is the aforementioned n.
    *Semioptional in that if they are not entered, user will be prompted for them.
    `Num` instance stores number and base ; also calculates and stores base 10 value.
    `Num` instance can then undergo basic operations (Num/float,Num*Num,etc, all returning a new `Num` instance),
    and can be subjected to base conversion via the `.convert` method.
    
    Preconditions:
    -The number must be entered in string form (although if there are no alphabetic characters, `Num` can convert the number from a float/int).
    -The base must be an integer between 2 and 35, inclusive.
    
    Notes:
    -Digits with values 10 or higher are represented with letters of the alphabet (A=10,B=11,etc).
    -Special methods (e.g. addition) are present but not uniform in the type they return. Check documentation.
    -Note that while there is some support for fractional parts of numbers (in any legal base),
    numbers may not be rounded in a helpful manner.
    -Note that while there is some support for negative numbers, special methods (e.g. the 'floor' function) may not give
    expected results.    
    '''
    
    bkey = [str(i) for i in list(range(10))]
    bkey.extend(map(chr,range(65,91)))
    bkey.append('?')
    
    def _basecon(self,num,b1,b2=10):
        '''
        Convert numbers from one base to another (where A = 10, B = 11, etc).
        Preconditions:
        `num` is a string representing a positive int/float. `b1` and `b2` are integers between 2 and 35, inclusive.
        '''
        neg = (num[0] == '-')
        if neg:
            num = num[1:]
        num = list(str(num))
        for i in range(len(num)):
            if num[i] != '.':
                num[i] = Num.bkey.index(num[i].upper())
            #print('index ',num[i])
        #print('num but listified, ',num) #
        num10 = Num.to10(num,b1)
        #print('in base 10, ',num10) #
        if b2 == 1 and num10%1<.00001:
            final = int(num10)*'1'
        elif b2 in range(2,36):
            numb2 = Num.tobase((num10),b2)
            final =''.join(numb2)
        else:
            raise Exception('Base entered is outside of module\'s capacities. Bases must be between 2 and 35, inclusive.')
        if neg:
            final = '-' + final
        return final

    def to10(num,b1):
        ''' Convert number num, originally in base b1, to base 10 and return an int/float.
        '''
        try:
            dec = num.index('.')
        except:
            dec = len(num)
        big = num[:dec]
        small = num[dec+1:]
        num = big+small
        sum = 0
        place = len(big) - 1
        for i in num:
            sum += int(i)*(b1**place)
            place -= 1
        #print('in to10, val10 is',sum)
        #print('which, if rounded, is',np.round(sum,10))
        return np.round(sum,10)
        #return sum
    
    def tobase(num10,b2):
        ''' Convert num 10 (int/float in base ten) into a base-b2 string. Return string.
        '''
        left = num10
        numb2 = []
        tries = 0
        big = True
        b2digs = math.ceil(math.log(left+0.000000001,b2))
        if b2digs<0:
            b2digs = 0
        #print('have entered tobase\nconverting b10 number ',num10,' to base ',b2)
        try:
            maxkey = str(num10)
            dot = maxkey.find('.')
            max = dot-len(maxkey)
            #print('maxkey ',len(maxkey),' dot ',dot)
        except:
            max = 0
        #print('max ',max)
        if left<1 and big == True:
            numb2.extend([0,'.'])
            big = False
        while b2digs > max:
            #print('power ',b2digs)
            #print('thing:',(b2**(b2digs-1)))
            dig = int(left//(b2**(b2digs-1)))
            #print('dig ',dig)
            left -= dig*(b2**(b2digs-1))
            #print('left ',left)
            if left > b2**(b2digs-1)*.99:
                dig += 1
                left -= b2**(b2digs-1)
            #else:
            #    print(left-b2**(b2digs-1))
            numb2.append(dig)
            if b2digs==1 and big == True:
                numb2.append('.')
                big = False
            #print('number so far, ',numb2)
            tries += 1
            b2digs -= 1
            assert tries<100,'Got really long decimal? Sorry.'
        numb2 = [Num.bkey[i] if i is not '.' else '.' for i in numb2]
        if '.' in numb2:
            while numb2[-1] == '0':
                numb2 = numb2[:-1]
        if numb2[-1] == '.':
            numb2 = numb2[:-1]
        return numb2
    
    def normalize(num,base):
        ''' For internal use. Re-represent num in order to remove understandable-but-technically-illegal alphanumeric
        characters (e.g. '5' or 'A' in base 4). Return string.
        '''
        #print('normalizing with num ',num,' base ',base)
        return Num._basecon(self=None,num=num,b1=base,b2=base)
    
    def __init__(self,startnum=None,startbase=10):
        #print('initializing')
        if startnum == None:
            self.startnum = input('number? ').upper()
            self.startbase = int(input('base? '))
        else:
            self.startnum = str(startnum).upper()
            self.startbase = startbase
        #print('initializing; startnum is '+self.startnum+' ; startbase is '+str(self.startbase))
        if self.startnum[0] == '-':
            self.pos = False
            self.startnum = self.startnum[1:]
        else:
            self.pos = True
        #print('startnum is initially',self.startnum)
        self.startnum = Num.normalize(num=self.startnum,base=self.startbase)
        #print('normalized startnum is',self.startnum)
        self.val10 = float(self._basecon(num=self.startnum,b1=self.startbase,b2=10))
        #print('value in b10 is',self.val10)
        if not self.pos:
            self.val10 *= -1
    
    def convert(self,b2):
        ''' For user use! User calls `convert` via something like num1.convert(4), which would convert `Num` instance num1 into base 4.
        Change object attributes; return nothing.
        '''
        self.startnum = self._basecon(num=self.startnum,b1=self.startbase,b2=b2)
        self.startbase = b2
    
    def same_base(self,other):
        ''' Evaluate whether two objects are in the same base. Return bool.
        '''
        ty = type(other)
        if ty == Num:
            if self.startbase == other.startbase:
                return True
            else:
                return False
        elif ty == int or ty == float:
            if self.startbase == 10:
                return True
            else:
                return False
        else:
            return False
    
    def __add__(self,other):
        ''' Return `Num` instance.
        '''
        ty = type(other)
        if ty == Num:
            if self.startbase == other.startbase:
                base = self.startbase
                sum = str(self.val10+other.val10)
                if float(sum)<0:
                    ret = Num(self._basecon(num=str(0-float(sum)),b1=10,b2=base),base)
                    ret.pos = (ret.pos==False)
                    return ret
                else:
                    return Num(self._basecon(num=sum,b1=10,b2=base),base)
            else:
                if self.val10+other.val10<0:
                    ret = Num(str(-(self.val10+other.val10)),10)
                    ret.pos = (ret.pos==False)
                    return ret
                else:
                    return Num(str(self.val10+other.val10),10)
        elif ty in [int,float]:
            if self.val10+other<0:
                ret = Num(self._basecon(num=str(-(self.val10+other)),b1=10,b2=self.startbase),self.startbase)
                ret.pos = (ret.pos==False)
                return ret
            else:
                return Num(self._basecon(num=str(self.val10+other),b1=10,b2=self.startbase),self.startbase)
    
    def __radd__(self,other):
        ''' Return `Num` instance.
        '''
        return self.__add__(other)
    
    def __sub__(self,other):
        ''' Return `Num` instance.
        '''
        ty = type(other)
        if ty == Num:
            #if self.val10<other.val10:
                #raise Exception('Answer would be negative. Module currently does not support negative numbers.')
            #elif self.val10 == other.val10:
                #raise Exception('Answer would be zero. Module currently does not support Num == 0.')
            if True:
                if self.startbase == other.startbase:
                    base = self.startbase
                    diff = str(self.val10-other.val10)
                    return Num(self._basecon(num=diff,b1=10,b2=base),base)
                else:
                    return Num(str(self.val10-other.val10),10)
        elif ty in [int,float]:
            return Num(self._basecon(num=str(self.val10-other),b1=10,b2=self.startbase),self.startbase)
    
    def __rsub__(self,other):
        ''' Return `Num` instance.
        '''
        if type(other) in [float,int]:
            #if other <= self.val10:
                #raise Exception('Right-subtraction would involve negative numbers; module currently does not support negative numbers.')
            return Num(self._basecon(num=str(other-self.val10),b1=10,b2=self.startbase),self.startbase)
    
    def __mul__(self,other):
        ''' Return `Num` instance.
        '''
        ty = type(other)
        if ty == Num:
            if self.startbase == other.startbase:
                base = self.startbase
                prod = str(self.val10*other.val10)
                return Num(self._basecon(num=prod,b1=10,b2=base),base)
            else:
                return Num(str(self.val10*other.val10),10)
        elif ty in [float,int]:
            return Num(self._basecon(num=str(self.val10*other),b1=10,b2=self.startbase),self.startbase)
    
    def __rmul__(self,other):
        ''' Return `Num` instance.
        '''
        return self.__mul__(other)
    
    def __truediv__(self,other):
        ''' Return `Num` instance.
        '''
        ty = type(other)
        if ty == Num:
            #if self.val10 % other.val10 != 0:
            #    raise Exception('Answer would be fractional. Module currently does not support fractional numbers.')
            if True:
                if self.startbase == other.startbase:
                    base = self.startbase
                    div = str(self.val10/other.val10)
                    return Num(self._basecon(num=div,b1=10,b2=base),base)
                else:
                    return Num(str(self.val10/other.val10),10)
        elif ty in [float,int]:
            return Num(self._basecon(num=str(self.val10/other),b1=10,b2=self.startbase),self.startbase)
    
    def __rtruediv__(self,other):
        ''' Return `Num` instance.
        '''
        if type(other) in [float,int]:
            return Num(self._basecon(num=str(other/self.val10),b1=10,b2=self.startbase),self.startbase)
        
    def __floordiv__(self,other):
        ''' Return `Num` instance.
        '''
        ty = type(other)
        if ty == Num:
            if self.startbase == other.startbase:
                base = self.startbase
                div = str(self.val10//other.val10)
                return Num(self._basecon(num=div,b1=10,b2=base),base)
            else:
                return Num(str(self.val10//other.val10),10)
        elif ty in [float,int]:
            return Num(self._basecon(num=str(self.val10//other),b1=10,b2=self.startbase),self.startbase)
    
    def __rfloordiv__(self,other):
        ''' Return `Num` instance.
        '''
        if type(other) in [float,int]:
            return Num(self._basecon(num=str(other//self.val10),b1=10,b2=self.startbase),self.startbase)
    
    def __mod__(self,other):
        ''' Return `Num` instance.
        '''
        ty = type(other)
        if ty == Num:
            if self.startbase == other.startbase:
                base = self.startbase
                val = str(self.val10%other.val10)
                return Num(self._basecon(num=val,b1=10,b2=base),base)
            else:
                return Num(str(self.val10%other.val10),10)
        elif ty in [float,int]:
            return Num(self._basecon(num=str(self.val10%other),b1=10,b2=self.startbase),self.startbase)
    
    def __rmod__(self,other):
        ''' Return `Num` instance.
        '''
        if type(other) in [float,int]:
            return Num(self._basecon(num=str(other%self.val10),b1=10,b2=self.startbase),self.startbase)
    
    def __pow__(self,other):
        ''' Return `Num` instance.
        '''
        ty = type(other)
        if ty == Num:
            if self.startbase == other.startbase:
                base = self.startbase
                val = str(self.val10**other.val10)
                return Num(self._basecon(num=val,b1=10,b2=base),base)
            else:
                return Num(str(self.val10**other.val10),10)
        elif ty in [float,int]:
            return Num(self._basecon(num=str(self.val10**other),b1=10,b2=self.startbase),self.startbase)
    
    def __rpow__(self,other):
        ''' Return `Num` instance.
        '''
        if type(other) in [float,int]:
            return Num(self._basecon(num=str(other**self.val10),b1=10,b2=self.startbase),self.startbase)
    
    def __abs__(self):
        ''' Return string.
        '''
        return self.startnum
    
    def __int__(self):
        ''' Return int.
        '''
        return int(self.val10)
    
    def __float__(self):
        ''' Return float.
        '''
        return float(self.val10)
    
    def __round__(self,n=0):
        ''' Return string, for now.
        '''
        x = list(self.startnum)
        #print('x is ',x)
        base = self.startbase
        cutoff = base/2
        if '.' in x:
            while len(x)-x.index('.') > n+2:
                x = x[:-1]
            if n == 0:
                if Num.bkey.index(x[-1]) >= cutoff:
                    x[-3] = Num.bkey[Num.bkey.index(x[-3])+1]
                x.pop()
                x.pop()
            elif n>0:
                if Num.bkey.index(x[-1]) >= cutoff:
                    x[-2] = Num.bkey[Num.bkey.index(x[-2])+1]
                x.pop()
        result = ''.join(x)
        return Num.normalize(result,base)
    
    def __floor__(self):
        ''' Return string, for now.
        '''
        x = list(self.startnum)         
        while '.' in x:
            x = x[:-1]
        return ''.join(x)
    
    def __ceil__(self):
        ''' Return string, for now.
        '''
        x = list(self.startnum)
        base = self.startbase
        if '.' in x:
            extra = False
            ind = x.index('.')
            for i in x[ind+1:]:
                if int(i) > 0:
                    extra = True
            if extra:
                x[ind-1] = Num.bkey[Num.bkey.index(x[ind-1])+1]
        while '.' in x:
            x = x[:-1]
        result = ''.join(x)
        return Num.normalize(result,base)
    
    def __lt__(self,other):
        ''' Return bool.
        '''
        ty = type(other)
        if self.val10 < other.val10:
            return True
        else:
            return False
    
    def __le__(self,other):
        ''' Return bool.
        '''
        ty = type(other)
        if self.val10 <= other.val10:
            return True
        else:
            return False
    
    def __gt__(self,other):
        ''' Return bool.
        '''
        ty = type(other)
        if self.val10 > other.val10:
            return True
        else:
            return False
    
    def __ge__(self,other):
        ''' Return bool.
        '''
        ty = type(other)
        if self.val10 >= other.val10:
            return True
        else:
            return False
    
    def __eq__(self,other):
        ''' Return bool.
        '''
        ty = type(other)
        if self.val10 == other.val10:
            return True
        else:
            return False
    
    def __ne__(self,other):
        ''' Return bool.
        '''
        ty = type(other)
        if self.val10 != other.val10:
            return True
        else:
            return False
    
    def __is__(self,other):
        ''' Return bool.
        '''
        ty = type(other)
        if ty == Num:
            return (self.val10 == other.val10 and self.startnum == other.startnum)
        elif ty in [int,float]:
            return (self.startbase == 10 and self.val10 == other)
    
    def __str__(self):
        ''' Return plain-english string.
        '''
        sign = ''
        if self.pos == False:
            sign = '-'
        return ('number '+sign+self.startnum+' in base '+str(self.startbase))
    
    def __repr__(self):
        ''' Return string representation.
        '''
        sign = ''
        if self.pos == False:
            sign = '-'
        return str((sign+self.startnum,'b'+str(self.startbase)))
    
    
    


'''
for fxn form, not object form
'''

if __name__=='__main__':
    num = str(input('Number? '))
    b1 = int(input('Start base? '))
    b2 = int(input('End base? '))
    numcon = Num._basecon('a',num,b1,b2)
    print('%s in base %d is %s in base %d' % (num,b1,numcon,b2))
